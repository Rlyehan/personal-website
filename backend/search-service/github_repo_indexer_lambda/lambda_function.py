import os
import json
import base64
import requests
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch

GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ELASTICSEARCH_HOST = os.environ["ELASTICSEARCH_HOST"]

INDEX_NAME = "repositories"


def get_github_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_readme(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        readme_content = response.json()["content"]
        return base64.b64decode(readme_content).decode("utf-8")
    else:
        return ""


def get_repository_tags(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/topics"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.mercy-preview+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()["names"]
    else:
        return []

def convert_embedding_to_nested_format(embedding):
    return [{"value": float_value} for float_value in embedding]


def create_opensearch_index(client, index_name):
    if not client.indices.exists(index_name):
        index_body = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                }
            },
            "mappings": {
                "properties": {
                    "repository_name": {"type": "text"},
                    "description": {"type": "text"},
                    "readme": {"type": "text"},
                    "tags": {"type": "keyword"},
                    "embedding": {"type": "nested", "properties": {"value": {"type": "float"}}}}
                }
            }
        client.indices.create(index_name, body=index_body)


def index_repositories(client, repositories, model):
    for repo in repositories:
        repo_name = repo["name"]
        repo_description = repo["description"] if repo["description"] else ""
        repo_readme = get_readme(GITHUB_USERNAME, repo_name)
        repo_tags = get_repository_tags(GITHUB_USERNAME, repo_name)

        text = f"{repo_name} {repo_description} {repo_readme}"
        embedding = model.encode(text)
        nested_embedding = convert_embedding_to_nested_format(embedding)

        document = {
            "repository_name": repo_name,
            "description": repo_description,
            "readme": repo_readme,
            "tags": repo_tags,
            "embedding": nested_embedding
        }

        client.index(index=INDEX_NAME, body=document)


def lambda_handler(event, context):
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        http_compress = True, # enables gzip compression for request bodies
        use_ssl = False,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False
    )
    create_opensearch_index(client, INDEX_NAME)

    model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
    repositories = get_github_repositories(GITHUB_USERNAME)

    index_repositories(client, repositories, model)

    return {
        "statusCode": 200,
        "body": json.dumps("Repositories indexed successfully."),
    }
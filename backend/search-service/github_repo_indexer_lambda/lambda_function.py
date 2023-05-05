import base64
import json
import os
import re
import ssl
from http import client

import hnswlib
import numpy as np
import requests
from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer

GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ELASTICSEARCH_HOST = os.environ["ELASTICSEARCH_HOST"]

INDEX_NAME = "repositories"
HNSW_INDEX_NAME = "hnsw_index"



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


def create_hnsw_index(dim):
    index = hnswlib.Index(space="cosine", dim=dim)
    return index


def save_hnsw_index(hnsw_index, file_name):
    hnsw_index.save_index(file_name)


def load_hnsw_index(file_name, dim):
    hnsw_index = hnswlib.Index(space="cosine", dim=dim)
    hnsw_index.load_index(file_name)

    return hnsw_index



def convert_embedding_to_dense_vector_format(embedding):
    return np.array(embedding)



def add_embeddings_to_hnsw_index(hnsw_index, embeddings, repo_ids):
    hnsw_index.init_index(max_elements=len(embeddings), ef_construction=100, M=16)
    hnsw_index.add_items(embeddings, repo_ids)


def index_repositories(client, repositories, model):
    repo_ids = []
    embeddings = []

    for repo in repositories:
        repo_id = repo["id"]
        repo_name  = repo["name"]
        repo_description = repo["description"] if repo["description"] else ""
        repo_readme = get_readme(GITHUB_USERNAME, repo_name)
        repo_tags = get_repository_tags(GITHUB_USERNAME, repo_name)

        text = f"{repo_name} {repo_description} {repo_readme}"
        embedding = model.encode(text)
        embedding_as_list = embedding.tolist()

        document = {
            "repository_name": repo_name,
            "description": repo_description,
            "readme": repo_readme,
            "tags": repo_tags,
            "embedding": embedding_as_list
        }

        print("Embedding shape:", embedding.shape)
        print(f"Indexing document: {document}")
        client.index(index=INDEX_NAME, body=document)

        repo_ids.append(repo_id)
        embeddings.append(embedding)

    return repo_ids, embeddings


def create_opensearch_index(client, index_name):
    if not client.indices.exists(index_name):
        index_body = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                "index.knn": True
            },
            "mappings": {
                "properties": {
                    "repository_name": {"type": "text"},
                    "description": {"type": "text"},
                    "readme": {"type": "text"},
                    "tags": {"type": "keyword"},
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": 384,
                        "method": {
                            "name": "hnsw",
                            "engine": "nmslib",
                            "space_type": "l2",
                            "parameters": {
                                "ef_construction": 128,
                                "m": 24
                            }
                        }
                    }
                }
            }
        }
        client.indices.create(index_name, body=index_body)


def delete_opensearch_index(client, index_name):
    if client.indices.exists(index_name):
        client.indices.delete(index_name)


def lambda_handler(event, context):
    client = OpenSearch(
        hosts=[ELASTICSEARCH_HOST],
        http_compress=True,
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False
    )
    delete_opensearch_index(client, INDEX_NAME)
    create_opensearch_index(client, INDEX_NAME)

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    repositories = get_github_repositories(GITHUB_USERNAME)

    repo_ids, embeddings = index_repositories(client, repositories, model)
    
    hnsw_index = create_hnsw_index(dim=len(embeddings[0]))
    add_embeddings_to_hnsw_index(hnsw_index, embeddings, repo_ids)
    save_hnsw_index(hnsw_index, HNSW_INDEX_NAME)

    return {
        "statusCode": 200,
        "body": json.dumps("Repositories and HNSW index created successfully.")
    }
import os
from typing import List, Tuple

from github import get_readme, get_repository_tags
from opensearchpy import OpenSearch

GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
INDEX_NAME = "repositories"


def index_repositories(
    client: OpenSearch, repositories: List[dict], model
) -> Tuple[List[int], List[List[float]]]:
    repo_ids = []
    embeddings = []

    for repo in repositories:
        repo_id = repo["id"]
        repo_name = repo["name"]
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
            "embedding": embedding_as_list,
        }

        client.index(index=INDEX_NAME, body=document)

        repo_ids.append(repo_id)
        embeddings.append(embedding)

    return repo_ids, embeddings


def create_opensearch_index(client: OpenSearch, index_name: str) -> None:
    if not client.indices.exists(index_name):
        index_body = {
            "settings": {
                "index": {"number_of_shards": 1, "number_of_replicas": 1},
                "index.knn": True,
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
                            "parameters": {"ef_construction": 128, "m": 24},
                        },
                    },
                }
            },
        }
        client.indices.create(index_name, body=index_body)


def delete_opensearch_index(client: OpenSearch, index_name: str) -> None:
    if client.indices.exists(index_name):
        client.indices.delete(index_name)

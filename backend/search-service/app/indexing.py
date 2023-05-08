from typing import List

import hnswlib
import numpy as np
from opensearchpy import OpenSearch
from opensearchpy.exceptions import RequestError


def create_hnsw_index(dim: int) -> hnswlib.Index:
    index = hnswlib.Index(space="cosine", dim=dim)
    return index


def save_hnsw_index(hnsw_index: hnswlib.Index, file_name: str) -> None:
    hnsw_index.save_index(file_name)


def load_hnsw_index(file_name: str, dim: int) -> hnswlib.Index:
    hnsw_index = hnswlib.Index(space="cosine", dim=dim)
    hnsw_index.load_index(file_name)

    return hnsw_index


def convert_embedding_to_dense_vector_format(embedding) -> np.ndarray:
    return np.array(embedding)


def add_embeddings_to_hnsw_index(
    hnsw_index: hnswlib.Index, embeddings: List[List[float]], repo_ids: List[int]
) -> None:
    hnsw_index.init_index(max_elements=len(embeddings), ef_construction=100, M=16)
    hnsw_index.add_items(embeddings, repo_ids)


def search_similar_repositories(
    client: OpenSearch, query_vector: List[float], index_name: str, top_k: int
) -> List[dict]:
    query_body = {
        "size": top_k,
        "query": {"knn": {"embedding": {"vector": query_vector, "k": top_k}}},
        "_source": ["repository_name", "description", "readme", "tags"],
    }

    try:
        response = client.search(index=index_name, body=query_body)
    except RequestError as e:
        print("Error:", e.info)
        raise e

    return response["hits"]["hits"]


def retrieve_all_repositories(client, index_name):
    query_body = {
        "size": 1000,
        "query": {"match_all": {}},
        "_source": {"excludes": ["embedding", "readme"]},
    }

    try:
        response = client.search(index=index_name, body=query_body)
    except RequestError as e:
        print("Error:", e.info)
        raise e

    return response["hits"]["hits"]

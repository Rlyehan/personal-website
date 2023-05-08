import os
from typing import List

from fastapi import FastAPI
from github import get_github_repositories
from indexing import (
    add_embeddings_to_hnsw_index,
    create_hnsw_index,
    retrieve_all_repositories,
    save_hnsw_index,
    search_similar_repositories,
)
from opensearch import (
    create_opensearch_index,
    delete_opensearch_index,
    index_repositories,
)
from opensearchpy import OpenSearch
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

app = FastAPI()

GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ELASTICSEARCH_HOST = os.environ["ELASTICSEARCH_HOST"]

INDEX_NAME = "repositories"
HNSW_INDEX_NAME = "hnsw_index"


client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_compress=True,
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")


class SearchRequest(BaseModel):
    text: str
    top_k: int = 5


class SearchResult(BaseModel):
    repository_name: str
    description: str
    tags: List[str]
    score: float


class Repository(BaseModel):
    repository_name: str
    description: str
    tags: List[str]


@app.post("/search", response_model=List[SearchResult])
async def search_repositories(search_request: SearchRequest) -> List[SearchResult]:
    text = search_request.text

    embedding = model.encode([text], convert_to_tensor=True)[0].cpu().numpy().tolist()
    search_result = search_similar_repositories(
        client, embedding, "repositories", search_request.top_k
    )

    formatted_results = [
        SearchResult(
            repository_name=hit["_source"]["repository_name"],
            description=hit["_source"]["description"],
            tags=hit["_source"]["tags"],
            score=hit["_score"],
        )
        for hit in search_result
    ]

    return formatted_results


@app.get("/repositories", response_model=List[Repository])
async def get_all_repositories() -> List[Repository]:
    results = retrieve_all_repositories(client, "repositories")

    formatted_results = [
        Repository(
            repository_name=hit["_source"]["repository_name"],
            description=hit["_source"]["description"],
            tags=hit["_source"]["tags"],
        )
        for hit in results
    ]

    return formatted_results


@app.post("/index_repositories/")
async def index_repositories_handler() -> dict:
    delete_opensearch_index(client, INDEX_NAME)
    create_opensearch_index(client, INDEX_NAME)

    repositories = await get_github_repositories(GITHUB_USERNAME)

    repos_ids, embeddings = index_repositories(client, repositories, model)

    hnsw_index = create_hnsw_index(dim=len(embeddings[0]))
    add_embeddings_to_hnsw_index(hnsw_index, embeddings, repos_ids)
    save_hnsw_index(hnsw_index, HNSW_INDEX_NAME)

    return {"message": f"Indexed {len(repositories)} repositories."}

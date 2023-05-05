from typing import List

from fastapi import FastAPI
from opensearchpy import OpenSearch
from opensearchpy.exceptions import RequestError
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

app = FastAPI()

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
    readme: str
    tags: List[str]
    score: float


class Repository(BaseModel):
    repository_name: str
    description: str
    tags: List[str]


def search_similar_repositories(client, query_vector, index_name, top_k):
    query_body = {
        "size": top_k,
        "query": {"knn": {"embedding": {"vector": query_vector, "k": top_k}}},
        "_source": ["repository_name", "description", "readme", "tags"],
    }

    print("opensearch query:", query_body)
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


@app.post("/search", response_model=List[SearchResult])
async def search_repositories(search_request: SearchRequest):
    text = search_request.text

    embedding = model.encode([text], convert_to_tensor=True)[0].cpu().numpy().tolist()
    print("Embedding:", embedding)
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
async def get_all_repositories():
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

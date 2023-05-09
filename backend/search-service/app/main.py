import base64
import logging
import os
from typing import List, Tuple

import hnswlib
import httpx
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opensearchpy import OpenSearch
from opensearchpy.exceptions import RequestError
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

INDEX_NAME = "repositories"
HNSW_INDEX_NAME = "hnsw_index"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

trace.set_tracer_provider(TracerProvider())

index_counter = Counter("index_operations", "Number of index operations")

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer(__name__)


async def github_request(method: str, url: str, headers: dict) -> List[dict]:
    with tracer.start_as_current_span("github_request") as span:
        span.set_attribute("http.method", method)
        span.set_attribute("http.url", url)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, headers=headers)
            if response.status_code == 200:
                logger.info(
                    f"Successful {method} request to {url}",
                    extra={"url": url, "method": method},
                )
                return response.json()
            else:
                logger.error(
                    f"Error during {method} request to {url}: {response.status_code} - {response.text}",
                    extra={
                        "url": url,
                        "method": method,
                        "status_code": response.status_code,
                        "response_text": response.text,
                    },
                )
                return []
        except Exception as e:
            logger.exception(
                f"Exception during {method} request to {url}: {e}",
                extra={"url": url, "method": method},
            )
            return []


async def get_github_repositories(username: str) -> List[dict]:
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    return await github_request("GET", url, headers)


async def get_readme(username: str, repo_name: str) -> str:
    url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = await github_request("GET", url, headers)

    if response:
        readme_content = response[0]["content"]
        decoded_content = base64.b64decode(readme_content).decode("utf-8")
        return decoded_content
    else:
        return ""


async def get_repository_tags(username: str, repo_name: str) -> List[str]:
    url = f"https://api.github.com/repos/{username}/{repo_name}/topics"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.mercy-preview+json",
    }
    response = await github_request("GET", url, headers)

    if response:
        return response[0]["names"]
    else:
        return []


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
        logger.error("Error:", e.info)
        raise e

    return response["hits"]["hits"]


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

        index_counter.inc()

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


def retrieve_all_repositories(client, index_name):
    query_body = {
        "size": 1000,
        "query": {"match_all": {}},
        "_source": {"excludes": ["embedding", "readme"]},
    }

    try:
        response = client.search(index=index_name, body=query_body)
    except RequestError as e:
        logger.error("Error:", e.info)
        raise e

    return response["hits"]["hits"]


app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_compress=True,
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

model = SentenceTransformer("flax-sentence-embeddings/all_datasets_v4_MiniLM-L6")


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
    with tracer.start_as_current_span("search_repositories") as span:
        span.set_attribute("search.text", search_request.text)
        span.set_attribute("search.top_k", search_request.top_k)
        try:
            text = search_request.text

            embedding = (
                model.encode([text], convert_to_tensor=True)[0].cpu().numpy().tolist()
            )
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
        except Exception as e:
            logger.exception(
                f"Exception during search for {search_request.text}: {e}",
                extra={"search_text": search_request.text},
            )
            return []


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
    with tracer.start_as_current_span("index_repositories_handler") as span:
        span.set_attribute("index_name", INDEX_NAME)
        try:
            delete_opensearch_index(client, INDEX_NAME)
            create_opensearch_index(client, INDEX_NAME)

            repositories = await get_github_repositories(GITHUB_USERNAME)

            repos_ids, embeddings = index_repositories(client, repositories, model)

            hnsw_index = create_hnsw_index(dim=len(embeddings[0]))
            add_embeddings_to_hnsw_index(hnsw_index, embeddings, repos_ids)
            save_hnsw_index(hnsw_index, HNSW_INDEX_NAME)

            logger.info(
                f"Indexed {len(repositories)} repositories.",
                {"repositories_indexed": len(repositories)},
            )
            return {"message": f"Indexed {len(repositories)} repositories."}
        except Exception as e:
            logger.exception(f"Exception during indexing: {e}")
            return {"message": "Error occurred during indexing."}

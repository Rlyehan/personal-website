import os

from lambda_function import INDEX_NAME
from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer

ELASTICSEARCH_HOST = os.environ["ELASTICSEARCH_HOST"]

def search_similar_repositories(client, query_text, model, size=10):
    query_embedding = model.encode(query_text)

    search_body = {
        "query": {
            "knn": {
                "embedding": {
                    "vector": query_embedding.tolist(),
                    "k": size
                }
            }
        },
        "_source": ["repository_name", "description", "tags"]
    }

    response = client.search(index=INDEX_NAME, body=search_body)
    return response['hits']['hits']




client = OpenSearch(
    hosts=[ELASTICSEARCH_HOST],
    http_compress=True,
    use_ssl=False,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False
)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Test the search function
query_text = "Natural Language Processing"
search_results = search_similar_repositories(client, query_text, model)

for result in search_results:
    print("Repository:", result["_source"]["repository_name"])
    print("Description:", result["_source"]["description"])
    print("Tags:", result["_source"]["tags"])
    print("Similarity score:", result["_score"])
    print("\n")

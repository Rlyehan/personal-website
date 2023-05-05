import requests

index_name = "repositories"

url = f"http://localhost:9200/{index_name}/_search"
query = {
    "size": 5,  # The number of documents you want to retrieve
    "_source": ["repository_name", "embedding.value"],  # The fields you want to retrieve
    "query": {
        "match_all": {}
    }
}

response = requests.post(url, json=query)

if response.status_code == 200:
    search_results = response.json()["hits"]["hits"]
    for idx, result in enumerate(search_results):
        print(f"Document {idx + 1}:")
        print(f"Repository name: {result['_source']['repository_name']}")
        embedding_values = [value_dict["value"] for value_dict in result['_source']['embedding']]
        print(f"Embedding: {embedding_values}\n")
else:
    print(f"Request failed with status code {response.status_code}")

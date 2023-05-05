import requests

url = "http://127.0.0.1:8000/search"
data = {"text": "Code review", "top_k": 5}

response = requests.post(url, json=data)

if response.status_code == 200:
    search_results = response.json()
    for idx, result in enumerate(search_results):
        print(f"Result {idx + 1}:")
        print(f"Repository name: {result['repository_name']}")
        print(f"Description: {result['description']}")
        print(f"Tags: {result['tags']}")
        print(f"Score: {result['score']}\n")
else:
    print(f"Request failed with status code {response.status_code}")

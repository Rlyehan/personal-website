import base64
import os
from typing import List

import httpx

GITHUB_USERNAME = os.environ["GITHUB_USERNAME"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]


async def github_request(method: str, url: str, headers: dict) -> List[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
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

import requests

def search_wikipedia(query):
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["extract"]
    return "Not found"

print(search_wikipedia("Agentic_AI"))
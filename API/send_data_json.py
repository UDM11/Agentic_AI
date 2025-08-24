import requests

url = "https://httpbin.org/post"

payload = {
    "task": "search",
    "query": "Agentic AI"
}

response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
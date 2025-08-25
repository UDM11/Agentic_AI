import requests

# Simple GET request 
response = requests.get("https://api.github.com")

# Status code
print(response.status_code)

# Response Content
print(response.text)
print(response.json())
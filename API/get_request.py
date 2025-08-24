import requests
url = "https://api.github.com/repos/psf/requests"
response = requests.get(url)

if response.status_code == 200:
    print("Request was successful")

elif response.status_code == 404:
    print("Resource not found")

else:
    print("An error occurred")
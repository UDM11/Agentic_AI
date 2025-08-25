import requests

def log_activity(task, status):
    url = "https://example.com/api/logs"
    payload = {"task": task, "status": status}
    headers = {"Authorization": "Bearer TOKEN_ABC"}
    requests.post(url, json=payload, headers=headers)


log_activity("search", "success")
print(log_activity)
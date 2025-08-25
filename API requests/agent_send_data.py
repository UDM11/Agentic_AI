import requests

def send_task_to_service(task_name):
    url = "http://example.com/api/tasks"
    payload = {"task": task_name}
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    response =requests.post(url, json=payload, headers=headers)
    return response.status_code

print(send_task_to_service("research"))
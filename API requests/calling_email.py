import requests

def send_email(recipient, subject, body):
    url = "https://example.com/api/send_email"
    payload = {
        "to": recipient,
        "subject": subject,
        "body": body
    }
    headers = {"Authorization": "Bearer TOKEN_123"}
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code

print(send_email("user@example.com", "Task Completed", "Your report is ready."))
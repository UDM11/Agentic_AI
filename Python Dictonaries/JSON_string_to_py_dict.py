import json

data = '{"name": "AgentX", "role": "Researcher"}'
parsed = json.loads(data)
print(parsed)
import json

agent_data = {
    "name" : "AgentX",
    "active" : True
}
json_string = json.dumps(agent_data)
print(json_string)
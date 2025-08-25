import json

agent = {
    "name": "AgentX",
    "role": "Writer"
}

# access
print(agent["name"])

# add
agent["status"] = "active"

#remove
del agent["role"]


print(agent)
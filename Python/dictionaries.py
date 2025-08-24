# creating
agent_memory = {"name": "AgentX", "store": "active"}

#access
print(agent_memory["name"])

#update
agent_memory["status"] = "idle"

#add
agent_memory["last_task"] = "search"
print(agent_memory)
agent_memory = {}

def remember(key, value):
    agent_memory[key] = value

def recall(key):
    return agent_memory.get(key, "Not found")


remember("user_name", "Alice")
remember("last_query", "Agentic Ai overview")

print(recall("user_name"))
print(recall("last_query"))
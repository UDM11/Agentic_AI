def search(query):
    return f"Results for {query}"

def summarize(text):
    return f"Summary of {text}"

def agent_pipeline(query):
    results = search(query)
    return summarize(results)

print(agent_pipeline("Ai agents in 2025"))

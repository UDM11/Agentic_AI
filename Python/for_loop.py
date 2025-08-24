tasks = ["search", "analyze", "calculate"]

for task in tasks:
    print("Agent is perform:", task)

tools = {"search": "Google Api", "calculate": "Math Engine"}
for key, value in tools.items():
    print(f"{key} {value}")
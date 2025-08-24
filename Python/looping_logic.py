tasks = ["search", "fact-check", "write"]

for task in tasks:
    print(f"Executing {task}...")

# Retry with while loop 
retries = 0
success = False

while retries < 3 and not success:
    print("Agent is attemtping task...")
    #simulate failure
    success = (retries == 2)
    retries += 1

print("Task completed:", success)
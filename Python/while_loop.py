attempts = 0

while attempts < 3:
    print("trying API call...")
    success = False
    if success:
        break
    attempts += 1

else:
    print("Max retrives reached, please check the API key or netweork connection")

    #continue

for i in range(5):
    if i == 2:
        continue
    print("Iteration:", i)
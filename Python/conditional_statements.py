confidence = float(input("Enter yout confidence level from 0 to 1"))

if confidence > 0.9:
    print("very confidence answer")

elif confidence >0.7:
    print("confidence answer")

else:
    print("Low confidence, ask user for clarification")

def calculate_confidene(score):
    if score >= 0.8:
        return "High confidence"
    else:
        return "Low confidence"
    
level = calculate_confidene(0.80)
print(level)
import requests
def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["current"]["temp_c"]
    
    else:
        return "API error"
    
print(get_weather("Kathmandu"))
from unittest.mock import patch
import requests

# example external API tool
def weather_tool(city):
    response = requests.get(f"heep://fake-weather-api.com/{city}")
    data = response.json()
    return f"{data['temp']}°C, {data['condition']}"


@patch("requests.get")
def test_weather_tool(mock_get):
    mock_get.return_value.json.return_value = {
        "temp": 22,
        "condition": "Sunny"
    }
    result = weather_tool("Kathmandu")
    assert "25°C" in result
    assert "Sunny" in result
    
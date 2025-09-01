import unittest
from unittest.mock import patch
import requests

# Tools
def calculator_tool(expr):
    try:
        return str(eval(expr))
    except:
        return "Invalid expression."

def weather_tool(city):
    response = requests.get(f"http://fake-weather-api/{city}")
    data = response.json()
    return f"{data['temp']}°C, {data['condition']}"

def echo_tool(message):
    return f"You said: {message}"

# Agent
class SimpleAgent:
    def __init__(self):
        self.memory = []

    def run(self, query):
        self.memory.append(query)
        query_lower = query.lower()

        if "weather" in query_lower:
            city = query.split("in")[-1].strip().replace("?", "")
            return weather_tool(city)
        elif any(op in query for op in ["+", "-", "*", "/"]):
            return calculator_tool(query)
        elif "echo" in query_lower:
            message = query.replace("echo", "").strip()
            return echo_tool(message)
        else:
            return "I don't know how to answer that."

agent = SimpleAgent()

# Unit Tests
class TestTools(unittest.TestCase):
    def test_calculator_tool(self):
        self.assertEqual(calculator_tool("2 + 3"), "5")
        self.assertEqual(calculator_tool("10 * 2"), "20")
        self.assertEqual(calculator_tool("invalid"), "Invalid expression.")

    def test_echo_tool(self):
        self.assertEqual(echo_tool("Hello"), "You said: Hello")
        self.assertEqual(echo_tool("Test"), "You said: Test")

# Integration Tests
class TestAgentIntegration(unittest.TestCase):
    @patch("requests.get")
    def test_agent_weather(self, mock_get):
        # Mock weather API
        mock_get.return_value.json.return_value = {"temp": 30, "condition": "cloudy"}

        response = agent.run("What's the weather in Pokhara?")
        self.assertIn("30°C", response)
        self.assertIn("cloudy", response)

    def test_agent_calculator(self):
        response = agent.run("7 + 8")
        self.assertEqual(response, "15")

    def test_agent_echo(self):
        response = agent.run("echo Hello world!")
        self.assertEqual(response, "You said: Hello world!")

    def test_agent_unknown_query(self):
        response = agent.run("Tell me a joke")
        self.assertEqual(response, "I don't know how to answer that.")

    def test_agent_memory(self):
        # Memory should store all queries
        agent.run("1 + 1")
        agent.run("echo Memory test")
        self.assertIn("1 + 1", agent.memory)
        self.assertIn("echo Memory test", agent.memory)

# Run Tests
if __name__ == "__main__":
    unittest.main()

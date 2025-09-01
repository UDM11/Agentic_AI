def test_agent_weather(agent):
    response = agent.run("What's the weather in Kathmandu?")
    assert "Kathmandu" in response
    assert "°C" in response
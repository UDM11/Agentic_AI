from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

# Define a dummy agent for demonstration purposes
class DummyAgent:
    def run(self, question):
        return f"Received question: {question}"

agent = DummyAgent()

@app.post("/agent")
async def run_agent(query: Query):
    response = agent.run(query.question)
    return {"response": response}
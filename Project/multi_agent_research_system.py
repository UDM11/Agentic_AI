from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Define CrewAI tools with proper type annotations
class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the web for information"

    def _run(self, query: str) -> str:
        return f"Search web results for: {query}"

class GrammarTool(BaseTool):
    name: str = "grammar_checker"
    description: str = "Check and correct grammar"

    def _run(self, text: str) -> str:
        return f"Checked grammar for: {text}"

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    openai_api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Define agents
researcher = Agent(
    role="Researcher",
    goal="Gather data on AI trends in 2025",
    backstory="You are an expert researcher who finds reliable sources",
    tools=[WebSearchTool()],
    llm=llm
)

writer = Agent(
    role="Writer",
    goal="Write a concise report based on research",
    backstory="You are a skilled writer who creates clear, engaging reports",
    llm=llm
)

editor = Agent(
    role="Editor",
    goal="Polish and fact-check the report",
    backstory="You are a meticulous editor ensuring high-quality output",
    tools=[GrammarTool()],
    llm=llm
)

# Define tasks with dependencies
research_task = Task(
    description="Research AI trends in 2025",
    agent=researcher,
    expected_output="Raw findings about AI trends in 2025"
)

write_task = Task(
    description="Write a report from research data",
    agent=writer,
    dependencies=[research_task],
    expected_output="Draft report on AI trends in 2025"
)

edit_task = Task(
    description="Polish and finalize the report",
    agent=editor,
    dependencies=[write_task],
    expected_output="Final well-polished report"
)

# Create crew
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task]
)

# Run the pipeline
result = crew.kickoff()
print(result)

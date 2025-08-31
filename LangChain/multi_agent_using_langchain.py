import os
from dotenv import load_dotenv
from collections import Counter

# LangChain imports
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

# Load API key
load_dotenv()

llm = ChatOpenAI(
    model_name="deepseek/deepseek-chat-v3.1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,
    max_tokens=1000
)

# Path Generator (ToT)
class PathGeneratorAgent:
    def __init__(self, llm):
        self.llm = llm
    
    def generate_paths(self, query, num_paths=3):
        template = """
        You are a problem-solving assistant.
        Generate {num_paths} different ways to approach this problem:
        {query}
        Number each path clearly.
        """
        prompt = PromptTemplate(
            input_variables=["query", "num_paths"],
            template=template
        )
        response = self.llm([HumanMessage(content=prompt.format(query=query, num_paths=num_paths))])
        text = response.content
        paths = [line.strip() for line in text.split("\n") if line.strip() and line[0].isdigit()]
        return paths

# Reasoning Agent (CoT)
class ReasoningAgent:
    def __init__(self, llm):
        self.llm = llm
    
    def reason_path(self, path):
        template = """
        Solve the following step by step using Chain-of-Thought reasoning:
        {path}
        Show all steps before giving the final answer.
        """
        prompt = PromptTemplate(
            input_variables=["path"],
            template=template
        )
        response = self.llm([HumanMessage(content=prompt.format(path=path))])
        return response.content

# Aggregator Agent (Self-Consistency) 
class AggregatorAgent:
    def __init__(self):
        pass
    
    def aggregate(self, results):
        answers = []
        for res in results:
            if "Answer:" in res:
                answers.append(res.split("Answer:")[-1].strip())
            elif "Final Answer:" in res:
                answers.append(res.split("Final Answer:")[-1].strip())
            else:
                answers.append(res.strip())
        most_common = Counter(answers).most_common(1)[0][0]
        return most_common
    
# Workflow
query = "If a train leaves at 3 PM at 60 km/h and another at 4 PM at 80 km/h from the same station, when do they meet?"

# Generate multiple paths
path_agent = PathGeneratorAgent(llm)
paths = path_agent.generate_paths(query)
print("Generated Paths (ToT):", paths, "\n")

# Chain-of-Thought reasoning for each path
reasoning_agent = ReasoningAgent(llm)
cot_results = [reasoning_agent.reason_path(path) for path in paths]
print("Chain-of-Thought Results:")
for idx, res in enumerate(cot_results, 1):
    print(f"Path {idx} reasoning:\n{res}\n")

# Self-Consistency aggregation
aggregator_agent = AggregatorAgent()
final_answer = aggregator_agent.aggregate(cot_results)
print("Self-Consistency Final Answer:", final_answer)

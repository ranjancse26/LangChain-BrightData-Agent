from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool

from tools.google_search import GoogleSearchTool
from tools.airbnb import AirbnbTool
from gemini_summary import summarize_with_gemini
from llm import GeminiLLM

load_dotenv()

llm = GeminiLLM()

tools = [
    Tool.from_function(func=GoogleSearchTool(), name="Google Search", description="Search Google for answers"),
    Tool.from_function(func=AirbnbTool(), name="Airbnb Search", description="Search Airbnb for listings")
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

if __name__ == "__main__":
    query = "Find Airbnb listings in New York and summarize Google reviews about staying there."
    try:
        result = agent.run(query)
        summary = summarize_with_gemini(result)
        print("\n===== RAW RESULT =====")
        print(result)
        print("\n===== SUMMARY =====")
        print(summary)
    except Exception as e:
        print(f"[Agent Error] {e}")

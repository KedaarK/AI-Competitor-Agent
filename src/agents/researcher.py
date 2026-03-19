# src/agents/researcher.py
import os
from crewai import Agent, LLM
from crewai.tools import tool  # Use this to wrap your function
from dotenv import load_dotenv
from src.tools.scraper import scrape_social_post # Now this import will work!

load_dotenv()

groq_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# We turn your function into a Tool the Agent can "grasp"
@tool("scrape_social_tool")
def scrape_social_tool(url: str):
    """
    Scrapes social media content from a URL.
    """
    from src.tools.scraper import scrape_social_post
    return scrape_social_post(url)

# Define the Agent
researcher_agent = Agent(
    role='Social Media Researcher',
    goal='Identify recent content themes for {competitor}',
    backstory=(
        "You are an expert at finding patterns in social media. "
        "When you use the scrape_social_tool, ensure you pass only the URL string. "
        "Expect raw text in return and summarize it into 3 clear themes."
    ),
    tools=[scrape_social_tool],
    llm=groq_llm,
    verbose=True,
    allow_delegation=False,
    max_iter=3 # Prevents infinite loops if tool calling fails
)
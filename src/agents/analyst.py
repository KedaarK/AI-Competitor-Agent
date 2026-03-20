# src/agents/analyst.py
import os
from crewai import Agent, LLM
from src.database.memory import query_memory # We use our Memory tool
from dotenv import load_dotenv

load_dotenv()

groq_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# This agent looks at the "Numbers" and "Themes" together
analyst_agent = Agent(
    role='Competitive Strategy Analyst',
    goal='Provide a transparent comparison of {comp1} and {comp2} with a detailed metrics table.',
    backstory=(
        "You are a rigorous data auditor. You MUST use the 'VIEWS' and 'METRICS' provided. "
        "Your report must include: "
        "1. A side-by-side comparison table of the latest video views. "
        "2. An 'Action Score' (1-10) based on how many action verbs (Run, Power, Build) are in titles. "
        "3. A 'Transparency Note' explaining if any brand is hiding its engagement data."
    ),
    llm=groq_llm,
    verbose=True
)
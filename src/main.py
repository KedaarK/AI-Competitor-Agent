# src/main.py
from crewai import Task, Crew
from src.agents.researcher import researcher_agent

def run_competitor_check(competitor_name, url):
    # 1. Use placeholders {competitor} and {url} in the description.
    # This lets CrewAI pass these values cleanly to the Agent.
    collection_task = Task(
        description="Scrape the provided URL {url} and summarize the top 3 themes for {competitor}.",
        expected_output="A summary of the latest strategy used by the competitor.",
        agent=researcher_agent
    )

    # 2. Create the Crew
    crew = Crew(
        agents=[researcher_agent],
        tasks=[collection_task]
    )

    # 3. Pass the actual values into kickoff as a dictionary.
    # This is the 'CrewAI way' that prevents formatting errors.
    return crew.kickoff(inputs={
        'competitor': competitor_name,
        'url': url
    })

if __name__ == "__main__":
    result = run_competitor_check("Nike", "https://www.youtube.com/@nike/videos")
    print("\n\n########################")
    print("## AGENT FINAL REPORT ##")
    print("########################\n")
    print(result)
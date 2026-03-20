# src/main.py
from src.agents.researcher import researcher_agent
from src.agents.analyst import analyst_agent
from src.tools.scraper import scrape_social_post
from src.database.memory import store_posts, query_memory, reset_memory
from crewai import Task, Crew



def run_competitor_check(competitor_name, url):
    # 1. Scrape and Store (The "Memory" Step)
    print(f"--- Scraping {competitor_name} ---")
    raw_content = scrape_social_post(url)
    
    if "Error" not in raw_content:
        # Split into individual lines for the Vector DB
        lines = [line.strip() for line in raw_content.split('\n') if len(line.strip()) > 5]
        store_posts(competitor_name, lines)

    # 2. Analysis Task (Using the data we just got)
    analysis_task = Task(
        description=(
            f"Based ONLY on this data: {raw_content}, "
            f"identify the top 3 marketing themes for {competitor_name}. "
            "Do not use any tools. Just summarize the text provided."
        ),
        expected_output="A list of 3 themes with a brief explanation for each.",
        agent=researcher_agent
    )

    crew = Crew(agents=[researcher_agent], tasks=[analysis_task])
    return crew.kickoff()


def run_comparison(comp1, comp2):
    # 1. Ask ChromaDB for the data we stored earlier
    comp1_data = query_memory(comp1)
    comp2_data = query_memory(comp2)

    # 2. Create the Comparison Task
    comparison_task = Task(
        description=(
            f"Compare these two competitors:\n"
            f"{comp1}: {comp1_data}\n"
            f"{comp2}: {comp2_data}\n\n"
            "Analyze who is using more 'Action' oriented content and who has better "
            "metrics like Views/Likes mentioned in the titles."
        ),
        expected_output="A professional comparison report with a clear winner in strategy.",
        agent=analyst_agent
    )

    crew = Crew(agents=[analyst_agent], tasks=[comparison_task])
    return crew.kickoff()


if __name__ == "__main__":
    # Now you can run them one after another
    print("--- Starting Competitive Analysis ---")
    reset_memory()
    # Run individual checks (This populates the Vector DB)
    run_competitor_check("Nike", "https://www.youtube.com/@nike/videos")
    run_competitor_check("Adidas", "https://www.youtube.com/@adidas/videos")
    
    # NOW CALL THE ANALYST
    print("\n--- ANALYST AGENT IS NOW COMPARING DATA ---")
    comparison_report = run_comparison("Nike", "Adidas")
    
    print("\n\n###############################")
    print("## FINAL STRATEGY COMPARISON ##")
    print("###############################\n")
    print(comparison_report)
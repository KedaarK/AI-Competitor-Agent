# src/tools/scraper.py
from playwright.sync_api import sync_playwright

def scrape_social_post(url: str):
    with sync_playwright() as p:
        # Using standard chromium instead of headless_shell for better compatibility
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print(f"--- Scraping {url} ---")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # Give the page 3 seconds to load dynamic content
            page.wait_for_timeout(3000) 
            
            # Get the text of the page
            # Note: On Twitter, this will likely still show a "Login" screen
            content = page.locator("body").inner_text()
            
            browser.close()
            return content[:2000] # Limit text so we don't blow the LLM tokens
        except Exception as e:
            browser.close()
            return f"Error: {str(e)}"
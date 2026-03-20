# src/tools/scraper.py
import time
import random
from playwright.sync_api import sync_playwright
from playwright_stealth.stealth import Stealth

stealth = Stealth()


def scrape_social_post(url: str):
    with sync_playwright() as p:
        # 1. Launch Browser
        browser = p.chromium.launch(headless=True)
        
        # 2. Setup a Human Profile
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
        
        context = browser.new_context(
            user_agent=user_agent,
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = context.new_page()

        # 3. Apply Stealth (This hides 'navigator.webdriver' and other bot flags)
        stealth.apply_stealth_sync(page)

        try:
            # 4. Human-like Delay (Wait 2-5 seconds before visiting)
            time.sleep(random.uniform(2, 5))
            
            print(f"--- Stealthily Navigating to {url} ---")
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Scroll down slightly to trigger lazy-loading (common on Instagram/Twitter)
            page.mouse.wheel(0, 500)
            time.sleep(2)

            # Platform Detection (Keep your elif logic here)
            if "youtube.com" in url:
                content = page.locator("#video-title, #description-text").all_inner_texts()
            elif "twitter.com" in url or "x.com" in url:
                content = page.locator("article div[lang]").all_inner_texts()
            else:
                content = page.locator("body").inner_text()

            browser.close()
            return "\n".join(content[:10]) if isinstance(content, list) else str(content)[:2000]

        except Exception as e:
            browser.close()
            return f"Stealth Scraping Error: {str(e)}"
import time
import random
import logging
from playwright.sync_api import sync_playwright

# Importing configurations and utility functions
from config import BASE_URL, SEARCH_TERMS, GEO_LOCATION, USER_AGENT, MAX_PAGES, OUTPUT_FILE
from utils import save_to_csv, generate_visual_report

def run() -> None:
    """
    Main execution function for the B2B Scraper.
    Uses stateless sessions to bypass anti-bot protections.
    """
    logging.info("Starting extraction process...")
    all_leads = []
    
    with sync_playwright() as p:
        for page_num in range(1, MAX_PAGES + 1):
            # Launch a fresh browser session for each page to maintain anonymity
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=USER_AGENT)
            page = context.new_page()
            
            url = f"{BASE_URL}?search_terms={SEARCH_TERMS}&geo_location_terms={GEO_LOCATION}&page={page_num}"
            logging.info(f"Navigating to: {url}")
            
            try:
                page.goto(url, wait_until="domcontentloaded")
                
                # Wait for the main results container to appear
                page.wait_for_selector(".result", timeout=25000)
                
                cards = page.query_selector_all(".result")
                logging.info(f"Page {page_num}: Found {len(cards)} items.")
                
                for card in cards:
                    # Select elements with explicit None checks to ensure code stability
                    name_el = card.query_selector(".business-name")
                    phone_el = card.query_selector(".phones")
                    web_el = card.query_selector(".links [href^='http']")
                    
                    name_text = name_el.inner_text() if name_el is not None else "N/A"
                    phone_text = phone_el.inner_text() if phone_el is not None else "N/A"
                    web_url = web_el.get_attribute("href") if web_el is not None else "N/A"
                    
                    all_leads.append({
                        "Business Name": name_text,
                        "Phone": phone_text,
                        "Website": web_url
                    })
                    
            except Exception as e:
                logging.error(f"Error on page {page_num}: {e}")
            
            # Close session and wait before initiating the next request
            browser.close()
            sleep_time = random.uniform(8, 15)
            logging.info(f"Session closed. Waiting {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
            
    # Save the aggregated results to CSV
    save_to_csv(all_leads, OUTPUT_FILE)
    
    # Trigger data visualization immediately after saving the dataset
    logging.info("Generating visual analytics report...")
    generate_visual_report(OUTPUT_FILE)
    
    logging.info("Extraction and reporting tasks completed successfully.")

if __name__ == "__main__":
    run()
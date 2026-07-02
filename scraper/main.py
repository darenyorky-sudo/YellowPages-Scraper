import time
import random
import logging
from playwright.sync_api import sync_playwright
from config import BASE_URL, SEARCH_TERMS, GEO_LOCATION, USER_AGENT, MAX_PAGES, SENDER_EMAIL, RECEIVER_EMAIL
from utils import save_to_csv, generate_visual_report, send_email_report, get_timestamped_filename

def run() -> None:
    logging.info("Starting extraction process...")
    # Generate unique filenames for each run
    csv_file = get_timestamped_filename("leads", "csv")
    img_file = get_timestamped_filename("chart", "png")
    all_leads = []
    
    with sync_playwright() as p:
        for page_num in range(1, MAX_PAGES + 1):
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=USER_AGENT)
            page = context.new_page()
            
            url = f"{BASE_URL}?search_terms={SEARCH_TERMS}&geo_location_terms={GEO_LOCATION}&page={page_num}"
            logging.info(f"Navigating to: {url}")
            
            try:
                page.goto(url, wait_until="domcontentloaded")
                page.wait_for_selector(".result", timeout=25000)
                cards = page.query_selector_all(".result")
                
                for card in cards:
                    name_el = card.query_selector(".business-name")
                    phone_el = card.query_selector(".phones")
                    web_el = card.query_selector(".links [href^='http']")
                    
                    all_leads.append({
                        "Business Name": name_el.inner_text() if name_el else "N/A",
                        "Phone": phone_el.inner_text() if phone_el else "N/A",
                        "Website": web_el.get_attribute("href") if web_el else "N/A"
                    })
            except Exception as e:
                logging.error(f"Error on page {page_num}: {e}")
            
            browser.close()
            # Random delay to simulate human behavior
            time.sleep(random.uniform(8, 15))
            
    # Post-processing pipeline
    save_to_csv(all_leads, csv_file)
    generate_visual_report(csv_file, img_file)
    send_email_report(csv_file, img_file, SENDER_EMAIL, RECEIVER_EMAIL)
    logging.info("Pipeline execution finished successfully.")

if __name__ == "__main__":
    run()
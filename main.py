import requests
import gspread
import random
import time
import logging

# OAuth2 authentication for Google Sheets
from oauth2client.service_account import ServiceAccountCredentials

# Selenium imports for web scraping
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# Chrome WebDriver manager for automatic driver handling
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging configuration for debugging and tracking issues
logging.basicConfig(level=logging.INFO)

# -----------------------
# Mailchimp API Configuration
# -----------------------
MAILCHIMP_API_KEY = ""  # Full Mailchimp API key (format: abc123-us3)
MAILCHIMP_DC = ""  # Mailchimp data center (extracted from API key after '-usX')
MAILCHIMP_LIST_ID = ""  # Mailchimp Audience/List ID
MAILCHIMP_CAMPAIGN_ENDPOINT = f"https://{MAILCHIMP_DC}.api.mailchimp.com/3.0/campaigns"

# -----------------------
# Google Sheets API Configuration
# -----------------------
SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
CREDENTIALS_FILE = ""  # JSON credentials file for Google Sheets API
SPREADSHEET_NAME = ""  # Name of the target Google Sheet

# -----------------------
# Request Headers (Used for making HTTP requests to avoid bot detection)
# -----------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.85 Safari/537.36"
}

# -----------------------
# Fetch Mailchimp Campaign Data via API
# -----------------------
def get_mailchimp_data():
    headers = {"Authorization": f"apikey {MAILCHIMP_API_KEY}"}
    response = requests.get(MAILCHIMP_CAMPAIGN_ENDPOINT, headers=headers)
    if response.status_code == 200:
        return response.json()["campaigns"]
    else:
        logging.error("Error fetching Mailchimp data: %s", response.text)
        return []

# -----------------------
# Update Google Sheets with Data
# -----------------------
def update_google_sheets(campaigns, scraped_data):
    """
    Updates the Google Sheet with Mailchimp campaign data and scraped tweet data.
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).sheet1
    
    # Clear previous data
    sheet.clear()
    
    # Insert campaign data
    sheet.append_row(["Campaign Name", "Status", "Emails Sent", "Open Rate", "Click Rate"])
    for campaign in campaigns:
        sheet.append_row([
            campaign["settings"]["title"],
            campaign["status"],
            campaign["emails_sent"],
            campaign["report_summary"]["open_rate"],
            campaign["report_summary"]["click_rate"]
        ])
    
    # Add separator before adding scraped tweet data
    sheet.append_row(["", "", "", "", ""])
    sheet.append_row(["Scraped Tweet Data"])
    
    # Insert scraped tweet data
    if scraped_data and isinstance(scraped_data[0], dict):
        sheet.append_row(["Timestamp", "Tweet Text"])
        for tweet in scraped_data:
            sheet.append_row([tweet.get("timestamp", "N/A"), tweet.get("text", "")])
    else:
        for item in scraped_data:
            sheet.append_row([item])
    
    logging.info("Google Sheets updated successfully!")

# -----------------------
# Scrape Dynamic Web Pages using Selenium
# -----------------------
def scrape_dynamic_site(url, scroll_pause_time=3, max_scroll_attempts=30, headless=False):
    """
    Scrapes dynamic sites (like X/Twitter) using Selenium with automated scrolling.
    """
    try:
        # Configure Selenium options
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("window-size=1920,1080")
        
        # Initialize WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        
        # Wait for page to load
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        time.sleep(2)
        
        # Locate tweets using the best available selector
        tweet_selector = "div[data-testid='tweet']"
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, tweet_selector)))
        except TimeoutException:
            tweet_selector = "article"
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, tweet_selector)))
        
        tweets_data = []
        seen_tweets = set()
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        for _ in range(max_scroll_attempts):
            tweet_elements = driver.find_elements(By.CSS_SELECTOR, tweet_selector)
            for tweet in tweet_elements:
                try:
                    tweet_text = tweet.text.strip()
                    if tweet_text and tweet_text not in seen_tweets:
                        timestamp = tweet.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                        seen_tweets.add(tweet_text)
                        tweets_data.append({"text": tweet_text, "timestamp": timestamp})
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    logging.error("Tweet extraction error: %s", e)
                    continue
            
            # Scroll down and check if new content loads
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        driver.quit()
        return tweets_data
    except Exception as e:
        logging.error("Selenium scraping error: %s", e)
        return []

# -----------------------
# Scraper Handler
# -----------------------
def scrape_site(url):
    if "x.com" in url:
        return scrape_dynamic_site(url, headless=True) # Set this false for debugging
    else:
        logging.error("Unsupported URL format.")
        return []

# -----------------------
# Main Execution
# -----------------------
if __name__ == "__main__":
    twitter_url = "REPLACE_WITH_URL"  # Fill in with the target X/Twitter profile
    scraped_data = scrape_site(twitter_url)
    mailchimp_data = get_mailchimp_data()
    update_google_sheets(mailchimp_data, scraped_data)
    
    # Print scraped tweet data to console
    if scraped_data:
        print("\nRecent Tweet Data:")
        for tweet in scraped_data:
            print(f"- {tweet.get('timestamp', 'N/A')}: {tweet.get('text', '')}")

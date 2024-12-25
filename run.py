import time
import os
import urllib.parse
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import re

# Function to setup Selenium WebDriver using WebDriver Manager
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Use WebDriver Manager to get the correct chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to load keywords from JSON file
def load_keywords_from_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if "keywords" in data and isinstance(data["keywords"], list):
                return [kw.strip() for kw in data["keywords"] if kw.strip()]
            else:
                print("Invalid JSON format. 'keywords' key not found or is not a list.")
                return []
    except FileNotFoundError:
        print(f"JSON file not found: {json_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

# Function to extract and store Telegram channel URLs
def extract_channel_urls(driver, page_source):
    channel_urls = []
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract all the relevant div elements containing Telegram channel info
    elements = soup.find_all("div", class_="gsc-thumbnail-inside")

    for element in elements:
        # Find <a> tag inside each <div class="gsc-thumbnail-inside">
        link_tag = element.find("a", class_="gs-title")
        if link_tag and 'href' in link_tag.attrs:
            channel_url = link_tag.attrs['href']
            channel_urls.append(channel_url)  # Append all URLs, including duplicates

    return channel_urls

# Function to extract unique channel IDs from URLs
def extract_channel_ids(urls):
    channel_ids = set()
    for url in urls:
        match = re.search(r't\.me/s/([^/\?]+)|t\.me/([^/\?]+)', url)
        if match:
            channel_id = match.group(1) or match.group(2)
            channel_ids.add(channel_id)
    return sorted(channel_ids)

# Function to combine and deduplicate IDs from all output files
def combine_all_channel_ids(output_dir):
    all_ids = set()

    # Iterate over all .txt files in the output directory
    for file_name in os.listdir(output_dir):
        if file_name.endswith(".txt"):
            file_path = os.path.join(output_dir, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.readlines()
                    urls = [line.strip() for line in content if line.strip()]
                    ids = extract_channel_ids(urls)
                    all_ids.update(ids)
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")

    # add @ to all IDs
    all_ids_with_at = [f"@{id}" for id in sorted(all_ids)]

    return all_ids_with_at


# Main function for searching and extracting channel URLs
def scrape_telegram_channels(keywords, output_dir, max_tabs, sort_by, save_ids_decision):
    base_url = "https://xtea.io/ts_en_channel.html"

    # Initialize Selenium WebDriver
    driver = setup_driver()

    try:
        for keyword in keywords:
            print(f"Searching for keyword: {keyword}")
            result_data = []  # List for storing results

            for tab in range(max_tabs):
                try:
                    # URL-encode the keyword (replace spaces with %20)
                    encoded_keyword = urllib.parse.quote_plus(keyword)  # Encoding the keyword for URL
                    
                    # Construct search URL with encoded keyword
                    search_url = f"{base_url}#gsc.tab={tab}&gsc.q={encoded_keyword}&gsc.sort={sort_by}"
                    print(f"Fetching URL: {search_url}")

                    # Load page with Selenium
                    driver.get(search_url)

                    # Wait for results to load, increase wait time to ensure content is loaded
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "gsc-results"))
                    )

                    # Wait a little longer to ensure dynamic content has loaded
                    time.sleep(5)

                    # Extract channel URLs from the page source
                    channel_urls = extract_channel_urls(driver, driver.page_source)

                    if channel_urls:
                        print(f"Found {len(channel_urls)} channels on page {tab + 1}")

                        # Add found URLs to result data (including duplicates)
                        result_data.extend(channel_urls)

                    else:
                        print(f"No channels found on page {tab + 1}")

                except Exception as e:
                    print(f"Error processing page {tab + 1}: {str(e)}")
                    continue

                time.sleep(2)  # Delay between requests

            # Save results for the current keyword
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_path = os.path.join(output_dir, f"{keyword}_{timestamp}.txt")
            
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write("\n".join(result_data))
            print(f"Results saved to {output_path}")

            # Check if user decided to save IDs
            if save_ids_decision == 'yes':
                channel_ids = extract_channel_ids(result_data)
                ids_output_path = os.path.join(output_dir, f"{keyword}_ids_{timestamp}.txt")
                with open(ids_output_path, 'w', encoding='utf-8') as file:
                    file.write("\n".join(channel_ids))
                print(f"Channel IDs saved to {ids_output_path}")

    finally:
        driver.quit()

# Main execution
if __name__ == "__main__":
    # Ask user whether to search or just extract IDs
    action = input("Do you want to search for keywords or only extract IDs from the Output folder? (search/extract): ").strip().lower()

    # Set output directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "Output")  # All output files will go here

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if action == "extract":
        # Combine and deduplicate IDs from the Output folder
        combined_ids = combine_all_channel_ids(output_dir)
        final_output_path = os.path.join(output_dir, f"final_channel_ids_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
        with open(final_output_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(combined_ids))
        print(f"All unique channel IDs saved to {final_output_path}")

    elif action == "search":
        # Path to JSON file containing keywords
        json_path = input("Enter the path to the keywords JSON file: ").strip()

        # Load keywords from JSON
        keywords = load_keywords_from_json(json_path)

        if not keywords:
            print("No keywords loaded from JSON. Exiting...")
            exit(1)

        # Ask user if they want to save channel IDs
        save_ids_decision = input("Do you want to extract and save unique channel IDs for each keyword? (yes/no): ").strip().lower()
        if save_ids_decision not in ['yes', 'no']:
            print("Invalid input for saving IDs. Exiting...")
            exit(1)

        # Get max tabs and sort option from user
        try:
            max_tabs = int(input("Enter the number of pages to scrape (e.g., 5): "))
        except ValueError:
            print("Invalid number of pages. Exiting...")
            exit(1)

        sort_by = input("Enter sorting option ('date' or leave empty for relevance): ").strip()

        # Start scraping process
        scrape_telegram_channels(keywords, output_dir, max_tabs, sort_by, save_ids_decision)

        # Ask if the user wants to combine all IDs into a single file
        combine_decision = input("Do you want to combine and deduplicate all channel IDs from the Output folder? (yes/no): ").strip().lower()
        if combine_decision == 'yes':
            combined_ids = combine_all_channel_ids(output_dir)
            final_output_path = os.path.join(output_dir, f"final_channel_ids_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
            with open(final_output_path, 'w', encoding='utf-8') as file:
                file.write("\n".join(combined_ids))
            print(f"All unique channel IDs saved to {final_output_path}")

    else:
        print("Invalid action. Exiting...")

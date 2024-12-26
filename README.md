---
# Telegram Channel Scraper

This Python-based script is designed to scrape Telegram channel URLs based on user-provided keywords, using **Selenium** and **BeautifulSoup**. It allows for the extraction of Telegram channel IDs, the option to save results, and a method for combining and deduplicating extracted channel IDs from previous results.
---

## Features

- **Keyword-based Search**: Input keywords to find relevant Telegram channels.
- **Dynamic Content Handling**: Uses Selenium to interact with dynamic web content.
- **Channel ID Extraction**: Extracts unique Telegram channel IDs from URLs.
- **Customizable Scraping**: Control the number of pages to scrape and the sorting method (e.g., by date).
- **Output Management**: Saves extracted channels and IDs to text files with timestamped filenames.
- **ID Deduplication**: Combine and deduplicate channel IDs from previously saved results.

---

## Requirements

### Libraries Used:

- `time`: Manages delays during the scraping process.
- `os`: Handles file and directory operations.
- `urllib.parse`: URL encoding for search keywords.
- `json`: For loading keywords from a JSON file.
- `selenium`: Web automation for dynamic content loading.
  - `webdriver`
  - `WebDriverWait`
  - `expected_conditions`
  - `By`
- `webdriver_manager`: Automatic management of ChromeDriver.
- `bs4 (BeautifulSoup)`: HTML parsing to extract URLs.
- `datetime`: Adds timestamps to output filenames.
- `re`: Regular expressions to extract Telegram channel IDs.

### Install Required Libraries

Install the dependencies using pip:

```bash
pip install selenium webdriver-manager beautifulsoup4
```

---

## How to Use

1. **Clone or Download the Repository**

   ```bash
   git clone https://github.com/MRAbbasi1/TelegramScraper.git
   cd TelegramScraper
   ```

2. **Set Up the Environment**

   Ensure you have Python 3.7+ installed.
   
  ```bash
  rm -rf .venv
python3 -m venv .venv
pip install -r requirements.txt
  ```

3. **Run the Script**

   The script allows for two main actions: searching for channels based on keywords or extracting and deduplicating channel IDs from existing output.

   - **To activate the virtual environment (if using one)**:

     ```bash
     source .venv/bin/activate
     ```

   - **Run the main script**:
     ```bash
     python run.py
     ```
     or
     ```bash
     python3 run.py
     ```

4. **User Input Prompts**

   The script will prompt you to choose between two actions:

   - **Search for Keywords**: Enter keywords to search Telegram channels.
   - **Extract and Deduplicate IDs**: Combine and deduplicate previously saved channel IDs.

5. **Output Files**  
   The script saves the results in the `Output/` directory, with filenames containing the keyword and timestamp:
   - Example: `Output/music_2024-12-25_12-00-00.txt`
   - Optionally, unique channel IDs can be saved in separate files.

---

## Example Interaction

1. **Search for Channels**:

   ```
   Do you want to search for keywords or only extract IDs from the Output folder? (search/extract): search
   Enter the path to the keywords JSON file: keywords.json
   Do you want to extract and save unique channel IDs for each keyword? (yes/no): yes
   Enter the number of pages to scrape (e.g., 5): 3
   Enter sorting option ('date' or leave empty for relevance): date
   ```

2. **Extract and Deduplicate Channel IDs**:
   ```
   Do you want to search for keywords or only extract IDs from the Output folder? (search/extract): extract
   All unique channel IDs saved to Output/final_channel_ids_2024-12-25_12-00-00.txt
   ```

---

## Code Overview

### Key Functions

1. **`setup_driver()`**:
   Sets up a headless Selenium WebDriver using WebDriver Manager.

2. **`load_keywords_from_json(json_path)`**:
   Loads keywords from a JSON file. Example format:

   ```json
   {
     "keywords": ["music", "technology", "news"]
   }
   ```

3. **`extract_channel_urls(driver, page_source)`**:
   Extracts Telegram channel URLs from the page source using BeautifulSoup.

4. **`extract_channel_ids(urls)`**:
   Extracts unique channel IDs using regular expressions and returns them in sorted order.

5. **`combine_all_channel_ids(output_dir)`**:
   Combines and deduplicates all channel IDs from `.txt` files in the `Output/` directory.

6. **`scrape_telegram_channels(keywords, output_dir, max_tabs, sort_by, save_ids_decision)`**:
   The main function that:
   - Constructs search URLs based on user-provided keywords.
   - Loads pages using Selenium and waits for dynamic content.
   - Extracts URLs and optionally saves channel IDs.

---

## File Structure

```
TelegramScraper/
├── run.py             # Main script for scraping and extracting
├── Output/            # Directory for saving output files
│   ├── music_2024-12-25_12-00-00.txt    # Example result file
│   ├── music_ids_2024-12-25_12-00-00.txt # Example ID file (if enabled)
└── README.md          # Documentation (this file)
```

---

## Notes

- Ensure **Chrome** is installed on your system, as the script uses `chromedriver` for Selenium.
- If you encounter issues with `chromedriver`, update it using `webdriver-manager`.
- The website you scrape from must be accessible. If it changes structure, updates to the script may be required.

---

## Disclaimer

This script is for educational and personal use only. Web scraping may violate the terms of service of some websites. Use responsibly and ensure compliance with all applicable laws.

---

## Contribution

Feel free to contribute by submitting issues or pull requests. Improvements and bug fixes are always welcome!

---

## License

This project is licensed under the **MIT License**.

---

### New Key Functionalities

- **Load Keywords from JSON**: You can now load keywords from a JSON file, making it easier to manage multiple search terms.
- **Dynamic Scraping**: The script dynamically scrapes content using Selenium, which is essential for websites that load content dynamically (e.g., via JavaScript).
- **Channel ID Extraction**: Unique channel IDs are extracted and saved in separate files if needed.
- **ID Deduplication**: A function has been added to combine and deduplicate channel IDs across multiple result files.

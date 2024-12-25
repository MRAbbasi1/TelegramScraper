# Telegram Channel Scraper

This script is a Python-based tool designed to scrape Telegram channel URLs and extract unique channel IDs based on user-provided keywords. The script utilizes Selenium WebDriver and BeautifulSoup for web scraping and provides options for storing results in text files.

---

## Features

- **Keyword-based Search**: Users can input keywords to find relevant Telegram channels.
- **Dynamic Content Loading**: Utilizes Selenium to handle dynamically loaded content on the target website.
- **Channel ID Extraction**: Extracts unique Telegram channel IDs from the scraped URLs.
- **Customizable Options**: Includes settings for the number of pages to scrape and sorting criteria.
- **Output Files**: Saves the results and optional channel IDs to text files in a specified output directory.

---

## Requirements

### Libraries Used:

- `time`: For managing delays in the scraping process.
- `os`: For managing file and directory operations.
- `urllib.parse`: For encoding URLs.
- `selenium`: For web automation and dynamic content loading.
  - `webdriver`
  - `WebDriverWait`
  - `expected_conditions`
  - `By`
- `webdriver_manager`: For automatic ChromeDriver installation.
- `bs4 (BeautifulSoup)`: For parsing HTML content.
- `datetime`: For timestamping output files.
- `re`: For regular expressions to extract Telegram channel IDs.

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

2. **Set Up Environment**
   Ensure you have Python 3.7+ installed.

3. **Run the Script**
   Execute the script with the following command:
   
  ```bash
  source .venv/bin/activate
  ```

   ```bash
   python Extract.py
   ```

4. **Provide User Inputs**
   - Enter keywords separated by commas (e.g., `news, technology`).
   - Enter the number of pages to scrape (e.g., `5`).
   - Optionally specify sorting criteria (`date` for chronological order or leave blank for relevance).

5. **Output Files**
   - The results will be saved in the `Output/` directory with filenames containing the keyword and timestamp.
   - Optionally, extract and save unique channel IDs.

---

## Example

1. **Input Example**:
   ```
   Enter keywords separated by commas: music, movies
   Enter the number of pages to scrape (e.g., 5): 3
   Enter sorting option ('date' or leave empty for relevance): date
   ```

2. **Output Files**:
   - `Output/music_2024-12-25_12-00-00.txt`
   - `Output/music_ids_2024-12-25_12-00-00.txt` (optional, if unique IDs are saved)

---

## Code Overview

### Key Functions:

1. **`setup_driver`**:
   Sets up a Selenium WebDriver using WebDriver Manager. Configured to run in headless mode for faster scraping.

2. **`extract_channel_urls`**:
   Uses BeautifulSoup to parse HTML and extract Telegram channel URLs.

3. **`extract_channel_ids`**:
   Extracts unique Telegram channel IDs from the URLs using regular expressions.

4. **`scrape_telegram_channels`**:
   The main function that:
   - Builds search URLs.
   - Loads pages using Selenium.
   - Extracts and saves channel URLs and IDs.

---

## File Structure

```
TelegramScraper/
├── Extract.py        # Main script
├── Output/           # Output directory for results
└── README.md        # Documentation file (this file)
```

---

## Notes

- Ensure Chrome is installed on your system, as the script uses `chromedriver`.
- If you encounter errors related to `chromedriver`, ensure it is up-to-date by using `webdriver-manager`.
- The target website for scraping must be accessible and functional. Any changes to the website structure might require updates to the script.

---

## Disclaimer

This script is for educational and personal use only. Scraping websites may violate their terms of service. Use responsibly and ensure you comply with all applicable laws and regulations.

---

## Contribution

Feel free to contribute by submitting issues or pull requests to improve the script.

---

## License

This project is licensed under the MIT License.


# TabScraper
Developed by Julius Murphy

A web scraping module for extracting data from HTML tables and websites.

## Features
- Fetch and parse webpages using BeautifulSoup
- Extract data from HTML tables
- Save scraped data to CSV format
- Command-line interface with flexible options
- Comprehensive error handling and logging

## Installation
Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line
```bash
# Basic usage
python scraper.py "https://example.com"

# Specify output file and table index
python scraper.py "https://en.wikipedia.org/wiki/List_of_countries_by_population" -o countries.csv -t 0

# Verbose logging
python scraper.py "https://example.com" -v

# Get help
python scraper.py --help
```

### Quick Test Commands
Add your own URLs here for quick testing. Copy URLs from your browser tabs and paste them below:

```bash
# Example: Wikipedia pages with tables
python scraper.py "https://en.wikipedia.org/wiki/List_of_countries_by_population" -o countries.csv
python scraper.py "https://en.wikipedia.org/wiki/List_of_programming_languages" -o languages.csv

# Example: Data-rich websites
# python scraper.py "YOUR_URL_HERE" -o output.csv

# Example: Specific table index
# python scraper.py "YOUR_URL_HERE" -o data.csv -t 1

# Example: Verbose mode for debugging
# python scraper.py "YOUR_URL_HERE" -v -o debug.csv
```

**Quick Test Files:**
- `quick_test.bat` - Windows batch file for running multiple tests
- `quick_test.py` - Python script for automated testing of multiple URLs

Edit these files to add your own URLs from browser tabs!

### Production Usage
For production deployments, use `production_scraper.py`:

```bash
# Run production scraper with tested URLs
python production_scraper.py
```

This script:
- Uses URLs verified in `quick_test.bat`
- Generates structured JSON results (`production_results.json`)
- Includes comprehensive logging (`production_scraper.log`)
- Handles errors gracefully
- Produces production-ready CSV files

### As a Python Module
```python
from scraper import fetch_page, scrape_table, save_to_csv

# Fetch a webpage
soup = fetch_page("https://example.com")

# Extract table data
table_data = scrape_table(soup, table_index=0)

# Save to CSV
save_to_csv(table_data, "output.csv")
```

## Next Steps
- Add authentication support for protected websites
- Implement data validation and cleaning
- Add support for different output formats (JSON, Excel)
- Create unit tests
- Add configuration file support
- Implement rate limiting and retry logic

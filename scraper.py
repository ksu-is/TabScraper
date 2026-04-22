"""
TabScraper - A web scraping module for extracting data from tables and websites.
Developed by Julius Murphy
"""

from bs4 import BeautifulSoup
import requests
import json
import csv
import logging
from typing import List, Dict, Optional
import sys
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def fetch_page(url: str) -> BeautifulSoup:
    """
    Fetch a webpage and return a BeautifulSoup object for parsing.
    
    Args:
        url (str): The URL of the webpage to fetch
        
    Returns:
        BeautifulSoup: Parsed HTML content
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')


def scrape_table(soup: BeautifulSoup, table_index: int = 0) -> List[Dict]:
    """
    Extract data from an HTML table.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content
        table_index (int): Index of the table to extract (default: 0)
        
    Returns:
        List[Dict]: List of dictionaries representing table rows
        
    Raises:
        ValueError: If no tables are found or table_index is out of range
    """
    tables = soup.find_all('table')
    logger.info(f"Found {len(tables)} tables on the page")
    
    if not tables:
        logger.warning("No tables found on the page")
        return []
    
    if table_index >= len(tables):
        logger.error(f"Table index {table_index} not found. Available tables: 0-{len(tables)-1}")
        raise ValueError(f"Table index {table_index} not found. Available tables: 0-{len(tables)-1}")
    
    table = tables[table_index]
    rows = []
    
    # Get headers
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    if not headers:
        # If no <th> elements, try to get headers from first row
        first_row = table.find('tr')
        if first_row:
            headers = [td.get_text(strip=True) for td in first_row.find_all('td')]
            logger.info(f"Using first row as headers: {headers}")
    
    if not headers:
        logger.warning("No headers found, using generic column names")
        # Count columns in first data row
        first_data_row = table.find_all('tr')[1] if len(table.find_all('tr')) > 1 else table.find('tr')
        if first_data_row:
            col_count = len(first_data_row.find_all('td'))
            headers = [f"Column_{i+1}" for i in range(col_count)]
    
    logger.info(f"Headers: {headers}")
    
    # Get data rows
    data_rows = table.find_all('tr')[1:] if headers else table.find_all('tr')
    for tr in data_rows:
        cells = [td.get_text(strip=True) for td in tr.find_all('td')]
        if cells and len(cells) == len(headers):
            row_dict = dict(zip(headers, cells))
            rows.append(row_dict)
    
    logger.info(f"Extracted {len(rows)} rows of data")
    return rows


def save_to_csv(data: List[Dict], filename: str) -> None:
    """
    Save scraped data to a CSV file.
    
    Args:
        data (List[Dict]): List of dictionaries to save
        filename (str): Output filename
    """
    if not data:
        print("No data to save")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Data saved to {filename}")


def main():
    """Main entry point for the scraper."""
    parser = argparse.ArgumentParser(description='Scrape tables from web pages')
    parser.add_argument('url', nargs='?', help='URL to scrape')
    parser.add_argument('-o', '--output', default='output.csv', help='Output CSV filename')
    parser.add_argument('-t', '--table-index', type=int, default=0, help='Table index to extract (default: 0)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if not args.url:
        print("TabScraper - A web scraping module for extracting data from tables")
        print("Usage: python scraper.py <URL> [options]")
        print("Example: python scraper.py https://example.com -o data.csv -t 1")
        return
    
    try:
        logger.info(f"Fetching page: {args.url}")
        soup = fetch_page(args.url)
        
        logger.info(f"Scraping table at index {args.table_index}")
        table_data = scrape_table(soup, table_index=args.table_index)
        
        if table_data:
            save_to_csv(table_data, args.output)
            print(f"Successfully scraped {len(table_data)} rows to {args.output}")
        else:
            print("No table data found. The page might not contain tables or require authentication.")
            
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
    url = "https://kennesaw.view.usg.edu/d2l/le/content/3825477/Home"
    output_file = "output.csv"
    description = "Scrape tables from the specified URL and save to CSV."
    print(description)
    try:
        soup = fetch_page(url)
        table_data = scrape_table(soup)
        save_to_csv(table_data, output_file)    
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        print(f"Error: {e}")
    



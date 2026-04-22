#!/usr/bin/env python3
"""
TabScraper Production Script
Production-ready script using tested URLs from quick_test.bat
Enhanced with retry logic, rate limiting, and comprehensive logging
"""

import sys
import os
import json
import time
from datetime import datetime
from scraper import fetch_page, scrape_table, save_to_csv
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('production_scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def scrape_with_retry(url_config, max_retries=3, delay_between_retries=2):
    """Scrape a URL with retry logic and rate limiting."""
    for attempt in range(max_retries):
        try:
            logger.info(f"Fetching: {url_config['url']} (attempt {attempt + 1}/{max_retries})")

            # Add rate limiting delay (except for first attempt)
            if attempt > 0:
                logger.info(f"Rate limiting: waiting {delay_between_retries} seconds...")
                time.sleep(delay_between_retries)

            soup = fetch_page(url_config['url'])
            table_data = scrape_table(soup, url_config['table_index'])

            if table_data:
                return table_data, None
            else:
                error_msg = "No table data found"
                if attempt < max_retries - 1:
                    logger.warning(f"{error_msg}, retrying...")
                    continue
                return None, error_msg

        except Exception as e:
            error_msg = str(e)
            if attempt < max_retries - 1:
                logger.warning(f"Error: {error_msg}, retrying...")
                continue
            return None, error_msg

    return None, "Max retries exceeded"

def scrape_production_data():
    """Scrape data from production URLs with retry logic and rate limiting."""

    # Production URLs (tested and verified from quick_test.bat)
    production_urls = [
        {
            "name": "World Population Data",
            "url": "https://en.wikipedia.org/wiki/List_of_countries_by_population",
            "output": "world_population_production.csv",
            "table_index": 0,
            "description": "Country population statistics from Wikipedia"
        },
        {
            "name": "Social Media Engagement",
            "url": "https://smallbiztrends.com/social-media-engagement-strategies/",
            "output": "social_media_engagement_production.csv",
            "table_index": 0,
            "description": "Social media visual impact data"
        },
        # Add more production URLs here:
        {
            "name": "Programming Languages",
            "url": "https://en.wikipedia.org/wiki/List_of_programming_languages",
            "output": "programming_languages_production.csv",
            "table_index": 0,
            "description": "List of programming languages from Wikipedia"
        },
        {
            "name": "World GDP Data",
            "url": "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)",
            "output": "world_gdp_production.csv",
            "table_index": 0,
            "description": "Country GDP statistics from Wikipedia"
        },
        {
            "name": "Tech Company Revenue",
            "url": "https://en.wikipedia.org/wiki/List_of_largest_technology_companies_by_revenue",
            "output": "tech_companies_production.csv",
            "table_index": 0,
            "description": "Largest technology companies by revenue"
        }
    ]

    results = {
        "timestamp": datetime.now().isoformat(),
        "total_urls": len(production_urls),
        "successful_scrapes": 0,
        "failed_scrapes": 0,
        "results": []
    }

    logger.info(f"Starting production scrape of {len(production_urls)} URLs")

    for i, url_config in enumerate(production_urls, 1):
        logger.info(f"[{i}/{len(production_urls)}] Processing: {url_config['name']}")

        # Use retry logic with rate limiting
        table_data, error = scrape_with_retry(url_config)

        if table_data:
            # Save to CSV
            save_to_csv(table_data, url_config['output'])
            logger.info(f"✓ Successfully scraped {len(table_data)} rows to {url_config['output']}")

            results["successful_scrapes"] += 1
            results["results"].append({
                "name": url_config["name"],
                "url": url_config["url"],
                "status": "success",
                "rows_extracted": len(table_data),
                "output_file": url_config["output"],
                "description": url_config["description"]
            })
        else:
            logger.error(f"✗ Failed to scrape {url_config['name']}: {error}")
            results["failed_scrapes"] += 1
            results["results"].append({
                "name": url_config["name"],
                "url": url_config["url"],
                "status": "failed",
                "error": error,
                "description": url_config["description"]
            })

    # Save results summary
    with open('production_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "="*60)
    print("PRODUCTION SCRAPE COMPLETE")
    print("="*60)
    print(f"Total URLs processed: {results['total_urls']}")
    print(f"Successful scrapes: {results['successful_scrapes']}")
    print(f"Failed scrapes: {results['failed_scrapes']}")
    print(f"Results saved to: production_results.json")
    print(f"Logs saved to: production_scraper.log")
    print("\nGenerated files:")
    for result in results["results"]:
        if result["status"] == "success":
            print(f"  ✓ {result['output_file']} ({result['rows_extracted']} rows)")
    print("="*60)

    return results

def main():
    """Main entry point."""
    print("TabScraper Production Script")
    print("Enhanced with retry logic and rate limiting")
    print("============================")
    print("Using tested URLs from quick_test.bat")
    print()

    try:
        results = scrape_production_data()

        # Exit with appropriate code
        if results["failed_scrapes"] > 0:
            logger.warning(f"Completed with {results['failed_scrapes']} failures")
            sys.exit(1)
        else:
            logger.info("All scrapes completed successfully!")
            sys.exit(0)

    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
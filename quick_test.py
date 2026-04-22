#!/usr/bin/env python3
"""
TabScraper Quick Test Script
Add your own URLs here for quick testing
"""

import subprocess
import sys
import os

def run_scraper(url, output_file="output.csv", table_index=0, verbose=False):
    """Run the scraper with given parameters."""
    cmd = [sys.executable, "scraper.py", url, "-o", output_file, "-t", str(table_index)]
    if verbose:
        cmd.append("-v")
    
    print(f"Running: {" ".join(cmd)}")
    result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
    return result.returncode == 0

def main():
    print("TabScraper Quick Test Script")
    print("============================")
    print()
    
    # Example tests - modify with your own URLs
    tests = [
        {
            "url": "https://en.wikipedia.org/wiki/List_of_countries_by_population",
            "output": "countries.csv",
            "description": "Wikipedia countries by population"
        },
        {
            "url": "https://en.wikipedia.org/wiki/List_of_programming_languages", 
            "output": "languages.csv",
            "description": "Wikipedia programming languages"
        },
        # Add your own URLs here:
        # {
        #     "url": "YOUR_URL_HERE",
        #     "output": "my_data.csv",
        #     "description": "My custom data source"
        # },
        # {
        #     "url": "ANOTHER_URL_HERE",
        #     "output": "more_data.csv", 
        #     "table_index": 1,
        #     "description": "Another data source (table index 1)"
        # }
    ]
    
    success_count = 0
    for test in tests:
        print(f"Testing: {test["description"]}")
        success = run_scraper(
            test["url"],
            test.get("output", "output.csv"),
            test.get("table_index", 0),
            test.get("verbose", False)
        )
        if success:
            success_count += 1
            print("✓ Success\n")
        else:
            print("✗ Failed\n")
    
    print(f"Completed {len(tests)} tests, {success_count} successful")

if __name__ == "__main__":
    main()

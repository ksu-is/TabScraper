"""
Tests for TabScraper
"""

import unittest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
from scraper import scrape_table, save_to_csv
import os
import tempfile


class TestTabScraper(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        # Sample HTML with a table
        self.sample_html = """
        <html>
        <body>
        <table>
        <tr><th>Name</th><th>Age</th><th>City</th></tr>
        <tr><td>John</td><td>25</td><td>NYC</td></tr>
        <tr><td>Jane</td><td>30</td><td>LA</td></tr>
        </table>
        </body>
        </html>
        """
        self.soup = BeautifulSoup(self.sample_html, 'html.parser')
    
    def test_scrape_table_with_headers(self):
        """Test scraping a table with proper headers."""
        result = scrape_table(self.soup, table_index=0)
        
        expected = [
            {'Name': 'John', 'Age': '25', 'City': 'NYC'},
            {'Name': 'Jane', 'Age': '30', 'City': 'LA'}
        ]
        
        self.assertEqual(result, expected)
    
    def test_scrape_table_no_tables(self):
        """Test scraping when no tables are present."""
        empty_soup = BeautifulSoup("<html><body></body></html>", 'html.parser')
        result = scrape_table(empty_soup, table_index=0)
        self.assertEqual(result, [])
    
    def test_scrape_table_invalid_index(self):
        """Test scraping with invalid table index."""
        with self.assertRaises(ValueError):
            scrape_table(self.soup, table_index=5)
    
    def test_save_to_csv(self):
        """Test saving data to CSV."""
        test_data = [
            {'Name': 'Alice', 'Score': '95'},
            {'Name': 'Bob', 'Score': '87'}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_filename = f.name
        
        try:
            save_to_csv(test_data, temp_filename)
            self.assertTrue(os.path.exists(temp_filename))
            
            # Check file contents
            with open(temp_filename, 'r') as f:
                content = f.read()
                self.assertIn('Name,Score', content)
                self.assertIn('Alice,95', content)
                self.assertIn('Bob,87', content)
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


if __name__ == '__main__':
    unittest.main()
# TabScraper Refactoring Plan

**Goal:** Convert excessive browser tabs into concise, organized data for easy webpage location and reference.

**TL;DR:** Refactor monolithic `scraper.py` into modular architecture with 5 new modules (config, exporters, utils, main) + comprehensive test suite. Maintains backward compatibility. Total time: ~60 minutes.

---

## Specific Improvements (Priority Order)

### HIGH PRIORITY

**1. Fix Unreachable Code**
- Lines after `main()` call in `if __name__ == "__main__"` block will never execute
- Move hardcoded URL test into a test function or remove it

**2. Add Retry Logic with Exponential Backoff**
- Network requests can fail temporarily
- Implement automatic retry strategy using `requests.adapters.HTTPAdapter` and `urllib3.util.retry.Retry`
- Configuration: 3 retries with 0.5 second backoff factor

**3. Add Timeout Parameter**
- Prevent hanging on slow/unresponsive servers
- Default: 10 seconds
- Make configurable via CLI arguments

**4. Multi-Table Scraping**
- Extract ALL tables at once instead of one at a time
- Implement `scrape_all_tables()` method
- Returns dictionary with table_index as key

### MEDIUM PRIORITY

**5. Add JSON Export**
- Alongside CSV export
- Support for nested data structures
- JSON export preserves metadata

**6. Better Header Detection**
- Handle `<thead>`, `<tbody>` structure
- Fall back strategies for tables without proper headers
- Generate generic headers when needed

**7. Data Cleaning**
- Strip whitespace from cells
- Handle empty cells gracefully
- Optional data type normalization

### LOWER PRIORITY

**8. Add Caching**
- Cache fetched pages to avoid re-downloading during development
- Cache expiration based on time or manual invalidation

**9. Add Logging to File**
- Write logs to `logs/scraper.log` in addition to console
- Optional per configuration

---

## Implementation Steps

### STEP 1: Create `utils.py` (Foundation Layer)
**File:** `utils.py`
**Dependencies:** None
**Time:** 5 minutes

Contains:
- `setup_logging()` - Configure logging with optional file output
- `validate_url()` - Validate URL format
- `sanitize_filename()` - Remove invalid filename characters
- `generate_cache_key()` - Create MD5 hash for caching
- `is_cache_valid()` - Check if cache has expired
- `save_to_cache()` / `load_from_cache()` - Cache operations
- `format_file_size()` - Human-readable file sizes
- `get_file_info()` - File metadata

**Testing:** `from utils import validate_url; validate_url("https://example.com")`

---

### STEP 2: Create `config.py` (Configuration Layer)
**File:** `config.py`
**Dependencies:** utils.py
**Time:** 5 minutes

Contains:
- `ScraperConfig` dataclass with fields:
  - Network: `timeout`, `retry_count`, `verify_ssl`
  - Output: `output_format`, `output_directory`
  - Scraping: `table_index`, `scrape_all_tables`
  - Logging: `log_level`, `log_to_file`, `log_file`
  - Caching: `cache_enabled`, `cache_directory`, `cache_duration`
- Methods: `to_dict()`, `to_json()`, `from_dict()`, `from_json_file()`, `save_to_file()`
- `BatchConfig` dataclass for batch scraping configuration
- Helper functions: `get_default_config()`, `create_default_config_file()`

**Testing:** `from config import ScraperConfig; c = ScraperConfig(); print(c.timeout)`

---

### STEP 3: Create `exporters.py` (Export Layer)
**File:** `exporters.py`
**Dependencies:** utils.py
**Time:** 5 minutes

Contains:
- `BaseExporter` abstract class
- `CSVExporter` - Export to CSV format
- `JSONExporter` - Export to JSON format
- `HTMLExporter` - Export to HTML table format
- `ExcelExporter` - Optional, exports to XLSX (requires openpyxl, pandas)
- `export_factory()` - Factory function for creating appropriate exporter

**Methods for all exporters:**
- `export(data, headers)` - Export data to file
- `_ensure_directory()` - Create nested directories if needed

**Testing:** `from exporters import export_factory; e = export_factory('csv', 'test.csv')`

---

### STEP 4: Refactor `scraper.py` (Core Layer)
**File:** `scraper.py` (refactored)
**Dependencies:** utils.py
**Time:** 15 minutes

**NEW - TabScraper Class:**
```
class TabScraper:
    __init__(url, timeout=10, retry_count=3)
    _validate_url(url) → str
    _create_session_with_retries(retry_count) → requests.Session
    fetch() → bool
    get_table_count() → int
    scrape_table(table_index) → Optional[ScrapedTable]
    scrape_all_tables() → Dict[int, ScrapedTable]
    _extract_headers(table) → List[str]
    close() → None
```

**NEW - ScrapedTable Dataclass:**
```
@dataclass
class ScrapedTable:
    data: List[Dict]
    index: int
    headers: List[str]
    row_count: int
    source_url: str
    
    to_dict() → Dict
```

**KEEP - Backward Compatibility:**
- `fetch_page(url)` - Deprecated, logs warning
- `scrape_table(soup, table_index)` - Deprecated, logs warning
- `save_to_csv(data, filename)` - Deprecated, logs warning
- `main()` - Updated to use new classes

**Testing:** `python scraper.py https://example.com`

---

### STEP 5: Create `main.py` (Entry Point)
**File:** `main.py`
**Dependencies:** scraper.py, config.py, exporters.py, utils.py
**Time:** 10 minutes

Main application class: `TabScraperApp`
```
class TabScraperApp:
    __init__(config: ScraperConfig)
    scrape_single_url(url, output_filename) → bool
    scrape_batch(batch_config: BatchConfig) → bool
    _export_single_table(table_data, output_filename) → bool
    _export_multiple_tables(all_tables, url, output_filename) → bool
```

CLI arguments:
```
python main.py <URL>
python main.py <URL> -o output.csv
python main.py <URL> -t 1 -f json
python main.py <URL> --all-tables -f html
python main.py --batch batch_config.json
python main.py --config config.json <URL>
python main.py --create-config
```

**Testing:** `python main.py --create-config`

---

### STEP 6: Create Enhanced `test_scraper.py` (Testing Layer)
**File:** `test_scraper.py`
**Dependencies:** All modules
**Time:** 20 minutes

Test framework: **unittest** (built-in, no dependencies)

8 test suites with 64 test cases:
1. **TestTabScraperCore** (7 tests) - Initialization, URL normalization
2. **TestTableExtraction** (8 tests) - Single/multiple tables, headers
3. **TestExporters** (10 tests) - CSV, JSON, HTML, factory pattern
4. **TestConfiguration** (7 tests) - Default, custom, save/load configs
5. **TestURLValidation** (10 tests) - Valid/invalid URLs
6. **TestFilenameSanitization** (9 tests) - Clean filenames
7. **TestNetworkMocking** (7 tests) - Fetch, timeout, errors
8. **TestScrapedTableMetadata** (4 tests) - Source URLs, no timestamps
9. **TestBatchConfiguration** (2 tests) - Multiple URLs

**Testing:** `python -m unittest test_scraper.py -v`

---

## File Structure After Refactoring

```
TabScraper/
├── main.py                  # ← NEW: Entry point
├── scraper.py               # ✓ Refactored (was monolithic)
├── config.py                # ← NEW: Configuration
├── exporters.py             # ← NEW: Export formats
├── utils.py                 # ← NEW: Utilities
├── test_scraper.py          # ✓ Enhanced (was basic)
├── requirements.txt         # Update with new dependencies
├── README.md
├── LICENSE
├── tab_scraper_plan.md      # ← NEW: This plan document
├── pytest.ini               # Optional: pytest configuration
│
# Existing output files (unchanged)
├── countries.csv
├── output.csv
├── production_results.json
├── production_scraper_enhanced.py
├── production_scraper.py
├── programming_languages_production.csv
├── quick_test.bat
├── quick_test.py
├── scraper.py (original backup recommended)
├── social_media_engagement_production.csv
├── world_gdp_production.csv
├── world_population_production.csv
│
# Auto-created directories
├── output/                  # Export output
├── logs/                    # Log files
├── cache/                   # Cache files (if enabled)
└── batch_output/            # Batch processing results
```

---

## Implementation Timeline

| Phase | File(s) | Time | Difficulty | Dependencies |
|-------|---------|------|-----------|--------------|
| 1 | utils.py | 5 min | Easy | None |
| 2 | config.py | 5 min | Easy | utils |
| 3 | exporters.py | 5 min | Easy | utils |
| 4 | scraper.py | 15 min | Medium | utils |
| 5 | main.py | 10 min | Medium | all |
| 6 | test_scraper.py | 20 min | Medium | all |
| **TOTAL** | **6 files** | **~60 min** | **Medium** | |

---

## File Dependencies

```
main.py
├── scraper.py (TabScraper class)
├── config.py (ScraperConfig, BatchConfig)
├── exporters.py (Export classes)
└── utils.py (Utilities)

scraper.py
└── utils.py (Logging, retry logic)

config.py
└── utils.py (Optional)

exporters.py
└── utils.py (Directory creation)

test_scraper.py
├── scraper.py
├── config.py
├── exporters.py
└── utils.py
```

**Import Order (when creating files):**
1. utils.py (no dependencies)
2. config.py (uses utils)
3. exporters.py (uses utils)
4. scraper.py (uses utils, calls config)
5. main.py (uses all)
6. test_scraper.py (uses all)

---

## Requirements.txt Updates

**Add these packages:**
```
requests>=2.28.0
beautifulsoup4>=4.11.0
openpyxl>=3.9.0  # Optional: Excel export
pandas>=1.5.0    # Optional: Excel export
```

**Current requirements (already present):**
- requests
- beautifulsoup4
- json (built-in)
- csv (built-in)
- logging (built-in)

---

## Backward Compatibility

**Old code will still work:**
```python
# OLD CODE STILL WORKS:
from scraper import fetch_page, scrape_table, save_to_csv
soup = fetch_page(url)
data = scrape_table(soup)
save_to_csv(data, 'output.csv')
```

**Warnings logged:**
```
WARNING: fetch_page() is deprecated. Use TabScraper class instead.
WARNING: scrape_table() is deprecated. Use TabScraper class instead.
WARNING: save_to_csv() is deprecated. Use exporters module instead.
```

**NEW RECOMMENDED CODE:**
```python
# NEW - RECOMMENDED:
from scraper import TabScraper
from exporters import export_factory

scraper = TabScraper(url)
scraper.fetch()
data = scraper.scrape_table(0)
scraper.close()

exporter = export_factory('csv', 'output.csv')
exporter.export(data.data, data.headers)
```

---

## Test Suite Overview

**Framework:** unittest (built-in Python)
**Total Tests:** 64
**Test Suites:** 9

| Suite | Tests | Coverage |
|-------|-------|----------|
| TabScraper Core | 7 | Initialization, URL handling |
| Table Extraction | 8 | Parsing, headers, errors |
| Export Formats | 10 | CSV, JSON, HTML, factory |
| Configuration | 7 | Default, custom, file I/O |
| URL Validation | 10 | Valid/invalid URLs |
| Filename Sanitization | 9 | Character removal, cleanup |
| Network Mocking | 7 | Fetch, timeout, errors |
| Table Metadata | 4 | Source tracking, no timestamps |
| Batch Configuration | 2 | Multiple URL handling |

**Running Tests:**
```bash
# Run all tests
python -m unittest test_scraper.py -v

# Run specific suite
python -m unittest test_scraper.TestTabScraperCore -v

# Run specific test
python -m unittest test_scraper.TestTabScraperCore.test_initialization -v

# Run with coverage (requires coverage package)
pip install coverage
coverage run -m unittest test_scraper.py
coverage report
coverage html  # generates htmlcov/index.html
```

---

## Key Architecture Decisions

### 1. ScrapedTable Metadata (NO Timestamp)
**Decision:** Do not include timestamp in ScrapedTable
**Reason:** User focus on tab organization by URL, not temporal tracking
**Metadata included:**
- `data` - Actual table rows
- `index` - Which table on page (0-based)
- `headers` - Column names
- `row_count` - Number of data rows
- `source_url` - Where table came from

### 2. Configuration-First Approach
**Decision:** All settings via ScraperConfig dataclass
**Reason:** Single source of truth, easy to persist/reload
**Benefits:**
- CLI arguments override config file
- Batch operations use same config system
- Easy to extend with new settings

### 3. Export Factory Pattern
**Decision:** Use factory function for exporter creation
**Reason:** Easy to add new formats without modifying core
**Example:** Adding XML export = just add `XMLExporter` class

### 4. Backward Compatibility Layer
**Decision:** Keep old function signatures, mark as deprecated
**Reason:** Existing scripts won't break during transition
**Migration path:** Warning messages guide users to new API

### 5. Batch Configuration in JSON
**Decision:** Batch URLs defined in JSON file
**Reason:** Supports "save tab groups as config" workflow
**Example:** Save 5 URLs you're researching → batch config file → run all at once

---

## Scope & Excluded Features

### INCLUDED:
✅ Core scraping functionality  
✅ Multiple export formats (CSV, JSON, HTML)  
✅ URL/filename validation  
✅ Configuration management  
✅ Batch processing  
✅ Error handling with retry logic  
✅ Logging (console + optional file)  
✅ Comprehensive test suite  
✅ Backward compatibility  

### DELIBERATELY EXCLUDED (Future Work):
❌ Async/concurrent scraping (complexity not justified yet)  
❌ Database storage (flat files sufficient for teaching)  
❌ Web UI/dashboard (CLI is sufficient)  
❌ Scheduling/task automation (out of scope for teaching)  
❌ Advanced caching with TTL (simple file cache included)  
❌ API endpoint for scraping (CLI tool focused)  
❌ Machine learning for table detection (manual selection fine)  
❌ Selenium/headless browser (BeautifulSoup sufficient for tables)  

---

## Verification Steps

After implementing each phase, verify:

**Phase 1 - utils.py:**
```bash
python -c "from utils import validate_url; print(validate_url('https://example.com'))"
# Expected: True
```

**Phase 2 - config.py:**
```bash
python -c "from config import ScraperConfig; c = ScraperConfig(); print(c.timeout)"
# Expected: 10
```

**Phase 3 - exporters.py:**
```bash
python -c "from exporters import export_factory; print(export_factory('csv', 'test.csv'))"
# Expected: <exporters.CSVExporter object at ...>
```

**Phase 4 - scraper.py:**
```bash
python scraper.py https://example.com
# Expected: Usage message or successful scrape
```

**Phase 5 - main.py:**
```bash
python main.py --create-config
# Expected: Creates config.json with defaults
```

**Phase 6 - test_scraper.py:**
```bash
python -m unittest test_scraper.py -v
# Expected: 64 tests pass
```

---

## Troubleshooting Common Issues

### Issue: ImportError when running tests
**Solution:** Ensure all module files are in same directory
```bash
ls -la  # Verify: utils.py, config.py, exporters.py, scraper.py, main.py, test_scraper.py
```

### Issue: Network tests failing
**Solution:** Mocked tests should not require internet. Check mock setup in test file.
```python
# Verify @patch decorator is present on test method
@patch('requests.Session.get')
def test_name(self, mock_get):
    mock_get.return_value = Mock()  # Return mock instead of real network
```

### Issue: File permissions error when creating output
**Solution:** Ensure output directory is writable
```bash
mkdir -p output logs cache batch_output
chmod 755 output logs cache batch_output
```

### Issue: "ModuleNotFoundError: No module named 'scraper'"
**Solution:** Run from correct directory or add to Python path
```bash
cd /path/to/TabScraper
python -m unittest test_scraper.py -v
```

---

## Next Steps After Implementation

1. **Run full test suite** to verify all components work together
2. **Test backward compatibility** with existing scripts
3. **Create example batch config** for tab groups
4. **Document API** in README.md with usage examples
5. **Add type hints** throughout codebase for IDE support
6. **Performance test** with large websites (1000+ row tables)
7. **User testing** with actual browser tab workflows

---

## Success Criteria

- [ ] All 64 tests pass
- [ ] Code coverage > 85%
- [ ] Old code still works (backward compatible)
- [ ] Can scrape single URL: `python main.py https://example.com`
- [ ] Can scrape batch: `python main.py --batch batch_config.json`
- [ ] Can export to CSV, JSON, HTML: `python main.py <URL> -f json`
- [ ] Config can be saved/loaded: `python main.py --create-config`
- [ ] No hardcoded values (all via config)
- [ ] Error messages are helpful
- [ ] Code is readable and well-documented

---

## Additional Resources

**BeautifulSoup Documentation:**
- Table parsing: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all

**Requests Library:**
- Retries: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.retry.html

**Python unittest:**
- Mock library: https://docs.python.org/3/library/unittest.mock.html
- Test organization: https://docs.python.org/3/library/unittest.html

---

## Questions for Future Refinement

1. Should scraped data include row numbers/indices?
2. Should we implement search/filtering on exported data?
3. Should batch operations support different configs per URL?
4. Should we track which tabs were "active" vs "archived"?
5. Should we support scheduled re-scraping of URLs?

---

**Last Updated:** April 22, 2026  
**Status:** Planning Phase Complete - Ready for Implementation  
**Author:** GitHub Copilot

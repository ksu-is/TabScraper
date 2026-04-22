@echo off
REM TabScraper Quick Test Commands
REM Add your own URLs here for quick testing

echo TabScraper Quick Test Commands
echo ================================
echo.

REM Example commands - uncomment and modify with your URLs

REM Wikipedia examples
echo Testing Wikipedia population data...
C:/Users/tremu/AppData/Local/Programs/Python/Python314/python.exe scraper.py "https://en.wikipedia.org/wiki/List_of_countries_by_population" -o countries.csv

REM Add your own URLs below:
REM C:/Users/tremu/AppData/Local/Programs/Python/Python314/python.exe scraper.py "YOUR_FIRST_URL_HERE" -o first_data.csv
REM C:/Users/tremu/AppData/Local/Programs/Python/Python314/python.exe scraper.py "YOUR_SECOND_URL_HERE" -o second_data.csv -t 1
REM C:/Users/tremu/AppData/Local/Programs/Python/Python314/python.exe scraper.py "YOUR_THIRD_URL_HERE" -v -o debug_data.csv

REM Change the above commands as needed to test different URLs and options.
REM C:/Users/tremu/AppData/Local/Programs/Python/Python314/python.exe scraper.py "YOUR_URL_HERE" -o output.csv -t 1 -v

REM to this:
C:/Users/tremu/AppData/Local/Programs/Python/Python314/python.exe scraper.py "https://smallbiztrends.com/social-media-engagement-strategies/"

REM Add more test commands as needed
REM to this:
C:/Users/tremu/AppData/Local/Programs/Python/Python314/python.exe scraper.py "https://www.bing.com/search?qs=UT&pq=how+do+i+add+jav&sk=CSYN1&sc=4-16&q=how+do+i+add+javascript+to+my+browser&cvid=0b17259b58674105ba47b532ecb213ab&gs_lcrp=EgRlZGdlKgYIARAAGEAyBggAEEUYOTIGCAEQABhAMgYIAhAAGEAyBggDEAAYQDIHCAQQ6wcYQNIBCTM4NDAxajBqOagCCLACAQ&FORM=ANAB01&PC=LCTS"

echo.
echo Done! Check the generated CSV files.
pause

from selenium import webdriver

# Start browser and collect tab metadata
driver = webdriver.Edge()  # Or webdriver.Edge(), etc.

# Open multiple tabs (example)
driver.get("https://www.python.org")
driver.execute_script("window.open('https://github.com');")
driver.execute_script("window.open('https://app.joinhandshake.com');")

tabs = []
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    tabs.append({
        "title": driver.title,
        "url": driver.current_url,
        "tags": [] # Tags can be added based on content or user input
    })

for tab in tabs:
    print(f"Title: {tab['title']}, URL: {tab['url']}")

driver.quit()
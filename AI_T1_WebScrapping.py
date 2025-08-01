from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import csv
import time

# Step 1: Setup headless Selenium browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open RDS main page
url = "https://www.rds.ca"
driver.get(url)
time.sleep(3)

# Scroll more times to load as many articles as possible
for _ in range(10):  # Increased scrolls for full content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Parse loaded homepage with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Step 2: Extract all article links
base_url = "https://www.rds.ca"
article_links = set()

for a in soup.find_all('a', href=True):
    href = a['href']
    if any(keyword in href for keyword in ['article', 'articles', 'hockey', 'boxe', 'canadiens','videos']):
        if href.startswith('/'):
            article_links.add(base_url + href)
        elif href.startswith('http'):
            article_links.add(href)

# Note: No article limit applied here

# Step 3: Scrape article pages using requests
csv_filename = "rds_all_articles.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Date', 'Description', 'URL'])

    print(f"\n⏳ Scraping {len(article_links)} articles (no limit)...\n")

    for i, link in enumerate(sorted(article_links), start=1):
        try:
            response = requests.get(link, timeout=10)
            article_soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title
            title_tag = article_soup.find(['h1', 'h2'])
            title = title_tag.get_text(strip=True) if title_tag else "No Title"

            # Extract date
            date_tag = article_soup.find('time')
            date = date_tag.get_text(strip=True) if date_tag else "No Date"

            # Extract first paragraph as description
            desc_tag = article_soup.find('p')
            description = desc_tag.get_text(strip=True) if desc_tag else "No Description"

            # Save to CSV
            writer.writerow([title, date, description, link])
            print(f"✅ {i}. {title[:60]}...")

        except Exception as e:
            print(f"❌ Error scraping {link}: {str(e)}")

print(f"\n✅ All article data saved to '{csv_filename}'")

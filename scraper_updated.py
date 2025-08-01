from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

# Sections to scrape
sections = {
    'NHL': 'https://www.rds.ca/hockey/lnh/nouvelles',
    'NBA': 'https://www.rds.ca/basketball/nba/nouvelles',
    'MLB': 'https://www.rds.ca/baseball/mlb/nouvelles',
    'NFL': 'https://www.rds.ca/football/nfl/nouvelles'
}

# Setup Selenium browser (headless)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(), options=chrome_options)
wait = WebDriverWait(driver, 10)

# Output CSV
csv_filename = "rds_full_news.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Section', 'Title', 'Date', 'Description', 'URL'])

    for section_name, section_url in sections.items():
        print(f"\n🔍 Scraping section: {section_name}")
        driver.get(section_url)
        time.sleep(3)

        # Load more articles
        while True:
            try:
                load_more_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Afficher plus de nouvelles')]")))
                driver.execute_script("arguments[0].scrollIntoView(true);", load_more_btn)
                time.sleep(1)
                load_more_btn.click()
                time.sleep(2)
            except:
                print("🚫 No more articles to load.")
                break

        # Parse full page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        article_links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/articles/' in href or '/videos/' in href:
                full_url = "https://www.rds.ca" + href if href.startswith('/') else href
                article_links.add(full_url)

        print(f"📰 Found {len(article_links)} articles in {section_name}.")

        # Visit each article page
        for i, link in enumerate(sorted(article_links), start=1):
            try:
                driver.get(link)
                time.sleep(2)
                article_soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Title
                title_tag = article_soup.find(['h1', 'h2'])
                title = title_tag.get_text(strip=True) if title_tag else "No Title"

                # Date
                date_tag = article_soup.find('time')
                if not date_tag:
                    date_tag = article_soup.find('span', class_='date')
                date = date_tag.get_text(strip=True) if date_tag else "No Date"

                # Description - skip BCE redirect messages
                description = "No Description"
                for p in article_soup.find_all('p'):
                    desc_text = p.get_text(strip=True)
                    if 'redirigé vers le site Web BCE' not in desc_text:
                        description = desc_text
                        break

                # Write row
                writer.writerow([section_name, title, date, description, link])
                print(f"✅ {section_name} [{i}/{len(article_links)}] - {title[:60]}...")

            except Exception as e:
                print(f"❌ Error scraping {link}: {str(e)}")

driver.quit()
print(f"\n✅ All sections scraped and saved to '{csv_filename}'")

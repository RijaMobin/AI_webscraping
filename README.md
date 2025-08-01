About: This project is a Python-based web scraper that automatically collects article data from the sports website RDS.ca.

It works by opening the RDS homepage using Selenium, scrolling down the page to load more content, and then collecting all article links that contain keywords like article, hockey, boxe, or canadiens. After collecting the links, it uses the Requests library to quickly open each article and BeautifulSoup to extract important information such as the title, publication date, a short description (usually the first paragraph), and the full article URL. All of this data is then saved into a structured CSV file named rds_all_articles.csv.

To build this scraper, I used several Python libraries:

Selenium was used to interact with the website and handle dynamic loading by scrolling. BeautifulSoup helped parse the HTML content and extract specific elements. Requests was used for fast and lightweight page loading. CSV module was used to write the extracted data into a CSV file. Time was used to add delays between actions, ensuring that the site content loads properly.

This tool helps automate the process of collecting large amounts of article data from a real news website for use in data analysis or AI projects.

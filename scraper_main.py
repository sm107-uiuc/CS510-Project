from basic_scraper import ScrapeWorker
import pandas as pd

scrape_worker = ScrapeWorker("data/")

scraping_links_f = open('scraping_links_master.txt', 'r')

scraping_links = scraping_links_f.readlines()

#remove duplicates from scraping_links
scraping_links = list(dict.fromkeys(scraping_links))

for link in scraping_links:
    scrape_status, urls = scrape_worker.scrape(link)
from basic_scraper import ScrapeWorker
from topic_modelling_worker import TopicModellingWorker
from topic_modelling import *
import pandas as pd

scrape_worker = ScrapeWorker("data/")


#pandas read csv
pd_medium = pd.read_csv('kaggle_dataset_medium.csv')
print(pd_medium.head())

#get only link column
medium_links = pd_medium['link'].tolist()

#add medium_link to scraping_links.txt
scraping_links_f = open('scraping_links.txt', 'w')
for link in medium_links:
    scraping_links_f.write(link + '\n')
scraping_links_f.close()


scraping_links_f = open('scraping_links.txt', 'r')
scraping_links = scraping_links_f.readlines()



for link in scraping_links:
    scrape_status, urls = scrape_worker.scrape(link)

clean_data_params = {
    'min_df': 0.01,
    'vocab_size': 300,
}

topic_modelling_worker = TopicModellingWorker("./data.json", "data/",pipeline=[
    {"stage": LoadData, "params": {}},
    {"stage": CleanData, "params": clean_data_params},
    {"stage": LdaModel, "params": {"num_topics": 10, "max_iter": 20}},
])
topic_modelling_worker.process()
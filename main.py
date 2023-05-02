from basic_scraper import ScrapeWorker
from topic_modelling_worker import TopicModellingWorker
from topic_modelling import *
scrape_worker = ScrapeWorker("data/")
scrape_status, urls = scrape_worker.scrape("https://www.databricks.com/blog/2021/07/29/an-experimentation-pipeline-for-extracting-topics-from-text-data-using-pyspark.html")

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
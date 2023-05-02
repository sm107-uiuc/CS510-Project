from pyspark.sql import SparkSession
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, CountVectorizer, StopWordsRemover
from pyspark.sql.functions import *
from topic_modelling import *

class TopicModellingWorker():
    
    def __init__(self, in_path, out_path, **kwargs):
        print(kwargs)
        self.kwargs = kwargs
        self.in_path = in_path
        self.out_path = out_path
        self.spark = SparkSession.builder.getOrCreate()
        self.spark.read.option("multiline","true")
        
    def get_defaults(self, class_name):
        if class_name == CleanData:
            return {
                'vocab_size': 1000,
                'min_df': 10,
                'max_df': 20
            }
        elif class_name == LoadData:
            return {
                'in_path': 'data.json',
            }
        elif class_name == LdaModel:
            return {
                'num_topics': 10,
                'max_iter': 10,
            }
        else:
            raise Exception("Class not found")
   
    def process(self):
        pipelines = self.kwargs['pipeline']
        for pipeline in pipelines:
            params = self.get_defaults(pipeline['stage'])
            params = {**params, **pipeline['params'], 'spark': self.spark}
            pipeline_object = pipeline['stage'](params)
            pipeline_object.process()
        
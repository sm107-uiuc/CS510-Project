from .pipeline_object import PipelineObject
from .constants import Constants
from nltk.corpus import stopwords
import json

import pandas as pd
from nltk.collocations import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

class LoadData(PipelineObject):
    def __init__(self,params):
        self.params = params
        
        super().__init__(params)
        
    def process(self):
        super().process()
        constants = Constants.getInstance()
        with open(self.params['in_path']) as json_file:
            data = json.load(json_file)
            data = [json.loads(str(file)) for file in data]
            data = [file for file in data if type(file) == dict]
        text_set = []
        for i in range(len(data)):
            file = data[i]
            try:
                text = (file['title']+file['h1']+ file['all_paragraphs']).lower()    
                text_set.append(text)
            except:
                pass
        text_set = text_set
        data = data
        #text_set = [(file['title']+file['h1']+ file['all_paragraphs']).lower() for file in data]
        print(f"Processing {len(text_set)} files")
        original_text_set = data
        #text_set = text_set[0:2]
        constants.set_data('text_set',text_set)
        constants.set_data('original_text_set',original_text_set)

        
        
        
        
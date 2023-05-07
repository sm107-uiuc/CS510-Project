from .pipeline_object import PipelineObject
from .constants import Constants
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from cso_classifier import CSOClassifier
from nltk.tokenize import word_tokenize
class CleanData(PipelineObject):
    def __init__(self, params):
        super().__init__(params)
        self.params = params
        pass
    def process(self):
        super().process()
        ignored_words = list(stopwords.words('english'))
        # Use CSO Classifier to remove all words that are not in the CSO Ontology
        cc = CSOClassifier(workers=16,modules = "syntactic", enhancement = "first")
        cso_words = []
        text_set = Constants.getInstance().get_data('text_set')
        cso_data = {}
        for i in range(len(text_set)):
            cso_data[str(i)] = text_set[i]
        cso_output = cc.batch_run(cso_data)
        
        
        for _, v in cso_output.items():
            cso_words.extend(v['syntactic'])
            cso_words.extend(v['enhanced'])
        
        ignored_words.extend(self.params['ignored_words'])
        cso_words = [*set(cso_words)]
        cso_words = [word.lower() for word in cso_words]
        count_vec = CountVectorizer(
            ngram_range = (1,1)   #1
            ,stop_words = ignored_words ,
            vocabulary=cso_words
        )
        Constants.getInstance().set_data('count_vec',count_vec)
        
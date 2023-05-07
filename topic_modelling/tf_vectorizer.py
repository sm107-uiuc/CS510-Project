
from .pipeline_object import PipelineObject
from .constants import Constants
import pandas as pd
from nltk.collocations import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import json
from nltk.corpus import stopwords
import pickle

class TfVectorizer(PipelineObject):
    
    def __init__(self, params):
        self.params = params
        super().__init__(params)
    
    def process(self):
        super().process()
        count_vec = Constants.getInstance().get_data('count_vec')
        text_set = Constants.getInstance().get_data('text_set')
        tf_result    = count_vec.fit_transform(text_set)
        tf_result_df = pd.DataFrame(tf_result.toarray()
                                    ,columns=count_vec.get_feature_names_out()) #3
        the_sum_s = tf_result_df.sum(axis=0) #4
        the_sum_df = pd.DataFrame({ #5
            'keyword':the_sum_s.index
            ,'tf_sum':the_sum_s.values
        })
        ignored_words = list(stopwords.words('english'))
        
        the_sum_df = the_sum_df[
            the_sum_df['tf_sum']>2  #6
        ].sort_values(by=['tf_sum'],ascending=False)
        start_index     = int(len(the_sum_df)*0.01) # exclude the top 1%
        my_word_df      = the_sum_df.iloc[start_index:]
        my_word_df      = my_word_df[my_word_df['keyword'].str.len()>2] 
        
        text_set_words  = [word_tokenize(text) for text in text_set] #1
        #text_set_words = []
        # for text in text_tokenized:
        #     text_set_words.append([word for word in text if word in count_vec.vocabulary_])
        bigram_measures = BigramAssocMeasures()
        finder = BigramCollocationFinder.from_documents(text_set_words) #2
        finder.apply_freq_filter(3) #3
        finder.apply_word_filter(lambda w: 
                                len(w) < 3 
                                or len(w) > 15 
                                or w.lower() in ignored_words) #4
        phrase_result = finder.nbest(bigram_measures.pmi, 20000) #5
        colloc_strings = [w1+' '+w2 for w1,w2 in phrase_result] #6
        colloc_strings = [colloc for colloc in colloc_strings if colloc in count_vec.vocabulary_] #7
        my_vocabulary = []
        my_vocabulary.extend(my_word_df['keyword'].tolist()) 
        my_vocabulary.extend(colloc_strings)
        Constants.getInstance().set_data('my_vocabulary',my_vocabulary)
        
        vec   = TfidfVectorizer(
                    analyzer     ='word'
                    ,ngram_range =(1, 2)
                    ,vocabulary  =my_vocabulary)
        
        with open('vocab2.pkl', 'wb') as f:
            pickle.dump(my_vocabulary, f)
        tf_idf = vec.fit_transform(text_set)
        # Save model as pickle file
        with open(self.params['out_path'], 'wb') as f:
            pickle.dump(vec, f)
        
       
        Constants.getInstance().set_data('tf_vec',vec)
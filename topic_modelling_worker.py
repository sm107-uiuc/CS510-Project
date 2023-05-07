
from topic_modelling import *
from sklearn.feature_extraction.text import TfidfVectorizer
class TopicModellingWorker(PipelineObject):
    
    def __init__(self, in_path, out_path, **kwargs):
        print(kwargs)
        self.kwargs = kwargs
        self.in_path = in_path
        self.out_path = out_path
        
    def get_defaults(self, class_name):
        if class_name == CleanData:
            return {
                'vocab_size': 1000,
                'min_df': 10,
                'max_df': 20,
                'ignored_words': []
            }
        elif class_name == LoadData:
            return {
                'in_path': 'data.json',
                'ignored_words': []
            }
        elif class_name == TfVectorizer:
            return {
                'num_topics': 10,
                'max_iter': 10,
                'max_terms_per_topic': 5,
                'out_path': 'model/lda_model'
            }
        else:
            raise Exception("Class not found")
   
    def process(self):
        pipelines = self.kwargs['pipeline']
        for pipeline in pipelines:
            params = self.get_defaults(pipeline['stage'])
            params = {**params, **pipeline['params']}
            pipeline_object = pipeline['stage'](params)
            pipeline_object.process()
    
    def predict(self):
        text_set = Constants.getInstance().get_data('text_set')
        vec = pickle.load(open('tfidf.pkl','rb'))
        tf_idf       = vec.fit_transform(text_set)
        result_tfidf = pd.DataFrame(tf_idf.toarray()
                                    , columns=vec.get_feature_names_out())  
        out = open('output2.txt','a+')
        original_data = Constants.getInstance().get_data('original_text_set')
        for i in range (len(result_tfidf[-1000:])):
            test_tfidf_row = result_tfidf.loc[i]
            keywords_df = pd.DataFrame({
                'keyword':test_tfidf_row.index,
                'tf-idf':test_tfidf_row.values
            })
            index = i
            keywords_df = keywords_df[
                keywords_df['tf-idf'] >0
            ].sort_values(by=['tf-idf'],ascending=False)
            actual_dict = {
                "url" : original_data[index]['url'],
                "keywords" : keywords_df['keyword'][:10].values.tolist(),
                "decription" : original_data[index]["description"],
                "all_paragraphs" : original_data[index]["all_paragraphs"],
                "title" : original_data[index]["title"],
                "h1" : original_data[index]["h1"],
            }
            out.write(json.dumps(actual_dict)+"\n")
        
        
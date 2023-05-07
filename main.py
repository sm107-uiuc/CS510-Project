def get_keywords(keywords_df, vocab):
    keywords = []
    for index, row in keywords_df.iterrows():
        if row['keyword'] in vocab:
            keywords.append(row['keyword'])
            if len(keywords) == 10:
                break
    return keywords

if __name__ == "__main__":
    from basic_scraper import ScrapeWorker
    from topic_modelling_worker import TopicModellingWorker
    from topic_modelling import *
    # scrape_worker = ScrapeWorker("data/")
    # scrape_status, urls = scrape_worker.scrape("https://towardsdatascience.com/keyword-extraction-python-tf-idf-textrank-topicrank-yake-bert-7405d51cd839")

    clean_data_params = {
       'min_df': 0.01,
       'vocab_size': 300,
    }

    print("Starting")
    #train model
    topic_modelling_worker = TopicModellingWorker("./data.json", "data/",pipeline=[
       {"stage": LoadData, "params": {'in_path': 'final_2.json' }},{"stage": CleanData, "params": clean_data_params},{"stage": TfVectorizer, "params": {
           'out_path':'tfidf_3.pkl'
       }}
    ])
    
    # topic_modelling_worker = TopicModellingWorker("./data.json", "data/",pipeline=[
    #    {"stage": LoadData, "params": {'in_path': 'final_2.json' }}
    # ])

    topic_modelling_worker.process()
    print("Done")
    
    #topic_modelling_worker.predict()
    vocab = pickle.load(open('vocab2.pkl','rb'))
    vec = pickle.load(open('tfidf_3.pkl','rb'))
    text_set  = Constants.getInstance().get_data('text_set')
    tf_idf = vec.transform(text_set)
    result_tfidf = pd.DataFrame(tf_idf.toarray()
                                    , columns=vec.get_feature_names_out())
    out = open('final_out4.json','w')
    final = []
    original_data = Constants.getInstance().get_data('original_text_set')
    for i in range (len(result_tfidf)):
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
            "keywords" : get_keywords(keywords_df, vocab),
            "title" : original_data[index]["title"]
        }
        final.append(actual_dict)
    json.dump(final,out)
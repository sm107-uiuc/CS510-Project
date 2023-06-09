"""
    A flask server that loads the model and serves it as an API. Resaves the model and vocab to disk if the model is updated.
"""
# coding: utf-8
from flask import Flask,jsonify, request
from cso_classifier import CSOClassifier
import pickle
from basic_scraper import ScrapeWorker
from flask_apscheduler import APScheduler
import pandas as pd
import traceback
import json
import gensim.downloader as api
from SearchInCDL.get_data_cdl import GetTop50DataFromCDL
from RankingModule.ranking import RankResults
#defaults
"""
A function that periodically saves the model and vocab to disk.
"""
def background_task():
    #print("Saving model")
    with open('./models/tfidf_3.pkl','wb') as f :
        pickle.dump(vec,f)


def get_all_keywords(keywords_df, vocab, hash_tags):
    keywords = {}
    for index, row in keywords_df.iterrows():
        if row['keyword'] in vocab and "_".join(row['keyword'].split(" ")) in hash_tags:
            keywords["_".join(row['keyword'].split(" "))] = row['tf-idf']
    
    return keywords
    
# Schedule the task to run every 30 minutes
scheduler = APScheduler()
app = Flask(__name__)
scheduler.init_app(app)

scheduler.start()
job = scheduler.add_job(id='update_models',func=background_task, trigger='interval',seconds=90)

cc = CSOClassifier(modules = "syntactic", enhancement = "first")
vec = pickle.load(open('./models/tfidf_3.pkl','rb'))
vocab = pickle.load(open('./models/vocab2.pkl','rb'))
scrapper_worker = ScrapeWorker()
PORT=8080
glove = api.load("glove-wiki-gigaword-50")


with open('./final_2.json') as json_file:
    all_data = json.load(json_file)
    all_data = [json.loads(str(file)) for file in all_data]
    all_data = [file for file in all_data if type(file) == dict]

lookup = {}
for data in all_data:
    lookup[data['url']] = data['all_paragraphs']

"""
Function that gets the top 10 keywords from the tf-idf matrix and filters out words that are not in the vocab.
"""
def get_keywords(keywords_df, vocab):
    keywords = []
    for _, row in keywords_df.iterrows():
        if row['keyword'] in vocab:
            keywords.append(row['keyword'])
            if len(keywords) == 10:
                break
    return keywords


"""
    A flask function that loads the model and serves it as an API. Resaves the model and vocab to disk if the model is updated.
"""
@app.route('/', methods=['POST'])
def index():
    try:
        #Step 1: 
        
        data = request.json
    
        # Extract only CS related words from request body
        content = data["content"]
        cso_output = cc.run(content)
        cso_words = []
        cso_words.extend(cso_output['syntactic'])
        cso_words.extend(cso_output['enhanced'])
        cso_words = set(cso_words)
        cso_words = [word.lower() for word in cso_words]
        
        #get results for the content
        vec.fit(cso_words)
        tf_idf = vec.transform([content])
        result_tfidf = pd.DataFrame(tf_idf.toarray(), columns=vec.get_feature_names_out())
        test_tfidf_row = result_tfidf.loc[0]
        keywords_df = pd.DataFrame({
            'keyword':test_tfidf_row.index,
            'tf-idf':test_tfidf_row.values
        })
        keywords_df = keywords_df[
            keywords_df['tf-idf'] >0
        ].sort_values(by=['tf-idf'],ascending=False)
        keywords = get_keywords(keywords_df, [*vec.vocabulary_])
        
        #Step 2:
        getTop50DataFromCDL = GetTop50DataFromCDL(keywords)
        result, hash_tags = getTop50DataFromCDL.doItsThing()
        
        #Step 3:
        """Construct body for similarity function"""
        query_keywords_score = get_keywords_score([content], hash_tags)[0]["keywords"]
        documents = [lookup[url] for url in result]
        
        url_score = get_keywords_score(documents, hash_tags)
        
        options = {
            "query_json": {
                "keywords": query_keywords_score
            },
            "results_json": {}
        }
        
        for i in range(len(url_score)):
            options["results_json"][i] = {}
            options["results_json"][i]["keywords"] = url_score[i]["keywords"]
            ##print(len(url_score[i]["keywords"]))
        
        semantic = {
            'query': content,
            'documents': documents
        }
        ranker = RankResults(options["query_json"], options["results_json"],semantic)
        ranker_res = ranker.rank(glove)

        
        final_scores = []
        for i in range(len(result)):
            temp = {
                'url': result[i],
                'score': ranker_res[i][0]
            }
            final_scores.append(temp)
        final_scores = sorted(final_scores, key=lambda d: d['score'])[::-1]
        return jsonify({
            "status": "success",
            "scores": final_scores
        })
        
        
    except Exception:
        #print("ERROR")
        #print(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": "An error occured"
        })

def get_keywords_score(all_urls, hash_tags):
    try:
        result = []
        for url in all_urls:
            scrapped_data = url
            tf_idf = vec.transform([scrapped_data])
            result_tfidf = pd.DataFrame(tf_idf.toarray(), columns=vec.get_feature_names_out())
            test_tfidf_row = result_tfidf.loc[0]
            keywords_df = pd.DataFrame({
                'keyword':test_tfidf_row.index,
                'tf-idf':test_tfidf_row.values
            })
            #print(result)
            result.append({
                "keywords" : get_all_keywords(keywords_df,vocab, hash_tags),
            })
        return result
    except Exception as e:
        #print(e)
        return []

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=PORT)
    
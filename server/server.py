"""
    A flask server that loads the model and serves it as an API. Resaves the model and vocab to disk if the model is updated.
"""
# coding: utf-8
from flask import Flask,jsonify, request
from semantic_sim import calculate_score
import json
from cso_classifier import CSOClassifier
import pickle
from flask_apscheduler import APScheduler
import pandas as pd
import traceback
import gensim.downloader as api

#defaults
"""
A function that periodically saves the model and vocab to disk.
"""
def background_task():
    print("Saving model")
    with open('./models/tfidf_3.pkl','wb') as f :
        pickle.dump(vec,f)
    
# Schedule the task to run every 30 minutes
scheduler = APScheduler()
app = Flask(__name__)
scheduler.init_app(app)

scheduler.start()
job = scheduler.add_job(id='update_models',func=background_task, trigger='interval',seconds=90)
glove = api.load("glove-wiki-gigaword-50")
cc = CSOClassifier(modules = "syntactic", enhancement = "first")
vec = pickle.load(open('./models/tfidf_3.pkl','rb'))
PORT=8080

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

        return jsonify({
            "status": "success",
            "keywords": keywords
        })
    except Exception:
        print("ERROR")
        print(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": "An error occured"
        })


@app.route('/semantic', methods=['POST'])
def semantic_compute():
    try:
        data = request.json

        query = data["query"]
        urls = data["urls"]
        
        with open('./final_2.json') as json_file:
            all_data = json.load(json_file)
            all_data = [json.loads(str(file)) for file in all_data]
            all_data = [file for file in all_data if type(file) == dict]

        documents = []
        lookup = {}
        for data in all_data:
            lookup[data['url']] = data['all_paragraphs']
        for url in urls:
            documents.append(lookup[url])
        scores = calculate_score(query, documents, glove)

        return jsonify({
            "status": "success",
            "scores": scores
        })
    except Exception:
        print("ERROR")
        print(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": "An error occured"
        })

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=PORT)
    
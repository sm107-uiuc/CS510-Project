from re import sub
from gensim.utils import simple_preprocess

from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.models import WordEmbeddingSimilarityIndex
from gensim.similarities import SparseTermSimilarityMatrix
from gensim.similarities import SoftCosineSimilarity
import numpy as np
from nltk.corpus import stopwords

stopwords = stopwords.words('english')

# From: https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/soft_cosine_tutorial.ipynb
def preprocess(doc):
    # Tokenize, clean up input document string
    doc = sub(r'<img[^<>]+(>|$)', " image_token ", doc)
    doc = sub(r'<[^<>]+(>|$)', " ", doc)
    doc = sub(r'\[img_assist[^]]*?\]', " ", doc)
    doc = sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " url_token ", doc)
    return [token for token in simple_preprocess(doc, min_len=0, max_len=float("inf")) if token not in stopwords]

def calculate_score(query_string, documents, glove):

    # Preprocess the documents, including the query string
    corpus = [preprocess(document) for document in documents]
    query = preprocess(query_string)

    # Load the model: this is a big file, can take a while to download and open
        
    similarity_index = WordEmbeddingSimilarityIndex(glove)

    # Build the term dictionary, TF-idf model
    dictionary = Dictionary(corpus+[query])
    tfidf = TfidfModel(dictionary=dictionary)

    # Create the term similarity matrix.  
    similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary, tfidf)

    query_tf = tfidf[dictionary.doc2bow(query)]
    index = SoftCosineSimilarity(
                tfidf[[dictionary.doc2bow(document) for document in corpus]],
                similarity_matrix)

    doc_similarity_scores = index[query_tf]

    # Output the sorted similarity scores and documents
    sorted_indexes = np.argsort(doc_similarity_scores)[::-1]
    
    scores = []
    for idx in sorted_indexes:
        scores.append(round(doc_similarity_scores[idx],3))
    
    np_scores = np.array(scores)
    converted_scores = np_scores.astype(np.float64)
    return list(converted_scores)
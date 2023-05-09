import json
import requests
import numpy as np
import pandas as pd

class CosineSimilarity:
    def __init__(self, query_json, results_json) -> None:
        ''''
        query_df: {
            "keywords" : {
                "keyword1" : tf-idf score,
                "keyword2" : tf-idf score, //assuming the number of keywords in 711
                ...
            }
        }
        '''

        ''''
        results_df: {
        //assuming that we are taking the top 50 results and 711 keywords each
            "result_one" : {
            "keywords" : {
                "keyword1" : tf-idf score,
                "keyword2" : tf-idf score,
                ...
            }
            },
            "result_two" : {
            "keywords" : {
                "keyword1" : tf-idf score,
                "keyword2" : tf-idf score,
                ...
            }
            },
            ...
        }
        '''
        #convert json to dataframe
        query_df = pd.DataFrame(query_json)
        results_df = pd.DataFrame(results_json)

        self.query_vector = query_df.to_numpy().flatten()
        self.results_matrix = results_df.to_numpy()

        self.results_matrix = [[d[k] for k in d] for d in self.results_matrix[0]]

        self.results_matrix = np.array(self.results_matrix)

        print(self.query_vector, "data type: ", type(self.query_vector))
        print(self.results_matrix, "data type: ", type(self.results_matrix))

        # self.keywords_list = open('keyword_set.txt', 'r').readlines()
        # self.keywords_list = [keyword.strip() for keyword in self.keywords_list]

    def calculate_cosine_similarity(self):
        '''calculate cosine similarity between query and each result

        returns a 1D numpy column vector of size 50
        '''

        den = np.sqrt(np.einsum('ij,ij->i',self.results_matrix,self.results_matrix)*np.einsum('j,j',self.query_vector,self.query_vector))
        out = self.results_matrix.dot(self.query_vector) / den
        #replace nan with 0
        out = np.nan_to_num(out)
        print(out)

        #convert out to 1D numpy column vector
        out = out.reshape(-1,1)

        return out


if __name__ == "__main__":
    query_json = json.load(open('sample_master_query.json','r'))
    results_json = json.load(open('sample_master_result.json','r'))

    cosine_similarity = CosineSimilarity(query_json, results_json)

    print(cosine_similarity.calculate_cosine_similarity())
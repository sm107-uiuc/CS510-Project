import json
import requests
import numpy as np
import pandas as pd

# if __name__ == "__main__":


#     keywords_list = open('keyword_set.txt', 'r').readlines()
#     keywords_list = [keyword.strip() for keyword in keywords_list]

#     print(keywords_list)


#     # data = json.load(open('final_out4.json','r'))
#     # #declare keyword set
#     # keyword_set = set()

#     # for i in range(len(data)):
#     #     entry = data[i]
#     #     entry['keywords'] = ["_".join(keyword.split(" ")) for keyword in entry['keywords']]
#     #     keyword_set.update(entry['keywords'])

#     # print(len(keyword_set))

#     #create a 2d array of size len(data) x len(keyword_set)
#     #each row represents a webpage
#     #each column represents a keyword
#     #each cell represents if the keyword appears in the webpage

#     feature_mat = [[0] * 10 for i in range(5)]
#     # print(list(keyword_set).index("machine_learning"))
#     # print(list(keyword_set).index("ethereum"))


#     # for i in range(len(data)):
#     #     entry = data[i]
#     #     for keyword in entry['keywords']:
#     #         feature_mat[i][list(keyword_set).index(keyword)] = 1

#     #declare feature_mat with 5 rows and 10 columns

#     feature_mat = [[0,0,0,0,0,0,0,0,0,0],
#                      [0,1,1,0,0,0,0,0,0,0],
#                         [0,0,1,0,0,0,0,0,0,0],
#                             [0,1,0,1,0,0,0,0,0,0],
#                                 [0,1,0,0,0,0,0,0,0,0]] 
    



#     #make feature_mat a numpy array
#     feature_mat = np.array(feature_mat)

#     temp_doc_vector = [0,1,0,0,0,0,0,0,0,0]

#     den = np.sqrt(np.einsum('ij,ij->i',feature_mat,feature_mat)*np.einsum('j,j',temp_doc_vector,temp_doc_vector))
#     out = feature_mat.dot(temp_doc_vector) / den
#     #replace nan with 0
#     out = np.nan_to_num(out)
#     print(out)

#     #get max 10 values from out and their indices
#     #sort out
#     #get top 10 values
#     #get their indices
#     #get the corresponding keywords
#     #print the keywords

#     out = np.argsort(out)[-10:]

#     #reverse argsort
#     out = out[::-1]

#     print(out)




#     print([feature_mat[i] for i in out[-10:]])


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

        self.keywords_list = open('keyword_set.txt', 'r').readlines()
        self.keywords_list = [keyword.strip() for keyword in self.keywords_list]

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
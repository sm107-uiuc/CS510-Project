import json
import requests
import numpy as np

if __name__ == "__main__":
    # data = json.load(open('final_out4.json','r'))
    # #declare keyword set
    # keyword_set = set()

    # for i in range(len(data)):
    #     entry = data[i]
    #     entry['keywords'] = ["_".join(keyword.split(" ")) for keyword in entry['keywords']]
    #     keyword_set.update(entry['keywords'])

    # print(len(keyword_set))

    #create a 2d array of size len(data) x len(keyword_set)
    #each row represents a webpage
    #each column represents a keyword
    #each cell represents if the keyword appears in the webpage

    feature_mat = [[0] * 10 for i in range(5)]
    # print(list(keyword_set).index("machine_learning"))
    # print(list(keyword_set).index("ethereum"))


    # for i in range(len(data)):
    #     entry = data[i]
    #     for keyword in entry['keywords']:
    #         feature_mat[i][list(keyword_set).index(keyword)] = 1

    #declare feature_mat with 5 rows and 10 columns

    feature_mat = [[0,0,0,0,0,0,0,0,0,0],
                     [0,1,1,0,0,0,0,0,0,0],
                        [0,0,1,0,0,0,0,0,0,0],
                            [0,1,0,1,0,0,0,0,0,0],
                                [0,1,0,0,0,0,0,0,0,0]] 
    



    #make feature_mat a numpy array
    feature_mat = np.array(feature_mat)

    temp_doc_vector = [0,1,0,0,0,0,0,0,0,0]

    den = np.sqrt(np.einsum('ij,ij->i',feature_mat,feature_mat)*np.einsum('j,j',temp_doc_vector,temp_doc_vector))
    out = feature_mat.dot(temp_doc_vector) / den
    #replace nan with 0
    out = np.nan_to_num(out)
    print(out)

    #get max 10 values from out and their indices
    #sort out
    #get top 10 values
    #get their indices
    #get the corresponding keywords
    #print the keywords

    out = np.argsort(out)[-10:]

    #reverse argsort
    out = out[::-1]

    print(out)




    print([feature_mat[i] for i in out[-10:]])
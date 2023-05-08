import json
import requests

if __name__ == "__main__":
    data = json.load(open('final_out4.json','r'))
    #declare keyword set
    keyword_set = set()

    for i in range(len(data)):
        entry = data[i]
        entry['keywords'] = ["_".join(keyword.split(" ")) for keyword in entry['keywords']]
        keyword_set.update(entry['keywords'])

    print(len(keyword_set))

    #create a 2d array of size len(data) x len(keyword_set)
    #each row represents a webpage
    #each column represents a keyword
    #each cell represents if the keyword appears in the webpage

    feature_mat = [[0] * len(keyword_set) for i in range(len(data))]

    for i in range(len(data)):
        entry = data[i]
        for keyword in entry['keywords']:
            feature_mat[i][list(keyword_set).index(keyword)] = 1
        
    print(feature_mat)
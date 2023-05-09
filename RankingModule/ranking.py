from RankingModule.cosine_similarity import CosineSimilarity

class RankResults:
    def __init__(self, query_json, results_json, result_docs) -> None:
        ''''
        query_json: {
            "keywords" : {
                "keyword1" : tf-idf score,
                "keyword2" : tf-idf score, //assuming the number of keywords in 711
                ...
            }
        }
        '''

        ''''
        results_json: {
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

        '''
        result_docs: { //assuming the length of result_docs is 50
            "result_one" : "content",
            "result_two" : "content",
            ...
        '''

        self.query_json =  query_json
        self.results_json = results_json
        self.result_docs = result_docs

    def rank(self):
        cosine_similarity = CosineSimilarity(self.query_json, self.results_json)
        cosine_similarity = cosine_similarity.calculate_cosine_similarity()

        # semantic similarity = ---> to be implemented

        # combine cosine similarity and semantic similarity
        # rank the results based on the combined similarity score
        # return the top 10 results

        final_score = 0.8 * cosine_similarity + 0.2 * semantic_similarity

        return final_score



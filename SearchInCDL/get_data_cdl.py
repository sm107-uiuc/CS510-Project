from typing import Any
import requests
import json
import sys

sys.path.append("../CS510-Project-1")
from constants import constants



class GetTop50DataFromCDL:
    def __init__(self, keyword_list) -> None:
        self.keyword_list = keyword_list
        self.url = constants.search_url

        self.headers = {
        'authorization': constants.auth_token,
        'authority': 'textdata.org',
        'origin': constants.origin,
        }
        self.params = {
            'query': ",".join(self.keyword_list),
            'community': constants.community_key,
        }

        #make GET request to CDL
        self.response = requests.get(self.url, headers=self.headers, params=self.params)

    
    def get_helper(self, searchId, page):
        current_url = ""

        if searchId is None:
            current_url = self.url + "?query=" + ",".join(self.keyword_list) + "&community="+ self.params['community'] + "&page=" + page
        else:
            current_url = self.url + "?search_id=" + searchId + "&community="+ self.params['community'] + "&page=" + page

        print(current_url)
        return requests.get(current_url, headers=self.headers).json()
    
    def get_recursive(self):

        startPage = 0
        allResponses = []

        firstResponse = self.get_helper(None, str(abs(startPage)))
        searchId = firstResponse["search_id"]
        pageCount = min(int(firstResponse["total_num_results"]/10), 5)

        print(firstResponse)

        allResponses.append(firstResponse)
    
        for page in range(startPage + 1, pageCount):
            response = self.get_helper(searchId, str(abs(page)))
            allResponses.append(response)

        print(allResponses)

        search_results_page = [response["search_results_page"] for response in allResponses]
        return search_results_page

    def doItsThing(self):
        result = self.get_recursive()
        result = [item for sublist in result for item in sublist]
        result_urls = [item["orig_url"] for item in result]

        return result_urls

if __name__ == "__main__":
    keyword_list = ["machine_learning", "software_engineering"]
    print(keyword_list)
    getTop50DataFromCDL = GetTop50DataFromCDL(keyword_list)
    result = getTop50DataFromCDL.doItsThing()




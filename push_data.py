import json
import requests
import curlify
if __name__ == "__main__":
    data = json.load(open('final_out4.json','r'))
    for i in range(len(data[:5])):
        entry = data[i]
        entry['keywords'] = ["_".join(keyword.split(" ")) for keyword in entry['keywords']]
        param = {
            'highlighted_text': '',
            'source_url':entry['url'],
            'community': '64506e22d299148c0dc9c74f',
            'explanation': entry['title'] + " " + " #".join(entry['keywords']),
        }
        #print(param)
        headers = {
            'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYzYzc0YzdmYTc4Njg3YTQ2ZWRhODQ5NCJ9.U9AKCQgBeZMOj9Ww-8F4THsFLNiqMf_d6kXaJFtlYp8',
            'authority': 'textdata.org',
            'origin' : 'chrome-extension://gkcdcpgfcfpoibajaakckbdnapfblgej'
            
        }
        response = requests.post('https://textdata.org/api/submission/', files=param, headers=headers)
        print(curlify.to_curl(response.request))
        if(response.status_code == 200):
            print(f"Completed entry {i}")
        else:
            print(f"Failed entry {i} with message {response.text}")
            
            
# highlighted_text: 
# source_url: https://stackoverflow.com/questions/52438304/capturing-response-body-for-a-http-error-in-python
# explanation: Test 5 #test5
# community: 64506e22d299148c0dc9c74f
        
# curl 'https://textdata.org/api/submission/' \
#   -H 'authority: textdata.org' \
#   -H 'accept: application/json, text/plain, */*' \
#   -H 'accept-language: en-US,en;q=0.9' \
#   -H 'authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYzYzc0YzdmYTc4Njg3YTQ2ZWRhODQ5NCJ9.U9AKCQgBeZMOj9Ww-8F4THsFLNiqMf_d6kXaJFtlYp8' \
#   -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundaryBIIRZ9r1AsAojW2X' \
#   -H 'origin: chrome-extension://gkcdcpgfcfpoibajaakckbdnapfblgej' \
#   -H 'sec-ch-ua: "Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "macOS"' \
#   -H 'sec-fetch-dest: empty' \
#   -H 'sec-fetch-mode: cors' \
#   -H 'sec-fetch-site: cross-site' \
#   -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58' \
#   --data-raw $'------WebKitFormBoundaryBIIRZ9r1AsAojW2X\r\nContent-Disposition: form-data; name="highlighted_text"\r\n\r\n\r\n------WebKitFormBoundaryBIIRZ9r1AsAojW2X\r\nContent-Disposition: form-data; name="source_url"\r\n\r\nhttps://www.w3schools.com/python/ref_requests_post.asp\r\n------WebKitFormBoundaryBIIRZ9r1AsAojW2X\r\nContent-Disposition: form-data; name="explanation"\r\n\r\nTest 3 #test4\r\n------WebKitFormBoundaryBIIRZ9r1AsAojW2X\r\nContent-Disposition: form-data; name="community"\r\n\r\n64506e22d299148c0dc9c74f\r\n------WebKitFormBoundaryBIIRZ9r1AsAojW2X--\r\n' \
#   --compressed
    
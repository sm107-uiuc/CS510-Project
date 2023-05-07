import json
import requests
import re
from bs4 import BeautifulSoup


with open('final_2.json') as json_file:
    data = json.load(json_file)
    data = [json.loads(str(file)) for file in data]
    data = [file for file in data if type(file) == dict and 'towards' in file['url']]

print(f"len(data): {len(data)}")
final = {}
regex = re.compile(r'^[a-z]{2}\sab$')
for item in data:
    page = requests.get(item['url'])   
    soup = BeautifulSoup(page.content, "html.parser")
    banned_words = ['Write', 'Member-only', 'Followers','Follow']
    print(f"{item['url']}")
    keywords = []
    for EachPart in soup.find_all("div", {"class" : regex}):
        if len(EachPart.get_text()) > 0 and not any(substring in EachPart.get_text() for substring in banned_words) and EachPart.get_text().isdigit() == False:
            keywords.append(EachPart.get_text())
    if len(keywords) > 0:
        final[item['url']] = keywords
with open('tags.json', 'w') as fp:
    json.dump(final, fp)
    
print("Completed")
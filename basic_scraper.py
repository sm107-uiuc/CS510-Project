import re
import json
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
from urllib.parse import urljoin



class ScrapeWorker:
    def __init__(self, out_path) -> None:
        self.out_path = out_path

    def scrape(self, url) -> dict:
        """
        Codes:
        -1 - scrape already attempted for url
        1 - success
        2 - invalid file ending for url
        3 - timeout
        4 - invalid status code
        5 - unable to parse
        6 - url name is too long to store
        """

        url, url_path = self.format_url_to_path(url)



        if len(url_path) > 255:
            return {"code": -6, "message": "url is too long"}, []
        if os.path.exists(self.out_path + url_path + "data.json"):
            return {"code": -1, "message": "file already exists"}, []
        else:
            # handle case where we fail before we write anything
            try:
                os.makedirs(self.out_path + url_path)
            except:
                pass

        data = {"url": url, "time": time.time(), "path": url_path}


        if url.split(".")[-1] in ["bz2", "zip", "csv", "sqlite3", "exe", "mp3", "mp4", "pdf", "gz", "png", "jpg"]:
            data["scrape_status"] = {"code": 2, "message": "url ending is invalid"}
            json.dump(data, open(self.out_path + url_path + "data.json", "w"))
            return data["scrape_status"], []

        try:
            resp = requests.get(url, timeout=5, headers={"User_Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
        except:
            data["scrape_status"] = {"code": 3, "message": "webpage timeout"}
            json.dump(data, open(self.out_path + url_path + "data.json", "w"))
            return data["scrape_status"], []
        
        print("\t Page acquired")
        
        if resp.status_code != 200:
            data["scrape_status"] = {"code": 4, "message": "invalid response status code", "resp_status_code": resp.status_code}
            json.dump(data, open(self.out_path + url_path + "data.json", "w"))
            return data["scrape_status"], []
        
        if resp.status_code == 200:
            try:
                len_text = len(resp.text)
                print("\t", len_text)
                if len_text > 9731000: #50000000:
                    raise Exception("too long!")
                metadata, outgoing_paragraph_urls, all_paragraphs, all_outgoing_urls = self.parse_html(resp.text, url)

            except Exception as e:
                print(e)
                data["scrape_status"] = {"code": 5, "message": "unable to parse webpage"}
                json.dump(data, open(self.out_path + url_path + "data.json", "w"))
                return data["scrape_status"], []


        data["webpage"] = {"metadata": metadata,
                           "outgoing_paragraph_urls": outgoing_paragraph_urls, 
                           "all_paragraphs": all_paragraphs, 
                           "all_outgoing_urls": all_outgoing_urls}
        data["scrape_status"] = {"code": "1"}
        json.dump(data, open(self.out_path + url_path + "data.json", "w"))
        all_outgoing = [x["url"] for x in all_outgoing_urls]
        return data["scrape_status"], all_outgoing

    def parse_html(self, html, page_url) -> tuple:

        html_no_script = re.sub(r"<script.*?</script>", "", str(html))
        metadata = {}
        all_paragraphs_text = []
        outgoing_paragraph_urls = []
        all_outgoing_urls = []


        if html_no_script:
            soup = BeautifulSoup(html_no_script, 'html.parser')
            title = ""
            h1 = ""
            description = ""

            # for title
            if soup.title and soup.title.text:
                title = soup.title.text
            if soup.h1 and soup.h1.text:
                h1 = soup.h1.text

            # for description
            meta = soup.find("meta", attrs={"name": "description"})
            if meta and meta.has_attr("content"):
                description = meta["content"]
            if not description:
                first_h1 = soup.find("h1")
                if first_h1:
                    first_p = first_h1.find_next("p")
                    if first_p and first_p.string:
                        description = first_p.text
            if not description:
                first_p = soup.find("p")
                if first_p and first_p.string:
                    description = first_p.string
            

            metadata = {
                "title": self.clean_text(title),
                "h1": self.clean_text(h1),
                "description": self.clean_text(description)
            }


            all_paragraphs = soup.find_all("p")
            all_urls = soup.find_all("a")

            for outgoing_url in all_urls:
                hyperlink_url = outgoing_url.get("href", "")
                
                isValidURL, hyperlink_url = self.test_fix_relative_url(hyperlink_url, page_url)
                
                hyperlink_text = self.clean_text(outgoing_url.text)
                if isValidURL:
                    all_outgoing_urls.append({
                        "url": hyperlink_url,
                        "anchor_text": hyperlink_text
                    })

            j = 0
            for paragraph in all_paragraphs:
                paragraph_text = self.clean_text(paragraph.text)
                if self.measure_string_quality(paragraph_text):
                    all_paragraphs_text.append(paragraph.text)
                    all_hyperlinks = paragraph.find_all("a")
                    for h in all_hyperlinks:
                        hyperlink_text = self.clean_text(h.text)
                        hyperlink_url = h.get("href", "")

                        isValidURL, hyperlink_url = self.test_fix_relative_url(hyperlink_url, page_url)
                        if isValidURL:
                            outgoing_paragraph_urls.append({
                                "url": hyperlink_url,
                                "anchor_text": hyperlink_text,
                                "paragraph_index": j
                            })
                    j += 1

        return metadata, outgoing_paragraph_urls, all_paragraphs_text, all_outgoing_urls
        


    def clean_text(self, text) -> str:
        if not text or len(text) == 0:
            return ""
        text = text.replace("\\r\\n", " ")
        text = text.replace("\\n", " ")
        text = text.replace("\\t", " ")
        text = " ".join(text.split())
        return text

    def test_fix_relative_url(self, url, base_url):
        if len(url) == 0:
            return False, url
        elif url[0] == "#": 
            return False, url
        elif url[0] == "/":
            url = urljoin(base_url, url)
            return True, url
        if url[:4] != "http":
            return False, url
        else:
            return True, url
        

    def measure_string_quality(self, string, type="paragraph") -> bool:
        if not string:
            return False
        num_words = len(string.split(" "))
        num_sentences = len(string.split(". "))

        letter_ratio = len(re.sub("[^a-z ]", "", string.lower())) / max(len(re.sub("[a-z ]", "", string.lower())), 1)
        avg_word_length = sum([len(x) for x in string.split(" ")]) / num_words

        if type == "paragraph":
            if avg_word_length < 10 and letter_ratio > 5 and num_words > 5 and num_sentences >= 1:
                return True
            else:
                return False
        if type == "title":
            if avg_word_length < 10 and letter_ratio > 10 and num_words > 3 and num_words < 50 :
                return True
            else:
                return False

    def remove_links(self, anchor):
        if not anchor:
            return

        replacements = [
            r'\S+\.\w{2,3}\/\S+',
            r'\S+\.[a-z]{2,3}\s'
        ]

        return re.sub("|".join(replacements), " ", anchor)

    def remove_long_words(self, word):
        if not word: return
        return re.sub(r'\w{20,}[^\.]', '', word)

    def measure_anchor_quality(self, anchor):
        if not anchor:
            return False
        return len(anchor) >= 5

    def format_url_to_path(self, url) -> str:

        # for webarchive, get actual url
        if "://web.archive.org/web/" in url:
            url = url.split("://web.archive.org/web/")[1]
            url = "http" + "".join(url.split("http")[1:])


        parsed_url = urlparse(url)

      
        # remove www if present 
        new_netloc = parsed_url.netloc
        if new_netloc[:4] == "www.":
            new_netloc = new_netloc[4:]

        full_path = new_netloc + parsed_url.path


        # for youtube only, add the query in the path
        if "youtube" in parsed_url.netloc or "youtu" in parsed_url.netloc:
            full_path = full_path + parsed_url.query
        # otherwise, remove query from url
        else:
            if "?" in url:
                url = url.split("?")[0]

        # always remove fragment from query
        if "#" in url:
            url = url.split("#")[0]
        if len(full_path) == 0:
            return url, ""
        if full_path[-1] != "/":
            full_path += "/"

        return url, full_path
import pandas as pd

#pandas read csv
#for each file in folder links_dataset
#add link to scraping_links.txt


import os
import glob

path = "/Users/sivaashaanth/Downloads/CS510-Project-1/links_datasets"
csv_files = glob.glob(os.path.join(path, "*.csv"))

scraping_links_f = open('scraping_links.txt', 'w')

for pd_medium_path in csv_files:
    pd_medium = pd.read_csv(pd_medium_path)
    
    print(pd_medium.columns)
    if 'url' in pd_medium.columns:
        medium_links = pd_medium['url'].tolist()
    elif 'links' in pd_medium.columns:
        medium_links = pd_medium['links'].tolist()
    elif 'link' in pd_medium.columns:
        medium_links = pd_medium['link'].tolist()
    elif 'Link' in pd_medium.columns:
        medium_links = pd_medium['Link'].tolist()
    elif 'Links' in pd_medium.columns:
        medium_links = pd_medium['Links'].tolist()

    #add medium_link to scraping_links.txt
    for link in medium_links:
        scraping_links_f.write(link + '\n')
    
    print("finished writing to scraping_links.txt")
scraping_links_f.close()

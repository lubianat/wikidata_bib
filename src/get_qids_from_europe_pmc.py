import urllib.parse
import requests
from helper import pmid_to_wikidata_qid, add_to_file, remove_read_qids
import re

category = "Cell types"
endpoint = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

params = {"query": '"catalog of cell types"', "format": "json", "pageSize": "1000"}
response = requests.get(
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search", params
)

data = response.json()
pmids = []


for article in data["resultList"]["result"]:
    try:
        pmid = article["pmid"]
        print(pmid)
        pmids.append(pmid)
    except:
        continue

print(pmids)
main_list = pmid_to_wikidata_qid(pmids)

# Ignore articles in toread.md
with open("toread.md", "r") as f:
    articles_file = f.read()

logged_articles = re.findall("Q[0-9]*", articles_file)
main_list = list(set(main_list) - set(logged_articles))

main_list = remove_read_qids(main_list)
if category != None:
    print("====== Appending QIDs to file toread.md ====== ")
    add_to_file(main_list, category)

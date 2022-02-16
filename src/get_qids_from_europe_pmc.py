import urllib.parse
import requests
from helper import pmid_to_wikidata_qid

endpoint = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

params = {"query": '"catalog of cell types"', "format": "json", "pageSize": "1000"}
response = requests.get(
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search", params
)

data = response.json()
print(data)
pmids = []
for article in data["resultList"]["result"]:
    print("-------")
    print(article)
    try:
        pmid = article["pmid"]
        print(pmid)
        pmids.append(pmid)
    except:
        continue

qids = pmid_to_wikidata_qid(pmids)

print(qids)

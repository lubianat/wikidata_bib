import requests
import sys
from glob import glob

# Example queries:
# Single-cell transcriptomics articles in either nature or science: https://w.wiki/3LhF
# Run: 
# $ python3 wadd.py https://w.wiki/3LhF all  

url = sys.argv[1]
only_new = sys.argv[2]


session = requests.Session()  # so connections are recycled
resp = session.head(url, allow_redirects=True)
url_sparql = resp.url.replace("https://query.wikidata.org/#", "https://query.wikidata.org/sparql?query=")

if "work" not in url_sparql:
    raise ValueError("SPARQL query needs to select a variable called ?work")

r = requests.get(url_sparql, params = {'format':'json'})

import pandas as pd

df = pd.json_normalize(r.json()["results"]["bindings"])

df["qid"] = [url.split("/")[4] for url in df["work.value"]]

if only_new == "all":
    for i in df["qid"]:
        print(i)
else:
    txtfiles = []
    for file_name in glob("./notes/*.md"):
        txtfiles.append(file_name)

    array_of_filenames = [name.replace(".md", "") for name in txtfiles]

    array_of_qids = []
    for item in array_of_filenames:
        if "Q" in item:
            array_of_qids.append(item)
    array_of_qids = [md.replace("./notes/Q", "Q") for md in array_of_qids]
    main_list = list(set(df["qid"]) - set(array_of_qids))
    for i in main_list:
        print(i)

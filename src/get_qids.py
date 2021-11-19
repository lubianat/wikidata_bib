import pandas as pd
import requests
from helper import wikidata2df
import argparse
from glob import glob

parser = argparse.ArgumentParser(
    description="Get a list of QIDs from Wikidata and Europe PMC"
)
parser.add_argument(
    "query", metavar="query", help="the value to query", type=str, nargs="+"
)
parser.add_argument(
    "--filter", help="filter out QIDs that were already read", action="store_true"
)
parser.add_argument(
    "--number",
    "-n",
    help="the number of articles to get (default = 25)",
    type=int,
    default=25,
)

args = parser.parse_args()

to_filter = args.filter
print("Filter: " + str(to_filter))
search = args.query[0]
print("Query: " + search)
number_of_results = str(args.number)
print("Number of articles: " + number_of_results)

result = requests.get(
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="
    + search
    + "&pageSize="
    + number_of_results
    + "&format=json"
)

df = pd.json_normalize(result.json()["resultList"]["result"])
df = df.dropna(axis=0, subset=["doi"])
formatted_dois = '{ "' + '" "'.join(df["doi"]) + '"}'
query = f"""SELECT ?id ?item  ?itemLabel
WHERE {{
    {{
    SELECT ?item ?id WHERE {{
        VALUES ?unformatted_id {formatted_dois}
        BIND(UCASE(?unformatted_id) AS ?id)
        ?item wdt:P356 ?id.
    }}
    }}
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}}}
"""

query_result = wikidata2df(query)

# Getting already read article
txtfiles = []
for file_name in glob("./notes/*.md"):
    txtfiles.append(file_name)

array_of_filenames = [name.replace(".md", "") for name in txtfiles]


array_of_qids = []
for item in array_of_filenames:
    if "Q" in item:
        array_of_qids.append(item)
array_of_qids = [md.replace("./notes/Q", "Q") for md in array_of_qids]

print("====== DOIs not found on Wikidata ========")

for doi in df["doi"]:
    if doi.upper() not in query_result["id"].values:
        print(doi)


print("====== QIDs found ========")

for i, row in query_result.iterrows():
    if to_filter:
        if row["item"] in array_of_qids:
            pass
        else:
            print(row["item"])

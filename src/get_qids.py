import pandas as pd
import requests
import sys
from wikidata2df import wikidata2df

search = sys.argv[1]
number_of_results = sys.argv[2]
result = requests.get(
    "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query="
    + search
    + "&pageSize="
    + number_of_results
    + "&format=json"
)
df = pd.json_normalize(result.json()["resultList"]["result"])

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
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
}}"""

query_result = wikidata2df(query)

print("====== DOIs not found ========")

for doi in df["doi"]:
    if doi.upper() not in query_result["id"].values:
        print(doi)


print("====== QIDs ========")

for i, row in query_result.iterrows():
    print(row["item"])

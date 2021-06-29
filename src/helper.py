import requests
import pandas as pd
from collections import defaultdict
from itertools import product, chain

# Based on https://github.com/jvfe/wikidata2df/blob/master/wikidata2df/wikidata2df.py
# Workaround due to user agent problems leading to 403
def wikidata2df(query):

    endpoint_url = "https://query.wikidata.org/sparql"

    response = requests.get(
        endpoint_url,
        params={"query": query, "format": "json"},
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        },
    )
    print(response)
    query_result = response.json()
    parsed_results = defaultdict(list)
    data = query_result["results"]["bindings"]
    keys = frozenset(chain.from_iterable(data))
    for json_key, item in product(data, keys):
        try:
            parsed_results[item].append(json_key[item]["value"])
        except:
            parsed_results[item].append(None)

    results_df = pd.DataFrame.from_dict(parsed_results).replace(
        {"http://www.wikidata.org/entity/": ""}, regex=True
    )

    return results_df

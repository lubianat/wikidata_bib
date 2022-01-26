import requests
import pandas as pd
from collections import defaultdict
from itertools import product, chain
import requests
import os
import warnings
from bs4 import BeautifulSoup
import pandas as pd

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


def add_to_file(qids, category, filepath="toread.md"):
    """Adds a list of qids to a file

    Inserts each qids as a newline after the category is found.

    Attributes:
        filepath (str): The path to the file to be modified
        qids (list): A list of qids to be added to the file as newlines
        category (str): A word matching a header in the file, below it the
        newlines shall be added
    """
    with open(filepath, "r") as f:
        lines = f.read().split("\n")

    for i, line in enumerate(lines):
        if category in line:
            print('- Category "{}" found in line {}'.format(category, i + 1))
            start_line = i + 1

    with open(filepath, "r") as f:
        to_read = f.readlines()

    newlines = []
    for i in qids:
        newlines.append(i + "\n")

    print(f"- {str(len(newlines))} QIDs inserted")

    to_read = to_read[:start_line] + newlines + to_read[start_line:]
    with open(filepath, "w") as f2:
        f2.writelines(to_read)


def get_doi_df(wikidata_id):
    query = (
        """
    SELECT ?item ?doi ?itemLabel
    WHERE
    {
    VALUES ?item {wd:"""
        + wikidata_id
        + """} .
    ?item wdt:P356 ?doi.  
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """
    )
    df = wikidata2df(query)
    return df


def download_paper(doi, source, path="~/Downloads/", prepop=False):
    """
    Given a DOI, downloads an article to a folder.

    Args:
        doi: A doi suffix (ex="10.7287/PEERJ.PREPRINTS.3100V1").
        source: The source to get the pdf from. One of ["sci-hub", "unpaywall"]
        path: The folder where the pdf will be saved.
    """

    if source == "sci-hub":
        # Warning: Only use SciHub to get articles that you have the rights for!
        base_url = "https://sci-hub.do/" + doi
        response = requests.get(base_url, verify=False)
        soup = BeautifulSoup(response.content, "html.parser")
        iframe = soup.find("iframe")
        if iframe:
            url = iframe.get("src")
        filename = url.split("/")[-1].split("#")[0]
        filepath = path + filename
        print("====== Dowloading article from Sci-Hub ======")

    elif source == "unpaywall":
        base_url = (
            f"https://api.unpaywall.org/v2/{doi}?email=tiago.lubiana.alves@usp.br"
        )
        response = requests.get(base_url)
        result = response.json()
        pdf_url = result["best_oa_location"]["url_for_pdf"]
        if pdf_url is None:

            warnings.warn(
                "====== Best OA pdf not found. Searching for first OA ====== "
            )
            pdf_url = result["first_oa_location"]["url_for_pdf"]
        filename = doi.replace("/", "_")
        filepath = path + filename + ".pdf"
        print("====== Dowloading article from Unpaywall ======")

    os.system(f"wget -O {filepath} -q --show-progress {pdf_url} --no-clobber ")

    if prepop:
        if os.path.exists(filepath):
            return {"saved": True}
        else:
            return {"saved": False}
    else:
        print("====== Opening PDF ======")
        os.system(f"xdg-open {filepath} &")

    return 0

"""
Helper private functions for Wikidata Bib

"""
import os
import warnings
from collections import defaultdict
from glob import glob
from itertools import chain, product
from pathlib import Path

import pandas as pd
import requests
import yaml
from bs4 import BeautifulSoup

HERE = Path(__file__).parent.resolve()


def get_qids_in_reading_list():
    """
    Returns a list of QIDs from the "to read" list.
    """

    toread = get_toread_dict()

    logged_articles = []
    for cat in toread["articles"]:
        logged_articles.extend(toread["articles"][cat])
    return logged_articles


def get_config_dict():
    """
    Gets the dict of the config YAML file.
    """
    config_path = HERE.parent.joinpath("data/config.yaml").resolve()
    with open(config_path, "r") as c:
        shortcuts = yaml.load(c.read(), Loader=yaml.FullLoader)
    return shortcuts


def get_toread_dict():
    """
    Gets the dict of the toread YAML file.
    """
    toread_path = HERE.parent.joinpath("data/toread.yaml").resolve()
    toread_string = toread_path.read_text(encoding="UTF-8")
    toread = yaml.safe_load(toread_string)
    return toread


def get_qids_from_europe_pmc(query):
    """
    Pulls a list of Wikidata QIDs ordered by date (newest first) from Europe PMC.
    """
    params = {"query": query, "format": "json", "pageSize": "100"}
    response = requests.get("https://www.ebi.ac.uk/europepmc/webservices/rest/search", params)

    data = response.json()
    pmids = []

    for article in data["resultList"]["result"]:
        try:
            pmid = article["pmid"]
            pmids.append(pmid)
        except:
            continue

    main_list = pmid_to_wikidata_qid(pmids)
    return main_list


def get_tweet_df(wikidata_id):
    """
    Retrieves a pandas DataFrame from Wikidata with twitter
    information for the authors of an article.
    """
    query = (
        """
    SELECT ?item ?itemLabel ?date ?doi ?url ?arxiv_id ?author ?twitter_id
    WHERE
    {
    VALUES ?item {wd:"""
        + wikidata_id
        + """}
    ?item wdt:P356 ?doi .
    ?item wdt:P50 ?author . 
    OPTIONAL { ?author wdt:P2002 ?twitter_id . } 

    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """
    )

    tweet_dataframe = wikidata2df(query)
    return tweet_dataframe


def get_title_df(wikidata_id):
    """
    Returns a pandas DataFrame with the title and other
    basic information for an article.
    """
    query = (
        """
    SELECT ?item ?itemLabel ?date ?doi ?url ?arxiv_id
    WHERE
    {
    VALUES ?item {wd:"""
        + wikidata_id
        + """}
    OPTIONAL {?item wdt:P577 ?date}.
    OPTIONAL {?item wdt:P356 ?doi} .
    OPTIONAL {?item wdt:P953 ?url}
    OPTIONAL {?item wdt:P818 ?arxiv_id}
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """
    )

    basic_info_dataframe = wikidata2df(query)

    return basic_info_dataframe


def remove_read_qids(list_of_qids):
    """
    Removes ther read QIDs from a list of qids.
    """
    read_path = HERE.parent.joinpath("data/read.csv").resolve()
    articles = pd.read_csv(read_path)
    old_articles = list(articles["wikidata_id"])
    diff = list(set(list_of_qids) - set(old_articles))
    main_list = [o for o in list_of_qids if o in diff]

    return main_list


def pmid_to_wikidata_qid(list_of_pmids):
    """
    Obtains a list of QIDs from Wikidata given a list of Pubmed IDs.
    The list is sorted by publication date, newest first.

    Args:
        list_of_pmids (List[str]): A list of Pubmed IDs.

    Returns:
        (List[str]): A list of QIDs.

    """

    values = ""
    for pmid in list_of_pmids:
        values = values + f' "{pmid}"'

    query = f"""
    SELECT 
      ?qid ?publication_date
    WHERE 
    {{
      VALUES ?pmid {{ {values} }} .
      ?qid wdt:P698 ?pmid .
      ?qid wdt:P577 ?publication_date .
    }}
    ORDER BY
      DESC (?publication_date)
    """
    print(query)
    qid_dataframe = wikidata2df(query)
    qids = qid_dataframe["qid"].values
    return qids


# Based on https://github.com/jvfe/wikidata2df/blob/master/wikidata2df/wikidata2df.py
# Workaround due to user agent problems leading to 403
def wikidata2df(query):
    """Queries the Wikidata SPARQL endpoint.

    Args:
        query (str): A SPARQL query formatted for the Wikidata query service.

    Returns:
        (pd.DataFrame): A table with the Wikidata results.

    """

    endpoint_url = "https://query.wikidata.org/sparql"

    response = requests.get(
        endpoint_url,
        params={"query": query, "format": "json"},
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)"
                "AppleWebKit/537.36 (KHTML, like Gecko)"
                "Chrome/50.0.2661.102 Safari/537.36"
            )
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


def remove_read_and_reading_list(main_list):
    logged_articles = get_qids_in_reading_list()

    diff = list(set(main_list) - set(logged_articles))
    main_list = [o for o in main_list if o in diff]

    main_list = remove_read_qids(main_list)
    return main_list


def add_to_file(qids, category):
    """Adds a list of qids to a file

    Inserts qids into a category in the toread.yaml file.

    Args:
        qids (list): A list of qids to be added to the file as newlines
        category (str): The key of the list to append the ids.
    """

    toread_path = HERE.parent.joinpath("data/toread.yaml").resolve()
    toread_string = toread_path.read_text(encoding="UTF-8")
    toread = yaml.safe_load(toread_string)
    old_articles = toread["articles"][category]
    qids.extend(old_articles)
    toread["articles"][category] = qids

    toread_path.write_text(yaml.dump(toread), encoding="UTF-8")


def get_doi_df(wikidata_id):
    """
    Returns a DOI-containing dataframe for a Wikidata ID.
    """
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
    doi_df = wikidata2df(query)
    return doi_df


def download_paper(doi, source, path="~/Downloads/", prepop=False):
    """
    Given a DOI, downloads an article to a folder.

    Args:
        doi (str): A doi suffix (ex="10.7287/PEERJ.PREPRINTS.3100V1").
        source (str): The source to get the pdf from. One of ["sci-hub", "unpaywall"]
        path (str): The folder where the pdf will be saved.
        prepop (bool): Wether to return 'saved' dictionary.
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
        base_url = f"https://api.unpaywall.org/v2/{doi}?email=tiago.lubiana.alves@usp.br"
        response = requests.get(base_url)
        result = response.json()
        pdf_url = result["best_oa_location"]["url_for_pdf"]
        if pdf_url is None:
            warnings.warn("====== Best OA pdf not found. Searching for first OA ====== ")
            pdf_url = result["first_oa_location"]["url_for_pdf"]
        filename = doi.replace("/", "_")
        filepath = path + filename + ".pdf"
        print("====== Dowloading article from Unpaywall ======")

    os.system(f"wget -O {filepath} -q --show-progress {pdf_url} --no-clobber ")

    if prepop:
        if os.path.exists(filepath):
            return {"saved": True}
        return {"saved": False}
    print("====== Opening PDF ======")
    os.system(f"xdg-open {filepath} &")

    return 0

#!/usr/bin/python3
import requests
from glob import glob
import argparse
import pandas as pd
import re
from wikidata_bib.helper import add_to_file, remove_read_and_reading_list

import os
import yaml
from pathlib import Path
import click


HERE = Path(__file__).parent.resolve()
DATA = HERE.parent.joinpath("data").resolve()


def main():
    update_from_yaml()


def get_qids_from_query(query_url):
    """
    Returns a list of QIDs given a SPARQL query. QIDs are returned for the projection '?work' .
    """
    session = requests.Session()  # so connections are recycled
    response = session.head(query_url, allow_redirects=True)
    url_sparql = response.url.replace(
        "https://query.wikidata.org/#", "https://query.wikidata.org/sparql?query="
    )

    if "work" not in url_sparql:
        raise ValueError("SPARQL query needs to select a variable called ?work")

    sparql_query_response = requests.get(url_sparql, params={"format": "json"})
    sparql_query_result = pd.json_normalize(sparql_query_response.json()["results"]["bindings"])
    sparql_query_result["qid"] = [url.split("/")[4] for url in sparql_query_result["work.value"]]

    return list(sparql_query_result["qid"])


@click.command(name="update_from_yaml")
def update_from_yaml():
    config = yaml.load(DATA.joinpath("config.yaml").read_text(), Loader=yaml.FullLoader)

    for cat in config["queries"]:

        queries = config["queries"][cat]
        for query in queries:

            full_category_name = config["lists"][cat]
            qids = get_qids_from_query(query)
            main_list = remove_read_and_reading_list(qids)
            if full_category_name is not None:
                add_to_file(main_list, full_category_name)


if __name__ == "__main__":
    main()

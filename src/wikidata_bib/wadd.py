#!/usr/bin/python3

import requests
from glob import glob
import argparse
import pandas as pd
import re
from .helper import add_to_file, remove_read_qids, get_qids_in_reading_list


def main():
    def get_sparql_query_result(url):
        session = requests.Session()  # so connections are recycled
        response = session.head(url, allow_redirects=True)
        url_sparql = response.url.replace(
            "https://query.wikidata.org/#", "https://query.wikidata.org/sparql?query="
        )

        if "work" not in url_sparql:
            raise ValueError("SPARQL query needs to select a variable called ?work")

        sparql_query_response = requests.get(url_sparql, params={"format": "json"})
        sparql_query_result = pd.json_normalize(sparql_query_response.json()["results"]["bindings"])
        sparql_query_result["qid"] = [
            url.split("/")[4] for url in sparql_query_result["work.value"]
        ]

        return sparql_query_result

    def get_final_list_of_articles(sparql_query_result):
        list_of_qids = sparql_query_result["qid"]

        main_list = remove_read_qids(list_of_qids)
        for i in main_list:
            print(i)

        return main_list

    parser = argparse.ArgumentParser()

    # Example queries:
    # Single-cell transcriptomics articles in either nature or science: https://w.wiki/3LhF
    # Run:
    # $ ./wadd https://w.wiki/3MDs -p --new

    parser.add_argument("url", help="A short link provided by the Wikidata Query Service", type=str)
    parser.add_argument(
        "--category",
        help="The category to which the list will be appended",
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--new",
        help="Select only the articles that are not in the notes folder",
        action="store_true",
    )
    parser.add_argument(
        "--print",
        "-p",
        help="Print QIDs instead of adding to the toread file",
        action="store_true",
    )

    args = parser.parse_args()
    url = args.url
    only_add_articles_that_were_not_read_before = args.new
    category = args.category
    to_print = args.print
    print("====== QIDs for articles matching the query ====== ")

    sparql_query_result = get_sparql_query_result(url)

    if not only_add_articles_that_were_not_read_before:
        for i in sparql_query_result["qid"]:
            print(i)
    else:

        main_list = get_final_list_of_articles(sparql_query_result)

        logged_articles = get_qids_in_reading_list()
        main_list = list(set(main_list) - set(logged_articles))

    if category != None and to_print == False:
        print("====== Appending QIDs to file toread.md ====== ")
        add_to_file(main_list, category)


if __name__ == "__main__":
    main()

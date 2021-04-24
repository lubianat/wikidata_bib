#!/usr/bin/python3

from wikidata2df import wikidata2df
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import sys


def main():
    def get_doi_df(wd_id):
        query = (
            """
        SELECT ?item ?doi ?itemLabel
        WHERE
        {
        VALUES ?item {wd:"""
            + wd_id
            + """} .
        ?item wdt:P356 ?doi.  
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }
        """
        )

        df = wikidata2df(query)

        return df

    wd_id = sys.argv[1]
    doi_df = get_doi_df(wd_id)

    print(doi_df)
    if doi_df.empty == True:
        print("No DOI found for " + wd_id + ".")
    else:
        doi_suffix = doi_df["doi"].values[0]
        print("DOI: " + doi_suffix)
        download_paper(doi=doi_suffix, path="./downloads/")


def download_paper(doi, path="~/Downloads/"):
    """
    Given a DOI, downloads an article to a folder.

    Arguments:
        doi: A doi suffix (ex="10.7287/PEERJ.PREPRINTS.3100V1").
        path: The folder where the pdf will be saved.
    """
    base_url = "https://sci-hub.do/" + doi
    res = requests.get(base_url, verify=False)
    s = BeautifulSoup(res.content, "html.parser")

    iframe = s.find("iframe")
    if iframe:
        url = iframe.get("src")

    filename = url.split("/")[-1].split("#")[0]
    filepath = path + filename

    print("====== Dowloading article from Sci-Hub ======")
    # Warning:
    # Only use SciHub to get articles tha you already paid for!

    os.system(f"wget -O {filepath} {url}")

    print("====== Opening PDF ======")
    os.system(f"xdg-open {filepath} &")

    return 0


if __name__ == "__main__":
    main()


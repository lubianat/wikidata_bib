#!/usr/bin/python3

from helper import wikidata2df
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import sys
import warnings
from src.helper import download_paper, get_doi_df


def main():
    wikidata_id = sys.argv[1]
    source = sys.argv[2]
    doi_df = get_doi_df(wikidata_id)
    print("======= Looking for article DOI on Wikidata =======")
    print(doi_df)
    if doi_df.empty == True:
        print("No DOI found for " + wikidata_id + ".")

    else:
        doi_suffix = doi_df["doi"].values[0]
        print("DOI: " + doi_suffix)
        download_paper(doi=doi_suffix, source=source, path="./downloads/")


if __name__ == "__main__":
    main()

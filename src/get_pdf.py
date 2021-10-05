#!/usr/bin/python3

from helper import wikidata2df
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import sys
import yaml
import warnings


def main():
    def get_doi_df(wikidata_id):
        """
        Gets a dataframe from Wikidata with the DOI for a given QID

        Args:
            wikidata_id: The QID for a scholarly work on Wikidata. 

        Returns: 
            A pandas DataFrame with the DOI values for the work

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
        df = wikidata2df(query)
        return df

    def download_paper(doi, source, path="~/Downloads/"):
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
                f"https://api.unpaywall.org/v2/{doi}?email=unpaywall_00@example.com"
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

        os.system(f"wget -O {filepath} {pdf_url}")
        print("====== Opening PDF ======")
        os.system(f"xdg-open {filepath} &")

        return 0

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


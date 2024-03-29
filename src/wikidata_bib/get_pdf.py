"""
Downloads a pdf for the article of interest given its QID.
"""

import sys
import webbrowser
from pathlib import Path

from wikidata_bib.helper import download_paper, get_doi_df

HERE = Path(__file__).parent.resolve()


def main():
    """
    Downloads a pdf for the article of interest given its QID.
    """
    wikidata_id = sys.argv[1]
    source = sys.argv[2]
    doi_df = get_doi_df(wikidata_id)
    print("======= Looking for article DOI on Wikidata =======")
    if doi_df.empty is True:
        print("No DOI found for " + wikidata_id + ".")

    else:
        doi_suffix = doi_df["doi"].values[0]
        webbrowser.open(f"https://doi.org/{doi_suffix}")
        print("DOI: " + doi_suffix)

        downloads_path = HERE.parent.parent.joinpath("downloads/").resolve().as_posix()
        download_paper(doi=doi_suffix, source=source, path=downloads_path + "/")


if __name__ == "__main__":
    main()

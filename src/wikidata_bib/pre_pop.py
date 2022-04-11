#!/usr/bin/python3

import sys
import re
import yaml
from src.helper import add_to_file
from src.helper import download_paper, get_doi_df

# Open file with the QIDs ("src/data/toread.md")
# and the file with the shortcuts ("config.yaml")

with open("src/data/toread.md", "r") as f:
    text = f.read()

with open("config.yaml", "r") as c:
    shortcuts = yaml.load(c.read(), Loader=yaml.FullLoader)

if len(sys.argv) == 2:
    reading_list_code = sys.argv[1]
    print(
        f'====== Pulling first QID in the "{shortcuts["lists"][reading_list_code]}" list ======'
    )
    regex = shortcuts["lists"][reading_list_code] + r"[\s\S]*?(Q[0-9]*)"
else:
    print("====== Pulling first QID in toread.md ======")
    regex = r"(Q[0-9]*)"
    code = ""

qid = re.findall(regex, text)[0]

if qid == "Q":
    print("No QID found.")

else:
    # Select "unpaywall" or "sci-hub"
    source = "unpaywall"
    doi_df = get_doi_df(qid)
    print("======= Looking for article DOI on Wikidata =======")
    print(doi_df)
    if doi_df.empty == True:
        print("No DOI found for " + qid + ".")

    else:
        doi_suffix = doi_df["doi"].values[0]
        print("DOI: " + doi_suffix)
        a = download_paper(
            doi=doi_suffix, source=source, path="./downloads/", prepop=True
        )
        print(a)

        if a["saved"]:
            with open("src/data/toread.md", "w+") as f:
                f.write(text.replace(qid + "\n", ""))

            add_to_file([qid], "Saved PDFs")
            # Implement logic to create notes document from Wikidata call

        else:
            # Implement recursive logic to get next valid QID
            pass

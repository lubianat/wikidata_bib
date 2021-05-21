import requests
import sys
from glob import glob
import argparse

parser = argparse.ArgumentParser()
# Example queries:
# Single-cell transcriptomics articles in either nature or science: https://w.wiki/3LhF
# Run:
# $ python3 wadd.py --url https://w.wiki/3MDs --new

parser.add_argument(
    "url", help="A short link provided by the Wikidata Query Service", type=str
)
parser.add_argument(
    "category",
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


parser.print_help()

args = parser.parse_args()
url = args.url
only_new = args.new
category = args.category
to_print = args.print

session = requests.Session()  # so connections are recycled
resp = session.head(url, allow_redirects=True)
url_sparql = resp.url.replace(
    "https://query.wikidata.org/#", "https://query.wikidata.org/sparql?query="
)

print(url_sparql)
if "work" not in url_sparql:
    raise ValueError("SPARQL query needs to select a variable called ?work")

r = requests.get(url_sparql, params={"format": "json"})
import pandas as pd

df = pd.json_normalize(r.json()["results"]["bindings"])

df["qid"] = [url.split("/")[4] for url in df["work.value"]]

print("====== QIDs for the matching works ====== ")
if not only_new:
    for i in df["qid"]:
        print(i)
else:
    txtfiles = []
    for file_name in glob("./notes/*.md"):
        txtfiles.append(file_name)

    array_of_filenames = [name.replace(".md", "") for name in txtfiles]

    array_of_qids = []
    for item in array_of_filenames:
        if "Q" in item:
            array_of_qids.append(item)
    array_of_qids = [md.replace("./notes/Q", "Q") for md in array_of_qids]
    main_list = list(set(df["qid"]) - set(array_of_qids))
    for i in main_list:
        print(i)


def add_to_file(qids, category, filepath="toread.md"):
    """ Adds a list of qids to a file 

    Inserts each qids as a newline after the category is found.

    Attributes:
        filepath (str): The path to the file to be modified
        qids (list): A list of qids to be added to the file as newlines
        category (str): A word matching a header in the file, below it the
        newlines shall be added 
    """
    # read the file into a list of lines
    with open(filepath, "r") as f:
        lines = f.read().split("\n")

    for i, line in enumerate(lines):
        if category in line:  # or word in line.split() to search for full words
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


if category != None and to_print == False:
    print("====== Appending QIDs to file toread.md ====== ")
    add_to_file(df["qid"], category)


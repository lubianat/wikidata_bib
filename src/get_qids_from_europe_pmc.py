import urllib.parse
import requests
from helper import (
    add_to_file,
    remove_read_qids,
    get_qids_from_europe_pmc,
)
import re

category = "Cell types"
query = '"catalog of cell types"'

main_list = get_qids_from_europe_pmc(query)

# Ignore articles in toread.md
with open("toread.md", "r") as f:
    articles_file = f.read()

logged_articles = re.findall("Q[0-9]*", articles_file)
main_list = list(set(main_list) - set(logged_articles))

main_list = remove_read_qids(main_list)
if category != None:
    print("====== Appending QIDs to file toread.md ====== ")
    add_to_file(main_list, category)

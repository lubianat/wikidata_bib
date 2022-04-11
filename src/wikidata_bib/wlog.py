#!/usr/bin/python3

import pandas as pd
from src.helper import wikidata2df
import os

articles = pd.read_csv("src/data/read.csv")

wd_id = articles.tail(1)["wikidata_id"].values[0]

query = (
    """
SELECT ?item ?itemLabel ?journal ?journalLabel ?date ?alt
WHERE 
{
  VALUES ?item {wd:"""
    + wd_id
    + """}.
  OPTIONAL {?item wdt:P1433 ?journal}.
  OPTIONAL {?item wdt:P577 ?date}.
  OPTIONAL {?journal skos:altLabel ?alt}.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""
)

df = wikidata2df(query)
message = "read: " + df["itemLabel"].values[0]

bash_command = f'git add . && git commit -m "{message}"'
os.system(bash_command)
os.system("git push")

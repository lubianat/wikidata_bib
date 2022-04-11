#! /usr/bin/python3

import pandas as pd
import os
import rdflib

df = pd.read_csv("src/data/read.csv")
entries = list(df["wikidata_id"])
last_entry = entries[-1]
print(last_entry)

os.system(f"python3 wread {last_entry}")

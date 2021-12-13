#! /usr/bin/python3

import pandas as pd
import os

df = pd.read_csv("read.csv")


entries = list(df["wikidata_id"])
last_entry = entries[-1]
print(last_entry)

os.system(f"rm notes/{last_entry}.md")

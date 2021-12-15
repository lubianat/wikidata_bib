#! /usr/bin/python3

import pandas as pd
import os
import rdflib

df = pd.read_csv("read.csv")


entries = list(df["wikidata_id"])
last_entry = entries[-1]
print(last_entry)

os.system(f"rm notes/{last_entry}.md")

# Note: code has not been tested!

g = rdflib.Graph()
result = g.parse("read.ttl", format="ttl")
wb = rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/")
wbn = rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/notes/")
wd = rdflib.Namespace("http://www.wikidata.org/entity/")

s = rdflib.term.URIRef(wd + last_entry)

g.remove((s, None, None))  # remove all triples about bob
g.serialize(destination="read.ttl", format="turtle")

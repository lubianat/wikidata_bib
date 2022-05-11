#! /usr/bin/python3

# Drops the last article read with Wikidata Bib from the dashboard
# Note: info is kept on read.csv.

import pandas as pd
import os
import rdflib
import click
from pathlib import Path

HERE = Path(__file__).parent.resolve()


@click.command(name="drop")
def main():
    """
    Drops the metadata on the last read article.
    """
    df = pd.read_csv(f"{HERE}/../data/read.csv")

    entries = list(df["wikidata_id"])
    last_entry = entries[-1]
    print(f"Dropping {last_entry}")

    os.system(f"rm {HERE}/../notes/{last_entry}.md")

    g = rdflib.Graph()
    g.parse(f"{HERE}/../data/read.ttl", format="ttl")
    wd = rdflib.Namespace("http://www.wikidata.org/entity/")
    s = rdflib.term.URIRef(wd + last_entry)
    g.remove((s, None, None))  # remove all triples about the QID
    g.serialize(destination=f"{HERE}/../data/read.ttl", format="turtle")


if __name__ == "__main__":
    main()

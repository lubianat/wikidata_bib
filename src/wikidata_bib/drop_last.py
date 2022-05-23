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

    csv_path = HERE.parent.joinpath("data/read.csv").resolve()
    df = pd.read_csv(csv_path)

    entries = list(df["wikidata_id"])
    last_entry = entries[-1]
    print(f"Dropping {last_entry}")

    os.system(f"rm {HERE}/../notes/{last_entry}.md")
    g = rdflib.Graph()
    read_ttl_path = HERE.parent.joinpath("data/read.ttl").resolve()
    g.parse(read_ttl_path, format="ttl")
    wd = rdflib.Namespace("http://www.wikidata.org/entity/")
    s = rdflib.term.URIRef(wd + last_entry)
    g.remove((s, None, None))  # remove all triples about the QID
    read_ttl_path = HERE.parent.joinpath("data/read.ttl").resolve()
    g.serialize(destination=read_ttl_path, format="turtle")


if __name__ == "__main__":
    main()

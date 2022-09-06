"""
Drops the last article read with Wikidata Bib from the dashboard
"""

import os
from pathlib import Path

import click
import pandas as pd
import rdflib

HERE = Path(__file__).parent.resolve()


@click.command(name="drop")
def main():
    """
    Drops the metadata on the last read article.
    """

    csv_path = HERE.parent.joinpath("data/read.csv").resolve()
    reading_dataframe = pd.read_csv(csv_path)

    entries = list(reading_dataframe["wikidata_id"])
    last_entry = entries[-1]
    print(f"Dropping {last_entry}")

    os.system(f"rm {HERE}/../notes/{last_entry}.md")
    rdf_database = rdflib.Graph()
    read_ttl_path = HERE.parent.joinpath("data/read.ttl").resolve()
    rdf_database.parse(read_ttl_path, format="ttl")
    wd_prefix = rdflib.Namespace("http://www.wikidata.org/entity/")
    statement = rdflib.term.URIRef(wd_prefix + last_entry)
    rdf_database.remove((statement, None, None))  # remove all triples about the QID
    read_ttl_path = HERE.parent.joinpath("data/read.ttl").resolve()
    rdf_database.serialize(destination=read_ttl_path, format="turtle")


if __name__ == "__main__":
    main()

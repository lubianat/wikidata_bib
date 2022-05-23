#!/usr/bin/python3

import pandas as pd
from .helper import wikidata2df
import os
from pathlib import Path
import click

HERE = Path(__file__).parent.resolve()


@click.command(name="log")
def main():
    """
    Updates the GitHub repository with the recent data.
    """
    read_path = HERE.parent.joinpath("data/read.csv").resolve()
    articles = pd.read_csv(read_path)

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
    parent_path = HERE.parent.parent.resolve()
    bash_command = f'cd {parent_path} && git add . && git commit -m "{message}" && git push'
    os.system(bash_command)


if __name__ == "__main__":
    main()

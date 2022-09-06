"""
Reopens last read paper.
"""

import os
from pathlib import Path

import click
import pandas as pd

HERE = Path(__file__).parent.resolve()


@click.command(name="reopen")
def main():
    """
    Reopens last read paper.
    """
    read_path = HERE.parent.joinpath("data/read.csv").resolve()
    read_articles_dataframe = pd.read_csv(read_path)
    entries = list(read_articles_dataframe["wikidata_id"])
    last_entry = entries[-1]
    print(last_entry)
    os.system(f"bib read {last_entry}")


if __name__ == "__main__":
    main()

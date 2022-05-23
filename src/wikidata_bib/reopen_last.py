#! /usr/bin/python3

import pandas as pd
import os
import click
from pathlib import Path

HERE = Path(__file__).parent.resolve()


@click.command(name="reopen")
def main():
    """
    Reopens last read paper.
    """
    df = pd.read_csv(f"{HERE}/../data/read.csv")
    entries = list(df["wikidata_id"])
    last_entry = entries[-1]
    print(last_entry)
    os.system(f"bib read {last_entry}")


if __name__ == "__main__":
    main()

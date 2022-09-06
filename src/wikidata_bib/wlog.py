"""
Updates the GitHub repository with the recent data.
"""

import os
from pathlib import Path

import click
import pandas as pd

from .helper import get_title_df

HERE = Path(__file__).parent.resolve()


@click.command(name="log")
def main():
    """
    Updates the GitHub repository with the recent data.
    """
    read_path = HERE.parent.joinpath("data/read.csv").resolve()
    articles = pd.read_csv(read_path)

    wd_id = articles.tail(1)["wikidata_id"].values[0]

    basic_info_dataframe = get_title_df(wd_id)
    message = "read: " + basic_info_dataframe["itemLabel"].values[0]
    parent_path = HERE.parent.parent.resolve()
    bash_command = f'cd {parent_path} && git add . && git commit -m "{message}" && git push'
    os.system(bash_command)


if __name__ == "__main__":
    main()

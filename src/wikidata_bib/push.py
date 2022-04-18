from .helper import add_to_file


#!/usr/bin/python3

import sys
import re
import os
import yaml
import click
from pathlib import Path

HERE = Path(__file__).parent.resolve()


@click.command(name="push")
@click.argument("category")
@click.argument("qid")
def main(category: str, qid: str):
    """
    Pops the first article of the reading list into read.

    """
    text = Path(f"{HERE}/../data/toread.md").read_text()

    with open(f"{HERE}/../data/config.yaml", "r") as c:
        shortcuts = yaml.load(c.read(), Loader=yaml.FullLoader)

    reading_list_code = category
    category_full_name = shortcuts["lists"][reading_list_code]

    add_to_file(qids=[qid], category=category_full_name)


if __name__ == "__main__":
    main()

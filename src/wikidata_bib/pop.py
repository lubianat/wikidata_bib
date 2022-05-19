#!/usr/bin/python3

import sys
import re
import os
import yaml
import click
from pathlib import Path

HERE = Path(__file__).parent.resolve()


@click.command(name="pop")
@click.argument("category")
@click.option(
    "--no-download",
    is_flag=True,
    show_default=True,
    default=False,
    help="Skip the download of a PDF.",
)
def main(category: str, no_download: bool):
    """
    Pops the first article of the reading list into read.

    """
    with open(f"{HERE}/../data/toread.yaml", "r") as c:
        toread = yaml.load(c.read(), Loader=yaml.FullLoader)

    with open(f"{HERE}/../data/config.yaml", "r") as c:
        shortcuts = yaml.load(c.read(), Loader=yaml.FullLoader)

    list_name = shortcuts["lists"][category]
    print(f'====== Pulling first QID in the "{list_name}" list ======')

    if len(toread["articles"][list_name]) > 0:
        qid = toread["articles"][list_name][0]
        toread["articles"][list_name] = toread["articles"][list_name][1:]

        with open(f"{HERE}/../data/toread.yaml", "w") as f:
            yaml.dump(toread, f)

        if no_download:
            os.system(f"bib read {qid} --no-download")
        else:
            os.system(f"bib read {qid}")
    else:
        print("No QID found.")


if __name__ == "__main__":
    main()

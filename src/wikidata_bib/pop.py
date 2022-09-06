"""
Pops the first article in one of the reading lists.
"""
import os
from pathlib import Path

import click
import yaml

from .helper import get_config_dict, get_toread_dict

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
    toread = get_toread_dict()

    shortcuts = get_config_dict()
    list_name = shortcuts["lists"][category]
    print(f'====== Pulling first QID in the "{list_name}" list ======')

    if len(toread["articles"][list_name]) > 0:
        qid = toread["articles"][list_name][0]
        toread["articles"][list_name] = toread["articles"][list_name][1:]
        toread_path = HERE.parent.joinpath("data/toread.yaml").resolve()
        toread_path.write_text(yaml.dump(toread), encoding="UTF-8")

        if no_download:
            os.system(f"bib read {qid} --no-download")
        else:
            os.system(f"bib read {qid}")
    else:
        print("No QID found.")

"""
Pushes an article to the top of a reading list.
"""
from pathlib import Path

import click
from .helper import add_to_file, get_config_dict

HERE = Path(__file__).parent.resolve()


@click.command(name="push")
@click.argument("category")
@click.argument("qid")
def main(category: str, qid: str):
    """
    Pushes an article to the top of a reading list.
    """
    shortcuts = get_config_dict()
    list_name = shortcuts["lists"][category]
    add_to_file(qids=[qid], category=list_name)

#!/usr/bin/python3
from .helper import add_to_file
import click
from pathlib import Path

HERE = Path(__file__).parent.resolve()


@click.command(name="push")
@click.argument("category")
@click.argument("qid")
def main(category: str, qid: str):
    """
    Pushes an article to the top of a reading list.
    """
    add_to_file(qids=[qid], category=category)


if __name__ == "__main__":
    main()

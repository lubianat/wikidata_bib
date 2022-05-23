#!/usr/bin/python3
from .helper import add_to_file
import click
from pathlib import Path
import yaml

HERE = Path(__file__).parent.resolve()


@click.command(name="push")
@click.argument("category")
@click.argument("qid")
def main(category: str, qid: str):
    """
    Pushes an article to the top of a reading list.
    """
    config_path = HERE.parent.joinpath("data/config.yaml").resolve()
    with open(config_path, "r") as c:
        shortcuts = yaml.load(c.read(), Loader=yaml.FullLoader)

    list_name = shortcuts["lists"][category]

    add_to_file(qids=[qid], category=list_name)


if __name__ == "__main__":
    main()

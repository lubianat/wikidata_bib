"""
Queries EuropePMC and adds articles to the reading list
"""
from pathlib import Path

import click
import yaml

from .helper import (
    add_to_file,
    get_qids_from_europe_pmc,
    get_qids_in_reading_list,
    remove_read_qids,
)

HERE = Path(__file__).parent.resolve()


@click.command(name="querypmc")
@click.argument("shortcut")
@click.argument("query")
def main(shortcut: str, query: str):
    """
    Queries EuropePMC and adds articles to the reading list.
    Only adds article that (1) are not in the list and
    (2) have not been read before.
    """
    main_list = get_qids_from_europe_pmc(f'"{query}"')

    config_path = HERE.parent.joinpath("data/config.yaml").resolve()

    yaml_string = config_path.read_text(encoding="UTF-8")
    shortcuts = yaml.safe_load(yaml_string)

    category = shortcuts["lists"][shortcut]

    logged_articles = get_qids_in_reading_list()

    diff = list(set(main_list) - set(logged_articles))
    main_list = [o for o in main_list if o in diff]

    main_list = remove_read_qids(main_list)
    if category is not None:
        print("====== Appending QIDs to file toread.yaml ====== ")
        add_to_file(main_list, category)

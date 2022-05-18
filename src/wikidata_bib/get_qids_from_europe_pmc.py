from unicodedata import category
from .helper import (
    add_to_file,
    remove_read_qids,
    get_qids_from_europe_pmc,
)
import re
import click
from pathlib import Path
import yaml

HERE = Path(__file__).parent.resolve()


@click.command(name="querypmc")
@click.argument("shortcut")
@click.argument("query")
def main(shortcut: str, query: str):
    """
    Queries EuropePMC and adds articles to the reading list
    """
    main_list = get_qids_from_europe_pmc(f'"{query}"')

    with open(f"{HERE}/../data/config.yaml", "r") as c:
        shortcuts = yaml.load(c.read(), Loader=yaml.FullLoader)

    category = shortcuts["lists"][shortcut]
    # Ignore articles in toread.md
    with open(f"{HERE}/../data/toread.md", "r") as f:
        articles_file = f.read()

    logged_articles = re.findall("Q[0-9]*", articles_file)

    diff = list(set(main_list) - set(logged_articles))

    print(main_list)
    main_list = [o for o in main_list if o in diff]

    main_list = remove_read_qids(main_list)
    if category != None:
        print("====== Appending QIDs to file toread.md ====== ")
        add_to_file(main_list, category)


if __name__ == "__main__":
    main()

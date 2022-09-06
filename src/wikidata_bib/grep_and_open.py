#!/usr/bin/python3
"""
Runs "grep" for the notes and opens the matches on VS Code.
"""
import os
import re
import sys
from pathlib import Path

import inquirer
import yaml

HERE = Path(__file__).parent.resolve()
index_path = HERE.parent.joinpath("data/index.yaml").resolve()
yaml_string = index_path.read_text(encoding="UTF-8")
INDEX = yaml.safe_load(yaml_string)


def get_tag_for_grep_search(index=INDEX, selected_lookup="none"):
    """
    After prompting the user with the index, returns the selected tag.
    Args:
      index (dict): A nested dictionary containing the tags as keys.
      selected_lookup (str): The lookup tag/key to open a lower
      level of the nested dict.
    """

    options = []
    for item in index:
        if isinstance(item, dict):
            for key in item:
                item_string = key
            options.append(item_string)

        else:
            options.append(item)

    inquirer_question = [
        inquirer.List("search", message="What topic are you looking for?", choices=options),
    ]

    answer = inquirer.prompt(inquirer_question)
    selected_lookup = answer["search"]
    search_at_level = input("Search at this level? (y/n)")

    if search_at_level == "y":
        return selected_lookup
    print("Searching down the tree")
    for _, item in enumerate(index):
        if selected_lookup in item:
            if isinstance(item, str):
                print(f"No more levels below. Searching for {selected_lookup}")
                return selected_lookup
            selected_lookup = get_tag_for_grep_search(
                item[selected_lookup], selected_lookup=selected_lookup
            )

    return selected_lookup


try:
    if sys.argv[1] == "ls":

        selected = get_tag_for_grep_search(INDEX)
        print("-----------")
        print(selected)
        print("-----------")

        search_string = " " + selected.split(" ")[0]
        search_string = re.escape(search_string)

    else:
        search_string = text = input("Add your search string:")

except Exception:
    print("ERROR")
    search_string = input("Add your search string:")


print("If there are notes they should appear below:")

# Future maybe remove false positives: grep -r "3\.1" *.md | grep -v "\.3\.1"
os.system(
    f"""
cd "$(dirname "{sys.argv[0]}")"
cd notes
grep -r --color=always  "{search_string}"
echo -n "Open notes in Virtual Studio Code(y/n)? "
old_stty_cfg=$(stty -g)
stty raw -echo ; answer=$(head -c 1) ; stty $old_stty_cfg # Careful playing with stty
if echo "$answer" | grep -iq "^y" ;then
    grep -r -l "{search_string}" | xargs code
else
    echo Ok!
fi
"""
)

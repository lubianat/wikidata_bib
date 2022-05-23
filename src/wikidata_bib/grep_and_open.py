#!/usr/bin/python3

import os
import sys
import inquirer
import re
import yaml

with open("index.yaml", "r") as f:
    index = yaml.load(f.read())


def get_answer(index, selected="none"):

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

    selected = answer["search"]

    search_at_level = input("Search at this level? (y/n)")

    if search_at_level == "y":
        return selected
    else:
        print("Searching down the tree")
        for i, item in enumerate(index):
            if selected in item:
                if isinstance(item, str):
                    print(f"No more levels below. Searching for {selected}")
                    return selected
                else:
                    selected = get_answer(item[selected], selected=selected)

    return selected


try:
    sys.argv[1]
    if sys.argv[1] == "ls":

        selected = get_answer(index)

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
    pass

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

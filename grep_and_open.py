#!/usr/bin/python3

import os
import sys
import inquirer
import re

questions = [
    inquirer.List(
        "search",
        message="What topic are you looking for",
        choices=[
            "1.1. The quest for interoperable knowledge",
            "1.2. Formal representation of knowledge",
            "1.3. Knowledge Representation in biology",
            "1.3.2. Biological knowledgebases",
            "3.1. Cell-type markers in Wikidata",
        ],
    ),
]
try:
    sys.argv[1]
    print(sys.argv[1])

    if sys.argv[1] == "ls":
        answers = inquirer.prompt(questions)
        search_string = answers["search"].split(" ")[0]
        search_string = re.escape(search_string)

    else:
        search_string = text = input("Add your search string:")


except:
    search_string = text = input("Add your search string:")
    pass

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

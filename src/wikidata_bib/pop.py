#!/usr/bin/python3

import sys
import re
import os
import yaml

# Open file with the QIDs ("src/data/toread.md")
# and the file with the shortcuts ("config.yaml")

with open("src/data/toread.md", "r") as f:
    text = f.read()

with open("config.yaml", "r") as c:
    shortcuts = yaml.load(c.read(), Loader=yaml.FullLoader)

if len(sys.argv) == 2:

    reading_list_code = sys.argv[1]
    print(
        f'====== Pulling first QID in the "{shortcuts["lists"][reading_list_code]}" list ======'
    )
    regex = shortcuts["lists"][reading_list_code] + r"[\s\S]*?(Q[0-9]*)"
else:
    print("====== Pulling first QID in toread.md ======")
    regex = r"(Q[0-9]*)"
    code = ""

qid = re.findall(regex, text)[0]

if qid == "Q":
    print("No QID found.")

else:
    with open("src/data/toread.md", "w+") as f:
        f.write(text.replace(qid + "\n", ""))
    os.system(f"python3 wread {qid}")

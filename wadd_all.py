#!/usr/bin/python3
import os
import yaml

# Open file with the QIDs ("toread.md")
# and the file with the shortcuts ("config.yaml")

with open("toread.md", "r") as f:
    text = f.read()


with open("config.yaml", "r") as c:
    config = yaml.load(c.read(), Loader=yaml.FullLoader)

print(config["queries"])

for cat in config["queries"]:
    print(cat)

    queries = config["queries"][cat]

    for query in queries:

        full_cat_name = config["lists"][cat]
        os.system(f"./wadd {query} --new --category='{full_cat_name}' ")

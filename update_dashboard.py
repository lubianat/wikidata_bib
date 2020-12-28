import os
import glob
import urllib.parse
import pandas as pd
import unicodedata
from wbib.wbib import render_dashboard

### Update table with notes

articles = pd.read_csv("read.csv")
articles = articles
articles["wikidata_id"] = ["<a href=./notes/" + i + ".md> " + i + "</a>" for i in articles["wikidata_id"]]
test = articles.to_html(escape="True")
test = test.replace("&lt;", " <").replace("&gt;", ">")

with open("notes.html", "w") as f:
    f.write(test)

### Update dashboard with queries

arr = os.listdir("notes")
txtfiles = []

for file in glob.glob("./notes/*.md"):
    txtfiles.append(file)
    
arr = [md.replace(".md", "")for md in txtfiles]

arr_qid = []
for item in arr:
    if "Q" in item:
        arr_qid.append(item)
arr_qid = [md.replace("./notes/Q", "wd:Q")for md in arr_qid]

readings = "{"
for i in arr_qid:
    readings = readings + " " + i
readings = readings + " }"

with open("index.html", "w") as f:
    html = render_dashboard(readings)
    f.write(html)
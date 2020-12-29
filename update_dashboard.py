import os
import glob
import urllib.parse
import pandas as pd
import unicodedata
from wbib.wbib import render_dashboard
import sys
from wikidata2df import wikidata2df
from mdutils.mdutils import MdUtils
import pandas as pd
import os.path
import rdflib
from datetime import date, datetime, timedelta
import os
import glob
import urllib.parse
import pandas as pd
import unicodedata
from wbib.wbib import render_dashboard
from pathlib import Path
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


g = rdflib.Graph()
result = g.parse("read.ttl", format="ttl")
wb=rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/")
wbc=rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/collections/")
wbn=rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/notes/")
wd=rdflib.Namespace("http://www.wikidata.org/entity/")

qres = g.query(
    """
    SELECT DISTINCT ?a ?time
       WHERE {
          ?a wb:read_in ?time .
       }""")


cols = ["item", "date_string"]
dat = pd.DataFrame(columns = cols)
for row in qres:
    dat = dat.append({'item': str(row[0]), 'date_string':row[1]},ignore_index=True)

dat["date"] = [datetime.strptime(i, "+%Y-%m-%dT00:00:00Z/11") for i in dat["date_string"]]

dat["month_year_pair"] = [date.strftime("%Y") + "/" + date.strftime("%B") for date in dat["date"]]

for pair in set(dat["month_year_pair"]):
    year = pair.split("/")[0]
    Path(f"./{year}").mkdir(parents=True, exist_ok=True)

    mini_dat = dat[dat["month_year_pair"] == pair]
    ids = [i.split("/")[4] for i in mini_dat["item"]]
    
    readings = "{"
    for i in ids:
        readings = readings + "wd:" + i + " "
    readings = readings + " }"

    with open(pair + ".html", "w") as f:
        html = render_dashboard(readings)

        f.write(html)


week_dat = dat[dat["date"] > (datetime.today() - timedelta(days=7))]
ids = [i.split("/")[4] for i in week_dat["item"]]

readings = "{"
for i in ids:
    readings = readings + "wd:" + i + " "
readings = readings + " }"

with open("this_week.html", "w") as f:
    html = render_dashboard(readings)

    f.write(html)


last_day = dat[dat["date"] == max(dat["date"])]
ids = [i.split("/")[4] for i in last_day["item"]]

readings = "{"
for i in ids:
    readings = readings + "wd:" + i + " "
readings = readings + " }"

with open("last_day.html", "w") as f:
    html = render_dashboard(readings)

    f.write(html)

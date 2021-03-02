from datetime import date, datetime, timedelta
from wikidata2df import wikidata2df
from mdutils.mdutils import MdUtils
import sys
import unicodedata
import pandas as pd
import os
import os.path
import rdflib
from pathlib import Path
import glob
import urllib.parse
from wbib.wbib import render_dashboard

# Set functions

def format_ids(ids):
    formatted_readings = "{"
    for i in ids:
        formatted_readings = formatted_readings + "wd:" + i + " "
    formatted_readings = formatted_readings + " }"
    return formatted_readings



### Update table with notes

articles = pd.read_csv("read.csv")
articles = articles
articles["wikidata_id"] = ["<a href=./notes/" + i + ".md> " + i + "</a>" for i in articles["wikidata_id"]]
test = articles.to_html(escape="True")
test = test.replace("&lt;", " <").replace("&gt;", ">")

with open("notes.html", "w") as f:
    f.write(test)

### Update dashboard with queries

txtfiles = []
for file in glob.glob("./notes/*.md"):
    txtfiles.append(file)
    
array_of_filenames = [md.replace(".md", "")for md in txtfiles]

array_of_qids = []
for item in array_of_filenames:
    if "Q" in item:
        array_of_qids.append(item)
array_of_qids = [md.replace("./notes/Q", "wd:Q")for md in array_of_qids]

formatted_readings = format_ids(array_of_qids)

with open("index.html", "w") as f:
    html = render_dashboard(formatted_readings)
    f.write(html)


g = rdflib.Graph()
result = g.parse("read.ttl", format="ttl")
wb=rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/")
wbc=rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/collections/")
wbn=rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/notes/")
wd=rdflib.Namespace("http://www.wikidata.org/entity/")

query_result = g.query(
    """
    SELECT DISTINCT ?a ?time
       WHERE {
          ?a wb:read_in ?time .
       }""")


cols = ["item", "date_string"]

articles_dataframe = pd.DataFrame(columns = cols)
for row in query_result:
    qid = str(row[0])
    date_string = row[1]
    articles_dataframe = articles_dataframe.append({'item': qid, 'date_string':date_string}, ignore_index=True)


dates_in_date_format = [datetime.strptime(i, "+%Y-%m-%dT00:00:00Z/11") for i in articles_dataframe["date_string"]]
articles_dataframe["date"] = dates_in_date_format

month_year_pairs = [date.strftime("%Y") + "/" + date.strftime("%B") for date in articles_dataframe["date"]]
articles_dataframe["month_year_pair"] = month_year_pairs

for pair in set(articles_dataframe["month_year_pair"]):
    year = pair.split("/")[0]

    # Create directory for year
    Path(f"./{year}").mkdir(parents=True, exist_ok=True)

    mini_df = articles_dataframe[articles_dataframe["month_year_pair"] == pair]
    ids = [i.split("/")[4] for i in mini_df["item"]]

    formatted_readings = format_ids(ids)

    with open(pair + ".html", "w") as f:
        html = render_dashboard(formatted_readings)

        f.write(html)


week_dat = articles_dataframe[articles_dataframe["date"] > (datetime.today() - timedelta(days=7))]
ids = [i.split("/")[4] for i in week_dat["item"]]

formatted_readings = format_ids(ids)

with open("this_week.html", "w") as f:
    html = render_dashboard(formatted_readings)

    f.write(html)


last_day = articles_dataframe[articles_dataframe["date"] == max(articles_dataframe["date"])]
ids = [i.split("/")[4] for i in last_day["item"]]

formatted_readings = format_ids(ids)

with open("last_day.html", "w") as f:
    html = render_dashboard(formatted_readings)

    f.write(html)

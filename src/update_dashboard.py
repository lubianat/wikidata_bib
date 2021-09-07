from datetime import date, datetime, timedelta
from helper import wikidata2df
from mdutils.mdutils import MdUtils
import unicodedata
import pandas as pd
import os
import os.path
import rdflib
from pathlib import Path
from glob import glob
import urllib.parse
import wbib.queries
from wbib import wbib


sessions = [
    "articles",
    "map of institutions",
    "list of authors",
    "list of topics",
    "list of journals",
    "curation of author items",
    "curation of author affiliations",
]


base_directory = "/docs"

PAGES = {
    "all time": {"name": "all time", "href": f"{base_directory}/"},
    "last_month": {"name": "past month", "href": f"{base_directory}/past_month.html"},
    "last week": {"name": "past week", "href": f"{base_directory}/past_week.html"},
    "last day": {"name": "last day", "href": f"{base_directory}/last_day.html"},
}


### Update table with notes


articles = pd.read_csv("read.csv")
articles = articles
articles["wikidata_id"] = [
    "<a href=./notes/" + i + ".md> " + i + "</a>" for i in articles["wikidata_id"]
]
test = articles.to_html(escape="True")
test = test.replace("&lt;", " <").replace("&gt;", ">")

with open("docs/notes.html", "w") as f:
    f.write(test)

### Update dashboard with queries

txtfiles = []
for file_name in glob("./notes/*.md"):
    txtfiles.append(file_name)

array_of_filenames = [name.replace(".md", "") for name in txtfiles]


array_of_qids = []
for item in array_of_filenames:
    if "Q" in item:
        array_of_qids.append(item)
array_of_qids = [md.replace("./notes/Q", "Q") for md in array_of_qids]


html = wbib.render_dashboard(
    info=array_of_qids,
    mode="basic",
    filepath="docs/index.html",
    pages=PAGES,
    sections_to_add=sessions,
    site_title="Wikidata Bib",
    site_subtitle="Dashboard of Tiago Lubiana's readings",
)


g = rdflib.Graph()
result = g.parse("read.ttl", format="ttl")
wb = rdflib.Namespace("https://wikidatabib.wiki.opencura.com/wiki/")
wd = rdflib.Namespace("http://www.wikidata.org/entity/")

query_result = g.query(
    """
    SELECT DISTINCT ?a ?time
       WHERE {
          ?a wb:read_in ?time .
       }"""
)


cols = ["item", "date_string"]

articles_dataframe = pd.DataFrame(columns=cols)
for row in query_result:
    qid = str(row[0])
    date_string = row[1]
    articles_dataframe = articles_dataframe.append(
        {"item": qid, "date_string": date_string}, ignore_index=True
    )


dates_in_date_format = [
    datetime.strptime(i, "+%Y-%m-%dT00:00:00Z/11")
    for i in articles_dataframe["date_string"]
]
articles_dataframe["date"] = dates_in_date_format

month_dat = articles_dataframe[
    articles_dataframe["date"] > (datetime.today() - timedelta(days=30))
]
ids = [i.split("/")[4] for i in month_dat["item"]]


html = wbib.render_dashboard(
    info=ids,
    mode="basic",
    filepath="docs/past_month.html",
    pages=PAGES,
    sections_to_add=sessions,
    site_title="Wikidata Bib",
    site_subtitle="Dashboard of Tiago Lubiana's readings",
)


week_dat = articles_dataframe[
    articles_dataframe["date"] > (datetime.today() - timedelta(days=7))
]
ids = [i.split("/")[4] for i in week_dat["item"]]

html = wbib.render_dashboard(
    info=ids,
    mode="basic",
    filepath="docs/past_week.html",
    pages=PAGES,
    sections_to_add=sessions,
    site_title="Wikidata Bib",
    site_subtitle="Dashboard of Tiago Lubiana's readings",
)

try:
    last_day = articles_dataframe[
        articles_dataframe["date"] == max(articles_dataframe["date"])
    ]
    ids = [i.split("/")[4] for i in last_day["item"]]

    html = wbib.render_dashboard(
        info=ids,
        mode="basic",
        filepath="docs/last_day.html",
        pages=PAGES,
        sections_to_add=sessions,
        site_title="Wikidata Bib",
        site_subtitle="Dashboard of Tiago Lubiana's readings",
    )
except ValueError as e:
    message(
        "Last day html will be available when Wikidata Bib is used for multiple days"
    )


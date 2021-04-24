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
from glob import glob
import urllib.parse
import os
import urllib.parse
import pandas as pd
import unicodedata
import wbib.queries


def render_dashboard(readings):

    url1 = wbib.queries.get_query_url_for_articles(readings)
    url1_legend = "Articles read"
    url2 = wbib.queries.get_query_url_for_topic_bubble(readings)
    url2_legend = "Topics of those articles (as bubbles)"
    url4 = wbib.queries.get_query_url_for_venues(readings)
    url4_legend = "Most read journals "
    url5 = wbib.queries.get_query_url_for_authors(readings)
    url5_legend = "Authors of papers I've read"
    url6 = wbib.queries.get_query_url_for_locations(readings)
    url6_legend = "Map of institutions"
    url7 = wbib.queries.get_query_url_for_citing_authors(readings)
    url7_legend = "Authors that cite those works"

    license_statement = """
            This content is available under a <a target="_blank" href="https://creativecommons.org/publicdomain/zero/1.0/"> 
            Creative Commons CC0</a> license.
  """
    code_availability_statement = """
  Source code for the website available at <a target="_blank" href="https://github.com/lubianat/wikidata_bib">
            https://github.com/lubianat/wikidata_bib </a>
  """

    scholia_credit_statement = """
SPARQL queries adapted from <a target="_blank" href="https://scholia.toolforge.org/">Scholia</a>
  """

    creator_statement = """
 Dashboard  by <a target="_blank" href="https://www.wikidata.org/wiki/User:TiagoLubiana">TiagoLubiana</a>
  """

    site_title = "Wikidata Bib"
    site_subtitle = """ Tiago Lubiana's personal reading status"""
    html = (
        """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>"""
        + site_title
        + """</title>
  <meta property="og:description" content="powered by Wikidata">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
  <link href="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js" rel="stylesheet"
    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.2/css/bulma.min.css">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>
  <section class="section">
    <div class="container">
      <div class="columns is-centered">
        <div class="column is-half has-text-centered">
          <h1 class="title is-1"> """
        + site_title
        + """</h1>
          <h2>"""
        + site_subtitle
        + """</h2>
        </div>
      </div>
    </div>
    <div class="column is-half has-text-centered">
  </section>
   </section>

   <div role="navigation">
<ul class="nav nav-pills justify-content-center">
  <li class="nav-item">
    <a class="nav-link" aria-current="page" href="/wikidata_bib/">All time</a>
  </li>
    <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/2020/November.html">November 2020</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/2020/December.html">December 2020</a>
  </li>
    </li>
   <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/2021/January.html">January 2021</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/2021/February.html">February 2021</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/2021/March.html">March 2021</a>
  </li>
   <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/this_week.html">This week</a>
  </li>
  <li class="nav-item">
    <a class="nav-link" href="/wikidata_bib/last_day.html">Last day</a>
  </li>
</ul>
</div>
      <h5 class="title is-5" style="text-align:center;"> """
        + url1_legend
        + """</h5>
        <p align="center">
          <iframe width=75% height="400" src="""
        + '"'
        + url1
        + '"'
        + """></iframe>
        </p>
    <br></br>
    <h5 class="title is-5" style="text-align:center;">"""
        + url2_legend
        + """ </h5>
        <p align="center">
        <iframe width=75%  height="400" src="""
        + '"'
        + url2
        + '"'
        + """></iframe>
        </p>
        <br></br>
      <h5 class="title is-5" style="text-align:center;display:block;"> """
        + url4_legend
        + """</h5>
                  <p align="center">
          <iframe width=75%   height="400" src="""
        + '"'
        + url4
        + '"'
        + """></iframe>
          </p>
   <br></br>
      <h5 class="title is-5" style="text-align:center;"> """
        + url5_legend
        + """  </h5>
        <p align="center">
            <iframe width=75%  height="400" src="""
        + '"'
        + url5
        + '"'
        + """></iframe>
        </p>
<br></br>
      <h5 class="title is-5" style="text-align:center;"> """
        + url6_legend
        + """ </h5>
      <p align="center">
            <iframe width=75%  height="400" src="""
        + '"'
        + url6
        + '"'
        + """></iframe>
      </p>
<br></br>
      <h5 class="title is-5" style="text-align:center;"> """
        + url7_legend
        + """ </h5>
      <p align="center">
            <iframe width=75%  height="400" src="""
        + '"'
        + url7
        + '"'
        + """></iframe>
      </p>
<br></br>
  </p>
  </div>
 </br>
  <footer class="footer">
    <div class="container">
      <div class="content has-text-centered">
        <p>"""
        + license_statement
        + """  </p>
        <p>"""
        + code_availability_statement
        + """ </p>
        <p>"""
        + scholia_credit_statement
        + """</p>
        <p>"""
        + creator_statement
        + """ </p>
      </div>
    </div>
  </footer>
</body>
</html>
  """
    )
    return html


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


formatted_readings = format_ids(array_of_qids)

with open("docs/index.html", "w") as f:
    html = render_dashboard(formatted_readings)
    f.write(html)


g = rdflib.Graph()
result = g.parse("read.ttl", format="ttl")
wb = rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/")
wbc = rdflib.Namespace(
    "https://github.com/lubianat/wikidata_bib/tree/main/collections/"
)
wbn = rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/notes/")
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

month_year_pairs = [
    date.strftime("%Y") + "/" + date.strftime("%B")
    for date in articles_dataframe["date"]
]
articles_dataframe["month_year_pair"] = month_year_pairs


for pair in set(articles_dataframe["month_year_pair"]):
    year = pair.split("/")[0]

    # Create directory for year
    Path(f"./{year}").mkdir(parents=True, exist_ok=True)

    mini_df = articles_dataframe[articles_dataframe["month_year_pair"] == pair]
    ids = [i.split("/")[4] for i in mini_df["item"]]

    formatted_readings = format_ids(ids)

    with open("docs/" + pair + ".html", "w") as f:
        html = render_dashboard(formatted_readings)

        f.write(html)


week_dat = articles_dataframe[
    articles_dataframe["date"] > (datetime.today() - timedelta(days=7))
]
ids = [i.split("/")[4] for i in week_dat["item"]]

formatted_readings = format_ids(ids)

with open("docs/this_week.html", "w") as f:
    html = render_dashboard(formatted_readings)

    f.write(html)


last_day = articles_dataframe[
    articles_dataframe["date"] == max(articles_dataframe["date"])
]
ids = [i.split("/")[4] for i in last_day["item"]]

formatted_readings = format_ids(ids)

with open("docs/last_day.html", "w") as f:
    html = render_dashboard(formatted_readings)

    f.write(html)

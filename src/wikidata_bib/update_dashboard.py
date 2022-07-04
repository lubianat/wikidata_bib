from datetime import datetime, timedelta
import pandas as pd
import rdflib
import wbib.queries
from wbib import wbib
from pathlib import Path


def main():
    HERE = Path(__file__).parent.resolve()

    sessions = [
        "articles",
        "map of institutions",
        "list of authors",
        "list of topics",
        "list of journals",
        "curation of author items",
        "curation of author affiliations",
    ]

    base_directory = "/wikidata_bib"

    PAGES = {
        "all time": {"name": "all time", "href": f"{base_directory}/"},
        "last_month": {"name": "past month", "href": f"{base_directory}/past_month.html"},
        "last week": {"name": "past week", "href": f"{base_directory}/past_week.html"},
        "last day": {"name": "last day", "href": f"{base_directory}/last_day.html"},
    }

    ### Update table with notes
    read_path = HERE.parent.joinpath("data/read.csv").resolve()
    articles = pd.read_csv(read_path)
    articles = articles
    articles["wikidata_id"] = [
        "<a href=./notes/" + i + ".md> " + i + "</a>" for i in articles["wikidata_id"]
    ]
    test = articles.to_html(escape="True")
    test = test.replace("&lt;", " <").replace("&gt;", ">")

    notes_path = HERE.parent.parent.joinpath("docs/notes.html").resolve()
    notes_path.write_text(test)

    ### Update dashboard with queries

    g = rdflib.Graph()
    result = read_ttl_path = HERE.parent.joinpath("data/read.ttl").resolve()
    g.parse(read_ttl_path, format="ttl")
    wb = rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/")
    wbc = rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/collections/")
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
    papers_df = pd.DataFrame(columns=cols)
    for row in query_result:
        qid = str(row[0])
        date_string = row[1]
        new_row = pd.DataFrame({"item": qid, "date_string": date_string}, index=[0])

        papers_df = pd.concat([papers_df, new_row])

    dates_in_date_format = [
        datetime.strptime(i, "+%Y-%m-%dT00:00:00Z/11") for i in papers_df["date_string"]
    ]
    papers_df["date"] = dates_in_date_format

    ids = [i.split("/")[4] for i in papers_df["item"]]

    docs_path = HERE.parent.parent.joinpath("docs").resolve()

    index_path = docs_path.joinpath("index.html").resolve()
    wbib.render_dashboard(
        info=ids,
        mode="basic",
        filepath=index_path,
        pages=PAGES,
        sections_to_add=sessions,
        site_title="Wikidata Bib",
        site_subtitle="Dashboard of Tiago Lubiana's readings",
    )

    month_dat = papers_df[papers_df["date"] > (datetime.today() - timedelta(days=30))]
    ids = [i.split("/")[4] for i in month_dat["item"]]

    past_month_path = docs_path.joinpath("past_month.html").resolve()
    wbib.render_dashboard(
        info=ids,
        mode="basic",
        filepath=past_month_path,
        pages=PAGES,
        sections_to_add=sessions,
        site_title="Wikidata Bib",
        site_subtitle="Dashboard of Tiago Lubiana's readings",
    )

    week_dat = papers_df[papers_df["date"] > (datetime.today() - timedelta(days=7))]
    ids = [i.split("/")[4] for i in week_dat["item"]]

    past_week_path = docs_path.joinpath("past_week.html").resolve()
    wbib.render_dashboard(
        info=ids,
        mode="basic",
        filepath=past_week_path,
        pages=PAGES,
        sections_to_add=sessions,
        site_title="Wikidata Bib",
        site_subtitle="Dashboard of Tiago Lubiana's readings",
    )

    last_day = papers_df[papers_df["date"] == max(papers_df["date"])]
    ids = [i.split("/")[4] for i in last_day["item"]]
    last_day_path = docs_path.joinpath("last_day.html").resolve()
    wbib.render_dashboard(
        info=ids,
        mode="basic",
        filepath=last_day_path,
        pages=PAGES,
        sections_to_add=sessions,
        site_title="Wikidata Bib",
        site_subtitle="Dashboard of Tiago Lubiana's readings",
    )


if __name__ == "__main__":
    main()

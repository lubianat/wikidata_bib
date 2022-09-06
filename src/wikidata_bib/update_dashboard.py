"""
Updates the Wikidata Bib dashboard.
"""
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import rdflib
import wbib.queries
from wbib import wbib

HERE = Path(__file__).parent.resolve()

BASE_DIR = "/wikidata_bib"

PAGES = {
    "all time": {"name": "all time", "href": f"{BASE_DIR}/"},
    "last_month": {"name": "past month", "href": f"{BASE_DIR}/past_month.html"},
    "last week": {"name": "past week", "href": f"{BASE_DIR}/past_week.html"},
    "last day": {"name": "last day", "href": f"{BASE_DIR}/last_day.html"},
}


def main():
    """
    Updates the Wikidata Bib dashboard.
    """

    sessions = [
        "articles",
        "map of institutions",
        "list of authors",
        "list of topics",
        "list of journals",
        "curation of author items",
        "curation of author affiliations",
    ]

    ### Update table with notes
    read_path = HERE.parent.joinpath("data/read.csv").resolve()
    articles = pd.read_csv(read_path)
    articles["wikidata_id"] = [
        "<a href=./notes/" + i + ".md> " + i + "</a>" for i in articles["wikidata_id"]
    ]
    basic_list_of_notes = articles.to_html(escape="True")
    basic_list_of_notes = basic_list_of_notes.replace("&lt;", " <").replace("&gt;", ">")

    notes_path = HERE.parent.parent.joinpath("docs/notes.html").resolve()
    notes_path.write_text(basic_list_of_notes, encoding="UTF-8")

    ### Update dashboard with queries

    graph = rdflib.Graph()
    read_ttl_path = HERE.parent.joinpath("data/read.ttl").resolve()
    graph.parse(read_ttl_path, format="ttl")

    query_result = graph.query(
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

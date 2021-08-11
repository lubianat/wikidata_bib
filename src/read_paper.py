#!/usr/bin/python3

import sys
from helper import wikidata2df
from mdutils.mdutils import MdUtils
import pandas as pd
import urllib.parse
import os.path
import rdflib
from datetime import date, datetime
import wbib.queries


def main():
    def get_title_df(wikidata_id):
        query = (
            """
        SELECT ?item ?itemLabel ?date ?doi ?url
        WHERE
        {
        VALUES ?item {wd:"""
            + wikidata_id
            + """}
        OPTIONAL {?item wdt:P577 ?date}.
        OPTIONAL {?item wdt:P356 ?doi} .
        OPTIONAL {?item wdt:P953 ?url}
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }
        """
        )

        df = wikidata2df(query)

        return df

    def create_markdown(file_path, title, publication_date="None", doi="", url=""):
        mdFile = MdUtils(file_name=file_path, title=title)

        mdFile.new_line("  [@wikidata:" + wikidata_id + "]")
        mdFile.new_line()

        if publication_date != "None":
            mdFile.new_line("Publication date : " + str(publication_date))

        mdFile.new_line()
        mdFile.new_header(1, "Highlights")
        mdFile.new_header(1, "Comments")
        mdFile.new_header(2, "Tags")
        mdFile.new_header(1, "Links")
        mdFile.new_line(
            f" * [Scholia Profile](https://scholia.toolforge.org/work/{wikidata_id})"
        )
        mdFile.new_line(f" * [Wikidata](https://www.wikidata.org/wiki/{wikidata_id})")
        mdFile.new_line(
            f" * [TABernacle](https://tabernacle.toolforge.org/?#/tab/manual/{wikidata_id}/P921%3BP4510)"
        )
        mdFile.new_line(
            " * [Author Disambiguator](https://author-disambiguator.toolforge.org/work_item_oauth.php?id="
            + wikidata_id
            + "&batch_id=&match=1&author_list_id=&doit=Get+author+links+for+work)"
        )
        if doi != "":
            mdFile.new_line(f" * [DOI](https://doi.org/{doi})")

        if url != "":
            mdFile.new_line(f" * [Full text URL]({url})")
        mdFile.new_line()
        mdFile.create_md_file()

    def update_turtle(wikidata_id):
        g = rdflib.Graph()
        result = g.parse("read.ttl", format="ttl")
        wb = rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/")
        wbn = rdflib.Namespace(
            "https://github.com/lubianat/wikidata_bib/tree/main/notes/"
        )
        wd = rdflib.Namespace("http://www.wikidata.org/entity/")

        s = rdflib.term.URIRef(wd + wikidata_id)
        p1 = rdflib.term.URIRef(wb + "has_notes")
        o1 = rdflib.term.URIRef(wbn + wikidata_id + ".md")
        g.add((s, p1, o1))

        g.serialize(destination="read.ttl", format="turtle")

        today = date.today()
        d1 = today.strftime("+%Y-%m-%dT00:00:00Z/11")
        s = rdflib.term.URIRef(wd + wikidata_id)
        p2 = rdflib.term.URIRef(wb + "read_in")
        o2 = rdflib.term.Literal(d1)
        g.add((s, p2, o2))

        g.serialize(destination="read.ttl", format="turtle")

    def update_csv(df):
        df_stored = pd.read_csv("read.csv")
        new_row = {"human_id": df["itemLabel"][0], "wikidata_id": df["item"][0]}
        df_stored = df_stored.append(new_row, ignore_index=True)
        df_stored = df_stored.drop_duplicates()
        print(df_stored)
        df_stored.to_csv("read.csv", index=False)

    wikidata_id = sys.argv[1]

    print("======= Getting title from Wikidata =======")
    df = get_title_df(wikidata_id)
    update_csv(df)

    title = df["itemLabel"][0]

    try:
        publication_date = df["date"][0]

        date_in_dateformat = datetime.strptime(publication_date, "%Y-%m-%dT00:00:00Z")
        publication_date = date_in_dateformat.strftime("%d of %B, %Y")
    except:
        publication_date = "None"
        pass

    try:
        doi = df["doi"][0]
    except:
        doi = ""
        pass

    try:
        text_url = df["url"][0]
    except:
        text_url = ""
        pass
    file_path = "notes/" + wikidata_id

    print("======= Creating markdown =======")
    create_markdown(file_path, title, publication_date, doi, text_url)
    update_turtle(wikidata_id)

    print("======= Updating dashboard =======")
    exec(open("src/update_dashboard.py").read())

    print("======= Done =======")


if __name__ == "__main__":
    wikidata_id = sys.argv[1]
    assert wikidata_id[0] == "Q"
    filename = "notes/" + wikidata_id + ".md"

    if os.path.isfile(filename):
        print("Article has already been read")
    else:
        main()

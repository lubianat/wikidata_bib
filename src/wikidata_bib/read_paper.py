#!/usr/bin/python3

import sys
from mdutils.mdutils import MdUtils
import pandas as pd
import os.path
import rdflib
from datetime import date, datetime
from helper import get_title_df
from pathlib import Path

HERE = Path(__file__).parent.resolve()


def main():
    def create_markdown(file_path, title, publication_date="None", doi="", url="", arxiv_id=""):
        """
        Creates a markdown file for notes from the Wikidata ID.
        """
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
        mdFile.new_line(f" * [Scholia Profile](https://scholia.toolforge.org/work/{wikidata_id})")
        mdFile.new_line(f" * [Wikidata](https://www.wikidata.org/wiki/{wikidata_id})")
        mdFile.new_line(
            " * [Author Disambiguator](https://author-disambiguator.toolforge.org/work_item_oauth.php?id="
            + wikidata_id
            + "&batch_id=&match=1&author_list_id=&doit=Get+author+links+for+work)"
        )
        if doi != "":
            mdFile.new_line(f" * [DOI](https://doi.org/{doi})")

        if url != "":
            mdFile.new_line(f" * [Full text URL]({url})")

        if arxiv_id != "":
            mdFile.new_line(f" * [arXiv ID](https://arxiv.org/pdf/{arxiv_id}.pdf)")
        mdFile.new_line()
        mdFile.create_md_file()

    def update_turtle(wikidata_id):
        """
        Opens and updates the local RDF database int Turtle format
        that records the articles that have been read.
        """
        g = rdflib.Graph()
        read_ttl_path = HERE.parent.joinpath("data/read.ttl").resolve()
        g.parse(read_ttl_path, format="ttl")
        wb = rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/")
        wbn = rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/notes/")
        wd = rdflib.Namespace("http://www.wikidata.org/entity/")

        s = rdflib.term.URIRef(wd + wikidata_id)
        p1 = rdflib.term.URIRef(wb + "has_notes")
        o1 = rdflib.term.URIRef(wbn + wikidata_id + ".md")
        g.add((s, p1, o1))

        read_ttl_path = HERE.parent.joinpath("data/read.ttl").resolve()
        g.serialize(destination=read_ttl_path, format="turtle")

        today = date.today()
        d1 = today.strftime("+%Y-%m-%dT00:00:00Z/11")
        s = rdflib.term.URIRef(wd + wikidata_id)
        p2 = rdflib.term.URIRef(wb + "read_in")
        o2 = rdflib.term.Literal(d1)
        g.add((s, p2, o2))

        read_ttl_path = HERE.parent.joinpath("data/read.ttl").resolve()
        g.serialize(destination=read_ttl_path, format="turtle")

    def update_csv(df):
        """
        Updates the CSV log of all articles read.
        """
        read_path = HERE.parent.joinpath("data/read.csv").resolve()

        df_stored = pd.read_csv(read_path)
        new_row = {"human_id": df["itemLabel"][0], "wikidata_id": df["item"][0]}
        new_row = pd.DataFrame(new_row, index=[0])
        df_stored = pd.concat([df_stored, new_row], ignore_index=True)

        df_stored = df_stored.drop_duplicates()
        print(df_stored)
        df_stored.to_csv(read_path, index=False)

    wikidata_id = sys.argv[1]

    print("======= Getting title from Wikidata =======")
    df = get_title_df(wikidata_id)
    update_csv(df)

    title = df["itemLabel"][0]

    try:
        publication_date = df["date"][0]

        date_in_dateformat = datetime.strptime(publication_date, "%Y-%m-%dT00:00:00Z")
        publication_date = date_in_dateformat.strftime("%d of %B, %Y")
    except Exception:
        publication_date = "None"
        pass

    try:
        doi = df["doi"][0]
    except Exception:
        doi = ""
        pass

    try:
        text_url = df["url"][0]
    except Exception:
        text_url = ""
        pass

    try:
        arxiv_id = df["arxiv_id"][0]
    except Exception:
        arxiv_id = ""
        pass

    file_path = HERE.parent.joinpath(f"notes/{wikidata_id}").resolve().absolute().as_posix()
    print(file_path)
    print("======= Creating markdown =======")
    create_markdown(file_path, title, publication_date, doi, text_url, arxiv_id)
    update_turtle(wikidata_id)

    print("======= Updating dashboard =======")

    update_path = HERE.joinpath("update_dashboard.py").resolve()
    exec(open(f"{update_path}").read())

    print("======= Done =======")


if __name__ == "__main__":
    wikidata_id = sys.argv[1]
    assert wikidata_id[0] == "Q"
    filename = HERE.parent.joinpath(f"notes/{wikidata_id}.md").resolve()

    if os.path.isfile(filename):
        print("Article has already been read")
    else:
        main()

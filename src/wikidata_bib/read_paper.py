"""
Creates a markdown file for notes from the Wikidata ID.
"""
import os.path
import sys
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import rdflib
from helper import get_title_df
from mdutils.mdutils import MdUtils

HERE = Path(__file__).parent.resolve()


def main():
    """
    Creates a markdown file for notes from the Wikidata ID.
    """
    wikidata_id = sys.argv[1]

    print("======= Getting title from Wikidata =======")
    basic_info_dataframe = get_title_df(wikidata_id)
    update_csv(basic_info_dataframe)
    title = basic_info_dataframe["itemLabel"][0]

    try:
        publication_date = basic_info_dataframe["date"][0]
        date_in_dateformat = datetime.strptime(publication_date, "%Y-%m-%dT00:00:00Z")
        publication_date = date_in_dateformat.strftime("%d of %B, %Y")

    except Exception:
        publication_date = "None"
        pass

    try:
        doi = basic_info_dataframe["doi"][0]
    except Exception:
        doi = ""
        pass

    try:
        text_url = basic_info_dataframe["url"][0]
    except Exception:
        text_url = ""
        pass

    try:
        arxiv_id = basic_info_dataframe["arxiv_id"][0]
    except Exception:
        arxiv_id = ""

    file_path = HERE.parent.joinpath(f"notes/{wikidata_id}.md")

    print("======= Creating markdown =======")
    create_markdown(file_path, title, wikidata_id, publication_date, doi, text_url, arxiv_id)
    update_turtle(wikidata_id)

    print("======= Updating dashboard =======")

    update_path = HERE.joinpath("update_dashboard.py").resolve()
    exec(open(f"{update_path}").read())
    print("======= Done =======")


def create_markdown(
    file_path, title, wikidata_id, publication_date="None", doi="", url="", arxiv_id=""
):
    """
    Creates a markdown file for notes from the Wikidata ID.
    """
    markdown_file = MdUtils(file_name=file_path, title=title)
    print(filename)
    markdown_file.new_line("  [@wikidata:" + wikidata_id + "]")
    markdown_file.new_line()
    if publication_date != "None":
        markdown_file.new_line("Publication date : " + str(publication_date))

    # Reading dates

    markdown_file.new_line()
    markdown_file.new_header(1, "Highlights")
    markdown_file.new_header(1, "Comments")
    markdown_file.new_header(2, "Tags")
    markdown_file.new_header(1, "Links")
    markdown_file.new_line(
        f" * [Scholia Profile](https://scholia.toolforge.org/work/{wikidata_id})"
    )
    markdown_file.new_line(f" * [Wikidata](https://www.wikidata.org/wiki/{wikidata_id})")
    markdown_file.new_line(
        " * [Author Disambiguator](https://author-disambiguator.toolforge.org/"
        f"work_item_oauth.php?id={wikidata_id}"
        "&batch_id=&match=1&author_list_id=&doit=Get+author+links+for+work)"
    )
    if doi != "":
        markdown_file.new_line(f" * [DOI](https://doi.org/{doi})")

    if url != "":
        markdown_file.new_line(f" * [Full text URL]({url})")

    if arxiv_id != "":
        markdown_file.new_line(f" * [arXiv ID](https://arxiv.org/pdf/{arxiv_id}.pdf)")
    markdown_file.new_line()

    markdown_file.new_header(1, "Reading dates")
    reading_date = date.today().isoformat()  # format: YYYY-MM-DD
    markdown_file.new_line(f" * {reading_date}\n")
    file_path.write_text(markdown_file.get_md_text())


def update_turtle(wikidata_id):
    """
    Opens and updates the local RDF database int Turtle format
    that records the articles that have been read.
    """
    g = rdflib.Graph()
    read_ttl_path = HERE.parent.joinpath("data/read.ttl").resolve()
    g.parse(read_ttl_path, format="ttl")
    wb = rdflib.Namespace("https://github.com/lubianat/wikidata_bib/tree/main/")
    g = add_read_today_triple(wikidata_id, g, wb)
    print(g)
    read_ttl_path = HERE.parent.joinpath("data/read.ttl").resolve()
    g.serialize(destination=read_ttl_path, format="turtle")


def add_read_today_triple(wikidata_id, graph, read_in_prefix):
    """
    Adds a triple to the graph stating that the QID was read today.
    """
    wikidata_prefix = rdflib.Namespace("http://www.wikidata.org/entity/")
    today = date.today()
    d1 = today.strftime("+%Y-%m-%dT00:00:00Z/11")
    s = rdflib.term.URIRef(wikidata_prefix + wikidata_id)
    p2 = rdflib.term.URIRef(read_in_prefix + "read_in")
    o2 = rdflib.term.Literal(d1)
    graph.add((s, p2, o2))
    return graph


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


def add_reading_date_to_existing_markdown(file_path):
    # Read in the existing markdown file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Prepare the new reading date
    reading_date = f" * {date.today().isoformat()}\n"

    # Find the lines with "Reading dates" heading and with dates
    reading_dates_index = next((i for i, line in enumerate(lines) if "Reading dates" in line), None)
    dates_indices = [
        i for i, line in enumerate(lines) if line.startswith(" * ") and i > reading_dates_index
    ]

    # Check if the reading date already exists in the file to avoid duplicate dates
    if reading_date in lines:
        print("Today's reading date already exists in the file.")
    else:
        # If "Reading dates" heading is found, append new reading date under this section
        if reading_dates_index is not None:
            if dates_indices:  # if there are already some dates
                lines.insert(
                    dates_indices[-1] + 1, reading_date
                )  # insert new date after the last existing date
            else:  # if there are no dates yet
                lines.insert(
                    reading_dates_index + 1, reading_date
                )  # insert new date right after the section heading
        # If not found, add "Reading dates" heading at the end and append new reading date
        else:
            new_section = [
                "\n# Reading dates\n",
                "  > Reading dates functionality became available on July 24, 2023\n",
                reading_date,
            ]
            lines.extend(new_section)

    # Write the updated lines back to the markdown file
    with open(file_path, "w") as file:
        file.writelines(lines)


if __name__ == "__main__":
    wikidata_id_outer_scope = sys.argv[1]
    assert wikidata_id_outer_scope[0] == "Q"
    filename = HERE.parent.joinpath(f"notes/{wikidata_id_outer_scope}.md").resolve()

    if os.path.isfile(filename):
        print("Article has already been read")
        add_reading_date_to_existing_markdown(filename)
    else:
        main()

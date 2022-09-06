"""
Runs the full Wikidata Bib workflow for a paper.
"""
import os
import webbrowser
from pathlib import Path

import click

from .helper import get_doi_df

HERE = Path(__file__).parent.resolve()


@click.command(name="read")
@click.argument("qid")
@click.option(
    "-d",
    "--download",
    is_flag=True,
    show_default=True,
    default=False,
    help="Downloads and opens the PDF.",
)
def main(qid: str, download: bool):
    """Reads a paper on demand.

    Given the QID for the article, read runs the Wikidata Bib workflow.
    """
    read_paper_path = HERE.joinpath("read_paper.py").resolve()
    os.system(f"python3 {read_paper_path} {qid}")

    doi_df = get_doi_df(qid)
    if doi_df.empty is True:
        print("No DOI found for " + qid + ".")
    else:
        doi_suffix = doi_df["doi"].values[0]
        webbrowser.open(f"https://doi.org/{doi_suffix}")
    if download is True:
        get_pdf_path = HERE.joinpath("get_pdf.py").resolve()
        os.system(f"python3 {get_pdf_path} {qid} unpaywall")

    notes_path = HERE.parent.joinpath(f"notes/{qid}.md").resolve()
    os.system(f'code "{notes_path}"')

    url = (
        "https://author-disambiguator.toolforge.org/"
        f"work_item_oauth.php?id={qid}&batch_id=&match=1"
        "&author_list_id=&doit=Get+author+links+for+work"
    )
    os.system(f"xdg-open {url}")

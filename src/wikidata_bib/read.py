#!/usr/bin/python3

import os
import click
from pathlib import Path

HERE = Path(__file__).parent.resolve()


@click.command(name="read")
@click.argument("qid")
@click.option(
    "-nd",
    "--no-download",
    is_flag=True,
    show_default=True,
    default=False,
    help="Skip the download of a PDF.",
)
def main(qid: str, no_download: bool):
    """Reads a paper on demand.

    Given the QID for the article, read runs the Wikidata Bib workflow.
    """
    read_paper_path = HERE.joinpath("read_paper.py").resolve()
    os.system(f"python3 {read_paper_path} {qid}")

    get_pdf_path = HERE.joinpath("get_pdf.py").resolve()
    if no_download is False:
        os.system(f"python3 {get_pdf_path} {qid} unpaywall")

    notes_path = HERE.parent.joinpath(f"notes/{qid}.md").resolve()
    os.system(f'code "{notes_path}"')

    url = f"https://author-disambiguator.toolforge.org/work_item_oauth.php?id={qid}&batch_id=&match=1&author_list_id=&doit=Get+author+links+for+wor"
    os.system(f"xdg-open {url}")


if __name__ == "__main__":
    main()

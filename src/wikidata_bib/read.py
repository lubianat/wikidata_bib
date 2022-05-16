#!/usr/bin/python3

import os
import sys
import click
from pathlib import Path

HERE = Path(__file__).parent.resolve()


@click.command(name="read")
@click.argument("qid")
@click.option("-nd",
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
    os.system(f"python3 {HERE}/read_paper.py {qid}")
    if no_download == False:
        os.system(f"python3 {HERE}/get_pdf.py {qid} unpaywall")
    os.system(f'code "{HERE}../../notes/{qid}.md"')

    url = f"https://author-disambiguator.toolforge.org/work_item_oauth.php?id={qid}&batch_id=&match=1&author_list_id=&doit=Get+author+links+for+wor"
    os.system(f"xdg-open {url}")


if __name__ == "__main__":
    main()

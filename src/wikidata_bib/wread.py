#!/usr/bin/python3

import os
import sys
import click


@click.command(name="wread")
@click.option("--qid", prompt=True, help="The QID of the paper of interest")
def main(qid: str):
    os.system(f"python3 src/wikidata_bib/read_paper.py {qid}")
    os.system(f"python3 src/wikidata_bib/get_pdf.py {qid} unpaywall")
    os.system(f'code "notes/{qid}.md"')

    url = f"https://author-disambiguator.toolforge.org/work_item_oauth.php?id={qid}&batch_id=&match=1&author_list_id=&doit=Get+author+links+for+wor"
    os.system(f"xdg-open {url}")


if __name__ == "__main__":
    main()

import click

from wikidata_bib import render_tweet, reopen_last

from . import drop_last, get_index, get_qids_from_europe_pmc, pop, push, read, reopen_last, wlog


@click.group()
def cli():
    """Wikidata Bib, a Wikidata-based, CLI-oriented pacakage for reading articles."""


cli.add_command(read.main)
cli.add_command(pop.main)
cli.add_command(wlog.main)
cli.add_command(drop_last.main)
cli.add_command(push.main)
cli.add_command(get_index.main)
cli.add_command(reopen_last.main)
cli.add_command(get_qids_from_europe_pmc.main)
cli.add_command(render_tweet.main)
if __name__ == "__main__":
    cli()

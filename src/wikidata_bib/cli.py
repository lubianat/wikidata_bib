import click

from . import read, pop, wlog, drop_last


@click.group()
def cli():
    """Wikidata Bib, a Wikidata-based, CLI-oriented pacakage for reading articles."""


cli.add_command(read.main)
cli.add_command(pop.main)
cli.add_command(wlog.main)
cli.add_command(drop_last.main)

if __name__ == "__main__":
    cli()

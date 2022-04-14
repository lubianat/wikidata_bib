import click

from . import wread, pop, wlog, drop_last


@click.group()
def cli():
    """Wikidata Bib, a Wikidata-based, CLI-oriented pacakage for reading articles."""


cli.add_command(wread.main)
cli.add_command(pop.main)
cli.add_command(wlog.main)
cli.add_command(drop_last.main)

if __name__ == "__main__":
    cli()

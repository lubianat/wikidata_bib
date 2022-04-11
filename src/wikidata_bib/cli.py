import click

from . import wread, pop, wlog


@click.group()
def cli():
    """PyORCIDator."""


cli.add_command(wread.main)
cli.add_command(pop.main)
cli.add_command(wlog.main)
if __name__ == "__main__":
    cli()

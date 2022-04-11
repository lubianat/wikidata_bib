import click

from . import wread


@click.group()
def cli():
    """PyORCIDator."""


cli.add_command(wread.main)

if __name__ == "__main__":
    cli()

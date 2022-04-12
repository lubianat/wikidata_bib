import click

from . import wread, pop, wlog, drop_last


@click.group()
def cli():
    """PyORCIDator."""


cli.add_command(wread.main)
cli.add_command(pop.main)
cli.add_command(wlog.main)
cli.add_command(drop_last.main)

if __name__ == "__main__":
    cli()

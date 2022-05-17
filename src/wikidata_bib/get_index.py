import os
from pathlib import Path
import click

HERE = Path(__file__).parent.resolve()


@click.command(name="index")
def main():
    """
    Opens index of tags to categorize notes.
    """
    path_to_index = HERE.parent.joinpath("data").joinpath("index.yaml")
    os.system(f"code {path_to_index}")


if __name__ == "__main__":
    main()

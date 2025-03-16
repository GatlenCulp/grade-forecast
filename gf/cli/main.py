"""Main CLI interface for a gf."""

import typer

from gf.cli.interface import interface

app = typer.Typer()


@app.command()
def run() -> None:
    """Run app

    Args:
        name: Name of the person to greet
    """
    interface()


if __name__ == "__main__":
    app()

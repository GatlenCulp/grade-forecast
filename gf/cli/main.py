"""Main CLI entry point for the grade forecast application."""

import typer

from gf.cli.interface import interface

app = typer.Typer(help="Grade Forecast - Track and forecast your university grades")


@app.command()
def run() -> None:
    """Run the Grade Forecast interactive CLI application."""
    interface()


if __name__ == "__main__":
    app()

"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """Pytest Repo Structure."""


if __name__ == "__main__":
    main(prog_name="pytest-repo-structure")  # pragma: no cover

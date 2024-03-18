"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """Pytest Environment."""


if __name__ == "__main__":
    main(prog_name="pytest-environment")  # pragma: no cover

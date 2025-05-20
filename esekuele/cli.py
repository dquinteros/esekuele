import click
from . import __version__
from .generator import generate_sql


@click.command()
@click.option('--engine', default='sqlite', show_default=True, help='SQL engine name')
@click.option('--schema', required=True, help='Schema description')
@click.argument('prompt')
@click.version_option(version=__version__)
def main(engine: str, schema: str, prompt: str) -> None:
    """Generate a SQL query for the given PROMPT."""
    query = generate_sql(engine, schema, prompt)
    click.echo(query)


if __name__ == '__main__':  # pragma: no cover
    main()


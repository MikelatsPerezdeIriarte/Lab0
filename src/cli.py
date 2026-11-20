"""CLI commands for console"""

import ast

import click

from src import preprocessing as pp


@click.group()
def cli():
    """Data processing tools."""


@cli.group()
def clean():
    """Data cleaning functions."""


@clean.command()
@click.argument("values", nargs=-1)
def remove_missing(values):
    """Removes missing values from a list of strings."""
    click.echo(pp.remove_missing(list(values)))


@clean.command()
@click.argument("values", nargs=-1)
@click.option("--fill-value", default=0, help="Value to fill the missing values.")
def fill_missing(values, fill_value):
    """Fills the missing values with a default value (0 by default)."""
    click.echo(pp.fill_missing(list(values), fill_value))


@cli.group()
def numeric():
    """Functions for numeric attributes."""


@numeric.command()
@click.argument("values", nargs=-1, type=float)
@click.option("--new-min", default=0.0, help="New minimum.")
@click.option("--new-max", default=1.0, help="New maximum.")
def normalize(values, new_min, new_max):
    """Normalizes a list of numerical values to the range [new_min, new_max]."""
    click.echo(pp.normalize(list(values), new_min, new_max))


@numeric.command()
@click.argument("values", nargs=-1, type=float)
def standardize(values):
    """Standarizes a list of numerical values (z-score)."""
    click.echo(pp.standardize(list(values)))


@numeric.command()
@click.argument("values", nargs=-1, type=float)
@click.option("--min-val", default=0.0, help="Minimum value.")
@click.option("--max-val", default=1.0, help="Maximum value.")
def clip(values, min_val, max_val):
    """Clips a list of numerical values to the range [min_val, max_val]"""
    click.echo(pp.clip(list(values), min_val, max_val))


@numeric.command()
@click.argument("values", nargs=-1)
def to_integers(values):
    """Converts a list of strings to integers"""
    click.echo(pp.to_integers(list(values)))


@numeric.command()
@click.argument("values", nargs=-1, type=float)
def log_transform(values):
    """Converts a list of numeric values to logarithmic scale"""
    click.echo(pp.log_transform(list(values)))


@cli.group()
def text():
    """Text processing functions."""


@text.command()
@click.argument("value")
def tokenize(value):
    """Tokenizes a text into words selecting only alphanumeric characters and lower-casing words."""
    click.echo(pp.tokenize(value))


@text.command()
@click.argument("value")
def remove_punctuation(value):
    """Removes the punctuation from a text."""
    click.echo(pp.remove_punctuation(value))


@text.command()
@click.argument("value")
@click.option("--stop-words", multiple=True, help="Palabras vacías a eliminar.")
def remove_stopwords(value, stop_words):
    """Removes stopwords from a text."""
    click.echo(pp.remove_stopwords(value, list(stop_words)))


@cli.group()
def struct():
    """Functions for data structures."""


@struct.command()
@click.argument("values", nargs=-1)
@click.option("--seed", type=int, default=None, help="Semilla para reproducibilidad.")
def shuffle(values, seed):
    """Shuffles a list of values with an optional seed."""
    click.echo(pp.shuffle(list(values), seed))


@struct.command()
@click.argument("nested_list")
def flatten(nested_list):
    """Flattens a list of lists."""
    try:
        parsed = ast.literal_eval(nested_list)
    except (ValueError, SyntaxError) as exc:
        raise click.BadParameter("Must be a valid list of lists") from exc
    click.echo(pp.flatten(list(parsed)))


@struct.command()
@click.argument("values", nargs=-1)
def unique(values):
    """Removes duplicates from a list of values."""
    click.echo(pp.remove_duplicates(list(values)))

import click
from .main import main
from typing import List
from database import read_database, DatabaseValidator
from helper import print_validation

@main.command()
@click.option("--source", "-s", default="data/", help='The Directory which contains the stations as JSON files')
def validate(source: str):
    """
    Validate the current database
    """
    database = read_database(source)
    result = DatabaseValidator().validate(database)
    print_validation(result)
    if len(result) > 0:
        exit(1)
    
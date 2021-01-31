import json
import os
import click
from .main import main
from typing import List
from database import read_database, DatabaseStation, StationDatabase, DatabaseRadioStream



@main.command()
@click.option("--source", "-s", default="data/", help='The Directory which contains the stations as JSON files')
@click.option("--name", help='The name of the station which should be created')
@click.option("--image-url", help='The image url of the station which should be created')
@click.option("--stream-url", help='The stream url of the station which should be created')
@click.option("--stream-type", help='The stream type of the station which should be created')
@click.option("--stream-rate", help='The stream rate of the station which should be created')
def add_station(source: str, target: str):
    """
    Create a new station and add it to the database
    """
    pass
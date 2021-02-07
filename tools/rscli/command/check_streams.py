import json
import os
import click
import csv
import uuid
import time
from helper import name_to_filepath, progressbar, validate_stream
from .main import main
from database import read_database, DatabaseStation, StationDatabase, DatabaseRadioStream

@main.command()
@click.option("--source", "-s", default="data/", help='The Directory which contains the stations as JSON files')
def check_streams(source: str):
    """
    Checks if the stream data is correct
    """
    database = read_database(source)
    errors = []
    with progressbar(database.stations, "Stream Check") as stations_bar:
        for station in stations_bar:
            for stream in station.streams:
                errors += validate_stream(stream)
    for error in errors:
        click.echo(error)
    if len(errors)>0:
        exit(1)
    else:
        click.echo("All streams are valid")

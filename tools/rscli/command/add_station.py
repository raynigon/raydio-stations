import json
import os
import click
import uuid
from .main import main
from helper import name_to_filepath
from typing import List
from database import read_database, DatabaseStation, StationDatabase, DatabaseRadioStream


@main.command()
@click.option("--source", "-s", default="data/", help='The Directory which contains the stations as JSON files')
@click.option("--name", help='The name of the station which should be created')
@click.option("--image-url", help='The image url of the station which should be created')
@click.option("--stream-url", help='The stream url of the station which should be created')
@click.option("--stream-type", help='The stream type of the station which should be created')
@click.option("--stream-rate", help='The stream rate of the station which should be created')
@click.option("--country", help='The origin country of the station', default="global")
@click.option("--corporation", help='The broadcasting corporation', default="unknown")
def add_station(source: str, name: str, image_url: str, stream_url: str, stream_type: str, stream_rate: int, country: str, corporation: str):
    """
    Create a new station and add it to the database
    """
    database = read_database(source)
    if name is None:
        name = click.prompt('Station Name')
    if stream_url is None:
        stream_url = click.prompt('Stream Url')
    if stream_type is None:
        stream_type = click.prompt('Stream Type')
    if stream_rate is None:
        stream_rate = click.prompt('Stream Rate', type=int)
    streams = [DatabaseRadioStream(stream_type, stream_rate, stream_url)]
    station = DatabaseStation(str(uuid.uuid4()), name_to_filepath(source, name, country, corporation), name, image_url, streams)
    database.add_station(station)
    database.save()
        
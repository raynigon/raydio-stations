import json
import os
import click
import csv
import uuid
from helper import name_to_filepath
from .main import main
from typing import List
from database import read_database, DatabaseStation, StationDatabase, DatabaseRadioStream

def read_csv(csv_path: str):
    with open(csv_path) as csvfile:
        spamreader = csv.reader(csvfile)
        return [row for row in spamreader]

def row_to_station(source, row):
    if len(row) < 6:
        return None
    country = row[0]
    corporation = row[1]
    image_url = row[2]
    name = row[3]
    rate = row[4]
    stream = row[5]
    stream_type = stream.split(".")[-1]
    if len(row) > 6 and row[6].strip() != "":
        stream_type = row[6]
    stream = DatabaseRadioStream(stream_type, rate, stream)
    station = DatabaseStation(str(uuid.uuid4()), name_to_filepath(source, name, country, corporation), name, image_url, [stream])
    return station

@main.command()
@click.option("--source", "-s", default="data/", help='The Directory which contains the stations as JSON files')
@click.option("--csv", "-c", help='The CSV File which should be used')
def import_csv(source: str, csv: str):
    """
    Import a CSV to the Database
    """
    database = read_database(source)
    if csv is None:
        csv = click.prompt("CSV File")
    data = read_csv(csv)
    for row in data:
        station = row_to_station(source, row)
        if station is None:
            continue
        db_station = database.find_by_stream(station.streams[0].url)
        if db_station is not None:
            continue
        db_station = database.find_by_filepath(station.path)
        if db_station is None:
            database.add_station(station)
            continue
        db_station.add_stream(station.streams[0])
    database.save()




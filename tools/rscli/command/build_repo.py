import click
from .main import main
from typing import List
from database import read_database, StationDatabase, DatabaseValidator
from repository import write_repository, StationRepository, RepositoryBundle, RepositoryStation, WebRadioStream
from helper import print_validation

def _to_repository(db: StationDatabase)->StationRepository:
    stations = []
    for db_station in db.stations:
        station = RepositoryStation(db_station.id, db_station.name, db_station.image_url)
        for db_stream in db_station.streams:
            stream = WebRadioStream(db_stream.stream_type, db_stream.rate, db_stream.url)
            station.streams.append(stream)
        stations.append(station)

    bundle = RepositoryBundle(1, "Europe 1", stations)
    return StationRepository([bundle])

def __validate_database(db: StationDatabase):
    result = DatabaseValidator().validate(db)
    print_validation(result)
    if len(result) > 0:
        exit(1)

@main.command()
@click.option("--source", "-s", default="data/", help='The Directory which contains the stations as JSON files')
@click.option("--target", "-t", default="build/", help='The Directory which will be used to write the repository')
def build_repo(source: str, target: str):
    """
    Build the repository layout from data folder.
    """
    database = read_database(source)
    __validate_database(database)
    repo = _to_repository(database)
    write_repository(repo, target)      
    click.echo(f"[INFO] Created Station Repository in '{target}'")




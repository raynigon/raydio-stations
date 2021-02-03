import json
import os
import click
from .main import main
from typing import List
from database import read_database, DatabaseStation, StationDatabase, DatabaseRadioStream
from repository import StationRepository, RepositoryBundle, RepositoryStation, WebRadioStream, write_repository, RepositoryValidationException


def _to_repository(db: StationDatabase)->StationRepository:
    stations = []
    for db_station in db.stations:
        station = RepositoryStation(db_station.id, db_station.name, db_station.image_url)
        for db_stream in db_station.streams:
            stream = WebRadioStream(db_stream.type, db_stream.rate, db_stream.url)
            station.streams.append(stream)
        stations.append(station)

    bundle = RepositoryBundle(1, "Europe 1", stations)
    return StationRepository([bundle])


@main.command()
@click.option("--source", "-s", default="data/", help='The Directory which contains the stations as JSON files')
@click.option("--target", "-t", default="build/", help='The Directory which will be used to write the repository')
def build_repo(source: str, target: str):
    """
    Build the repository layout from data folder.
    """
    database = read_database(source)
    repo = _to_repository(database)

    try:
        write_repository(repo, target)
    except RepositoryValidationException as ex:
        click.secho("Repository contains errors:", fg='red')
        for error in ex.errors:
            click.secho(error, fg='red')
        exit(1)
    click.echo(f"Created Station Repository in '{target}'")




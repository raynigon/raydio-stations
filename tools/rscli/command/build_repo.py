import json
import os
import click
from .main import main
from typing import List
from repository import StationRepository, RepositoryBundle, RepositoryStation, WebRadioStream, write_repository, RepositoryValidationException


def _read_stations(source: str)->List[RepositoryStation]:
    stations = []
    iterateable = os.walk(source)
    with click.progressbar(iterateable) as it:
        for path,_,files in it:
            for filename in files:
                if not filename.endswith(".json"):
                    continue
                full_path = os.path.join(path, filename)
                with open(full_path) as file:
                    station_dict = json.load(file)
                station = RepositoryStation(station_dict["id"], station_dict["name"], station_dict["imageUrl"])
                for stream_dict in station_dict["streams"]:
                    stream = WebRadioStream(stream_dict["type"], stream_dict["rate"], stream_dict["url"])
                    station.streams.append(stream)
                stations.append(station)
    return stations


@main.command()
@click.option("--source", "-s", default="data/", help='The Directory which contains the stations as JSON files')
@click.option("--target", "-t", default="build/", help='The Directory which will be used to write the repository')
def build_repo(source: str, target: str):
    """
    Build the repository layout from data folder.
    """
    click.echo("This is a CLI built with Click ✨")
    
    stations = _read_stations(source)
    bundle = RepositoryBundle(1, "Europe 1", stations)
    repo = StationRepository([bundle])

    try:
        write_repository(repo, target)
    except RepositoryValidationException as ex:
        click.secho("Repository contains errors:", fg='red')
        for error in ex.errors:
            click.secho(error, fg='red')



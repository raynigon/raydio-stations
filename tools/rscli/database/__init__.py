import os
import json
from .model import *
from .validator import DatabaseValidator

def read_database(source: str)->StationDatabase:
    stations = []
    for path,_,files in os.walk(source):
        for filename in files:
            if not filename.endswith(".json"):
                continue
            full_path = os.path.join(path, filename)
            with open(full_path) as file:
                station_dict = json.load(file)
            station = DatabaseStation.from_dict(station_dict, full_path)
            stations.append(station)
    return StationDatabase(stations)
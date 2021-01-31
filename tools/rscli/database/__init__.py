import os
import json
from .model import *

def read_database(source: str)->StationDatabase:
    stations = []
    for path,_,files in os.walk(source):
        for filename in files:
            if not filename.endswith(".json"):
                continue
            full_path = os.path.join(path, filename)
            with open(full_path) as file:
                station_dict = json.load(file)
            station = DatabaseStation(station_dict["id"], full_path, station_dict["name"], station_dict["imageUrl"])
            for stream_dict in station_dict["streams"]:
                stream = DatabaseRadioStream(stream_dict["type"], stream_dict["rate"], stream_dict["url"])
                station.streams.append(stream)
            stations.append(station)
    return StationDatabase(stations)
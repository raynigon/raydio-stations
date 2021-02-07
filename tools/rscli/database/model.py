from __future__ import annotations
from typing import List, Dict, Any
import os
import json

def empty_callback():
    raise Exception("Empty callback was called")

class DatabaseRadioStream:

    def __init__(self, stream_type: str, rate: int, url: str):
        self.__type = stream_type
        self.__rate = int(rate)
        self.__url = url
        self.edit_callback = empty_callback

    def edited(self):
        self.__edited = True

    def saved(self):
        self.__edited = False

    @property
    def stream_type(self):
        return self.__type

    @property
    def rate(self):
        return self.__rate

    @property
    def url(self):
        return self.__url

    @stream_type.setter
    def stream_type(self, value):
        self.__type = value
        self.edit_callback()
    
    @stream_type.setter
    def stream_type(self, value):
        self.__type = value
        self.edit_callback()
    
    @rate.setter
    def rate(self, value):
        self.__rate = value
        self.edit_callback()
    
    @url.setter
    def url(self, value):
        self.__url = value
        self.edit_callback()

    def to_dict(self):
        return {
            "type": self.__type,
            "rate": self.__rate,
            "url": self.__url
        }

    @classmethod
    def from_dict(cls, stream_dict: Dict[str, Any])->DatabaseStation:
        return DatabaseRadioStream(stream_dict["type"], stream_dict["rate"], stream_dict["url"])


class DatabaseStation:

    def __init__(self, identifier: str, path: str, name: str, image_url: str, streams: List[DatabaseRadioStream] = []):
        self.__id = identifier
        self.__path = path
        self.__name = name
        self.__image_url = image_url
        self.__streams = streams
        self.__edited = False
        for stream in self.__streams:
            stream.edit_callback = self.edited

    def edited(self):
        self.__edited = True

    def modified(self)->bool:
        return self.__edited

    def add_stream(self, stream: DatabaseRadioStream):
        stream.edit_callback = self.edited
        self.__streams.append(stream)
        self.edited()

    def remove_stream(self, stream: DatabaseRadioStream):
        self.__streams.remove(stream)
        self.edited()

    @property
    def id(self):
        return self.__id

    @property
    def path(self):
        return self.__path

    @property
    def name(self):
        return self.__name

    @property
    def image_url(self):
        return self.__image_url

    @property
    def streams(self):
        return self.__streams.copy()

    @name.setter
    def name(self, value):
        self.__name = value
        self.edited()
    
    @image_url.setter
    def image_url(self, value):
        self.__type = value
        self.edited()

    def save(self):
        folder = os.path.dirname(self.path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(self.path, "w") as file:
            json.dump(self.to_dict(), file, indent=4)
        self.__edited = False

    def to_dict(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "imageUrl": self.__image_url,
            "streams": list(map(lambda x: x.to_dict(), self.__streams))
        }

    @classmethod
    def from_dict(cls, station_dict: Dict[str, Any], full_path: str)->DatabaseStation:
        streams = []
        for stream_dict in station_dict["streams"]:
            streams.append(DatabaseRadioStream.from_dict(stream_dict))
        return DatabaseStation(station_dict["id"], full_path, station_dict["name"], station_dict["imageUrl"], streams)


class StationDatabase:

    def __init__(self, stations: List[DatabaseStation] = []):
        self.__stations = stations
        self.__station_by_id = {}
        self.__station_by_path = {}
        self.__station_by_stream = {}
        self.__deleted_stations = []
        self.rebuild_index()

    def __index_station(self, station):
        self.__station_by_id[station.id] = station
        self.__station_by_path[station.path] = station
        for stream in station.streams:
            self.__station_by_stream[stream.url] = station

    def rebuild_index(self):
        """
        Recreates all indices from scratch
        """
        self.__station_by_id = {}
        self.__station_by_path = {}
        for station in self.__stations:
            self.__index_station(station)

    def add_station(self, station: DatabaseStation):
        if self.find_by_id(station.id):
            raise Exception(f"A Station with the id '{station.id}' already exists")
        self.__stations.append(station)
        self.__index_station(station)
        station.edited()

    def delete_station(self, station: DatabaseStation):
        self.__stations.remove(station)
        del self.__station_by_id[station.id]
        del self.__station_by_path[station.path]
        self.__deleted_stations.add(station)

    def find_by_id(self, station_id)->DatabaseStation:
        if station_id not in self.__station_by_id.keys():
            return None
        return self.__station_by_id[station_id]

    def find_by_filepath(self, filepath)->DatabaseStation:
        if filepath not in self.__station_by_path.keys():
            return None
        return self.__station_by_path[filepath]

    def find_by_stream(self, stream)->DatabaseStation:
        if stream not in self.__station_by_stream.keys():
            return None
        return self.__station_by_stream[stream]

    @property
    def stations(self):
        return self.__stations.copy()

    def save(self):
        for station in self.__deleted_stations:
            os.remove(station.path)
        self.__deleted_stations.clear()
        for station in self.__stations:
            if not station.modified():
                continue
            station.save()

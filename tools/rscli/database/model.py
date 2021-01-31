from typing import List

def empty_callback():
    raise Exception("Empty callback was called")

class DatabaseRadioStream:

    def __init__(self, type: str, rate: int, url: str):
        self.__type = type
        self.__rate = rate
        self.__url = url
        self.edit_callback = empty_callback

    @property
    def type(self):
        return self.__type

    @property
    def rate(self):
        return self.__rate

    @property
    def url(self):
        return self.__url

    @type.setter
    def type(self, value):
        self.__type = value
        self.edit_callback()
    
    @type.setter
    def type(self, value):
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


class StationDatabase:

    def __init__(self, stations: List[DatabaseStation] = []):
        self.__stations = stations
        self.__station_by_id = {}
        self.__station_by_path = {}
        self.rebuild_index()

    def rebuild_index(self):
        """
        Recreates all indices from scratch
        """
        self.__station_by_id = {}
        self.__station_by_path = {}
        for station in self.__stations:
            self.__station_by_id[station.id] = station
            self.__station_by_path[station.path] = station

    def add_station(self, station: DatabaseStation):
        if self.find_by_id(station.id):
            raise Exception(f"A Station with the id '{station.id}' already exists")
        self.__stations.append(station)
        self.__station_by_id[station.id] = station
        self.__station_by_path[station.path] = station

    def delete_station(self, station: DatabaseStation):
        self.__stations.remove(station)
        del self.__station_by_id[station.id]
        del self.__station_by_path[station.path]

    def find_by_id(self, station_id)->DatabaseStation:
        if station_id not in self.__station_by_id.keys():
            return None
        return self.__station_by_id[station_id]

    def find_by_filepath(self, filepath)->DatabaseStation:
        if filepath not in self.__station_by_path.keys():
            return None
        return self.__station_by_path[filepath]

    @property
    def stations(self):
        return self.__stations.copy()

from io import TextIOBase
from typing import List, Dict, Any

class WebRadioStream:

    def __init__(self, stream_type: str, rate: int, url: str):
        self.stream_type = stream_type
        self.rate = rate
        self.url = url

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.stream_type,
            "rate": self.rate,
            "url": self.url
        }

class RepositoryStation:

    def __init__(self, id: str, name: str, imageUrl: str, streams: List[WebRadioStream] = []):
        self.id = id
        self.name = name
        self.imageUrl = imageUrl
        self.streams = streams

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "imageUrl": self.imageUrl,
            "streams": list(map(lambda x: x.to_dict(), self.streams))
        }

class RepositoryBundle:

    def __init__(self, version: int, name: str, stations: List[RepositoryStation] = []):
        self.version = version
        self.name = name
        self.stations = stations

    def identifier(self)->str:
        return self.name.lower().replace(" ", "-")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "name": self.name,
            "stations": list(map(lambda x: x.to_dict(), self.stations))
        }


class StationRepository:

    def __init__(self, bundles: List[RepositoryBundle], version: int = 1, active: bool = True):
        self.version = version
        self.active = active
        self.bundles = bundles

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "active" : self.active,
            "bundles": self.__bundles_meta_data()
        }
    
    def __bundles_meta_data(self):
        result = []
        for bundle in self.bundles:
            result.append({
                "id"     : bundle.identifier(),
                "name"   : bundle.name,
                "version": bundle.version,
            })
        return result

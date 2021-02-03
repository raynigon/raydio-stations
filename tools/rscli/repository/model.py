from io import TextIOBase
from typing import List, Dict, Any

ALLOWED_STREAM_TYPES = ["mp3", "aac"]
MINIMUM_STREAM_RATE = 32
MAXIMUM_STREAM_RATE = 512

class WebRadioStream:

    def __init__(self, type: str, rate: int, url: str):
        self.type = type
        self.rate = rate
        self.url = url

    def validate(self) -> List[str]:
        result = []
        if not isinstance(self.type, str):
            result.append(
                f"WebRadioStream version is not a string (got: {self.type})")
        if self.type not in ALLOWED_STREAM_TYPES:
            result.append(
                f"WebRadioStream type is not allowed (got: {self.type}, expected one of: {', '.join(ALLOWED_STREAM_TYPES)})")
        if not isinstance(self.rate, int):
            result.append(
                f"WebRadioStream rate is not an int (got: {self.rate})")
        elif self.rate <= MINIMUM_STREAM_RATE or self.rate >= MAXIMUM_STREAM_RATE:
            result.append(
                f"WebRadioStream rate is outside of allowed range (got: {self.rate}, allowed range: {MINIMUM_STREAM_RATE}-{MAXIMUM_STREAM_RATE} kbit/s)")
        if not isinstance(self.url, str):
            result.append(
                f"WebRadioStream url is not a string (got: {self.url})")
        elif not self.url.startswith("http"):
            result.append(
                f"WebRadioStream url has to be a http/https url (got: {self.url})")
        return result

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "rate": self.rate,
            "url": self.url
        }

class RepositoryStation:

    def __init__(self, id: str, name: str, imageUrl: str, streams: List[WebRadioStream] = []):
        self.id = id
        self.name = name
        self.imageUrl = imageUrl
        self.streams = streams

    def validate(self) -> List[str]:
        result = []
        if not isinstance(self.id, str):
            result.append(
                f"RepositoryStation id is not a string (got: {self.id})")
        if not isinstance(self.name, str):
            result.append(
                f"RepositoryStation name is not a string (got: {self.name})")
        if self.imageUrl is None:
            result.append(
                f"RepositoryStation ({self.name}) imageUrl is missing")
        elif not self.imageUrl is not None and isinstance(self.imageUrl, str):
            result.append(
                f"RepositoryStation ({self.name}) imageUrl is not a string (got: {self.imageUrl})")
        for stream in self.streams:
            result.extend(
                map(lambda x: f"{self.name} -> {x}", stream.validate()))
        return result

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

    def validate(self) -> List[str]:
        result = []
        if not isinstance(self.version, int):
            result.append(
                f"RepositoryBundle version is not an integer (got: {self.version})")
        if not isinstance(self.name, str):
            result.append(
                f"RepositoryBundle name is not a string (got: {self.name})")
        if self.name == "":
            result.append(
                f"RepositoryBundle name is empty")
        for station in self.stations:
            result.extend(
                map(lambda x: f"{self.name} -> {x}", station.validate()))
        return result

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

    def validate(self) -> List[str]:
        result = []
        if not isinstance(self.version, int):
            result.append(
                f"StationRepository version is not an integer (got: {self.version})")
        if not isinstance(self.active, bool):
            result.append(
                f"StationRepository active is not a boolean (got: {self.active})")
        for bundle in self.bundles:
            result.extend(bundle.validate())
        return result

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

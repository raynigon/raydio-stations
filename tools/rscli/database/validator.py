from .model import *
from typing import List

ALLOWED_STREAM_TYPES = ["mp3", "aac", "m3u"]
MINIMUM_STREAM_RATE = 32
MAXIMUM_STREAM_RATE = 512


class DatabaseValidator:

    def __init__(self):
        pass

    def validate(self, database: StationDatabase)->List[str]:
        result = self.__validate_database(database)
        # Unable to verify stations, if database is broken
        if len(result) > 0:
            return result
        for station in database.stations:
            result += self.__validate_station(station)
        # Unable to verify streams, if station is broken
        if len(result) > 0:
            return result
        for station in database.stations:
            for stream in station.streams:
                result += self.__validate_stream(stream, station.name)
        return result

    def __validate_database(self, database: StationDatabase) -> List[str]:
        result = []
        # TODO verify version number
        return result


    def __validate_station(self, station: DatabaseStation) -> List[str]:
        result = []
        if not isinstance(station.id, str):
            result.append(
                f"DatabaseStation id is not a string (got: {station.id})")
        if not isinstance(station.name, str):
            result.append(
                f"DatabaseStation name is not a string (got: {station.name})")
        if station.image_url is None:
            result.append(
                f"DatabaseStation ({station.name}) imageUrl is missing")
        elif not station.image_url is not None and isinstance(station.image_url, str):
            result.append(
                f"DatabaseStation ({station.name}) imageUrl is not a string (got: {station.image_url})")
        return result

    def __validate_stream(self, stream: DatabaseRadioStream, breadcrumbs: str) -> List[str]:
        result = []
        if not isinstance(stream.stream_type, str):
            result.append(
                f"WebRadioStream version is not a string (got: {stream.stream_type})")
        if stream.stream_type not in ALLOWED_STREAM_TYPES:
            result.append(
                f"WebRadioStream type is not allowed (got: {stream.stream_type}, expected one of: {', '.join(ALLOWED_STREAM_TYPES)})")
        if not isinstance(stream.rate, int):
            result.append(
                f"WebRadioStream rate is not an int (got: {stream.rate})")
        elif stream.rate < MINIMUM_STREAM_RATE or stream.rate > MAXIMUM_STREAM_RATE:
            result.append(
                f"WebRadioStream rate is outside of allowed range (got: {stream.rate}, allowed range: {MINIMUM_STREAM_RATE}-{MAXIMUM_STREAM_RATE} kbit/s)")
        if not isinstance(stream.url, str):
            result.append(
                f"WebRadioStream url is not a string (got: {stream.url})")
        elif not stream.url.startswith("http"):
            result.append(
                f"WebRadioStream url has to be a http/https url (got: {stream.url})")
        return list(map(lambda x: f"{breadcrumbs} -> {x}",result))

class ValidationException(Exception):

    def __init__(self, errors: List[str]):
        super().__init__(self, "Station Database contains errors")
        self.errors = errors
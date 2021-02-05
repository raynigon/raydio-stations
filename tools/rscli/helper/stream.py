from database import DatabaseRadioStream
from typing import List
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import eyed3


class StreamInfo:

    def __init__(self, url: str, bit_rate: int, stream_type: str, station_name: str, station_description: str, station_url: str, station_genre: str):
        self.url = url
        self.bit_rate = bit_rate
        self.stream_type = stream_type,
        self.station_name = station_name
        self.station_description = station_description
        self.station_url = station_url
        self.station_genre = station_genre

def generate_mp3_stream_info(stream: DatabaseRadioStream)->StreamInfo:
    response = urlopen(stream.url)
    station_name = None
    station_description = None
    station_url = None
    station_genre = None
    for key in list(response.headers):
        if not key.startswith("icy"):
            continue
        if key.lower() == "icy-name":
            station_name = response.headers["icy-name"]
        if key.lower() == "icy-description":
            station_description = response.headers["icy-description"]
        if key.lower() == "icy-url":
            station_url = response.headers["icy-url"]
        if key.lower() == "icy-genre":
            station_genre = response.headers["icy-genre"]
    with NamedTemporaryFile(suffix=".mp3") as tmp_file:
        CHUNK = 16 * 1024
        with open(tmp_file.name, 'wb') as f:
            i = 0
            while i < 10:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)
                i += 1
        mp3_stream = eyed3.load(tmp_file.name)
        bit_rate = int(mp3_stream.info.bit_rate[1])
    return StreamInfo(stream.url, bit_rate, "mp3", station_name, station_description, station_url, station_genre)

def validate_stream(stream: DatabaseRadioStream) -> List[str]:
    if stream.type != "mp3":
        return []
    try:
        stream_info = generate_mp3_stream_info(stream)
    except Exception as ex:
        return [f"Unable to read Stream Information for {stream.url}"+str(ex)]
    if stream_info.bit_rate != int(stream.rate):
        return [f"{stream.url} differs in bit rate, expected {stream.rate} actual {bit_rate}"]
    return []

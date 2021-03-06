import os
from .stream import StreamInfo, validate_stream, generate_mp3_stream_info
from .progressbar import progressbar
from .print_validation import print_validation

def __clean_name(name: str):
    name = name.lower()\
        .replace(" ", "-")\
        .replace(",", "_")\
        .replace("ü","ue")\
        .replace("ä","ae")\
        .replace("ö","oe")\
        .replace("(","")\
        .replace(")","")
    while "--" in name:
        name = name.replace("--", "-")
    return name

def name_to_filepath(source: str, name: str, country: str, corporation: str):
    base = os.path.join(source, "countries", __clean_name(country), __clean_name(corporation))
    filename = __clean_name(name)
    return os.path.join(base, f"{filename}.json")
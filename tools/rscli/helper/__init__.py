import os

def name_to_filepath(source: str, name: str, country: str, corporation: str):
    base = os.path.join(source, "countries", country.lower(), corporation.lower())
    filename = name.lower()\
        .replace(" ", "-")\
        .replace(",", "_")\
        .replace("ü","ue")\
        .replace("ä","ae")\
        .replace("ö","oe")\
        .replace("(","")\
        .replace(")","")
    return os.path.join(base, f"{filename}.json")
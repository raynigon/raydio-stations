import uuid
import json
import os

country = "de"
container = "br"
name = input("Station Name:")
stream = input("Stream Url:")

filename = name.lower().replace(" ", "-").replace("ü","ue").replace("ä","ae").replace("ö","oe").replace("(","").replace(")","")+".json"
with open(os.path.join("countries", country, container, filename), "w") as file:
    json.dump({
        "id": str(uuid.uuid4()),
        "name": name,
        "imageUrl": None,
        "streams": [{
            "type": "mp3",
            "rate": 128,
            "url": stream
        }]
    }, file, indent=4) 
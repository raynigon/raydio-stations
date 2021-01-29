import json
import os

def check_station(station):
    return True

stations = []
for path,_,files in os.walk("countries"):
    for filename in files:
        if not filename.endswith(".json"):
            continue
        full_path = os.path.join(path, filename)
        with open(full_path) as file:
            station = json.load(file)
        if not check_station(station):
            continue
        stations.append(station)

bundle = {
    "version": 1,
    "name": "Europe",
    "stations": stations
}

if not os.path.exists("build/bundles"):
    os.makedirs("build/bundles/")
with open("build/bundles/europe-1.json", "w") as file:
    json.dump(bundle, file)
with open("build/index.json", "w") as file:
    json.dump({
        "version": 1,
        "active" : True,
        "bundles": [
            {
                "id"     : "europe-1",
                "name"   : bundle["name"],
                "version": bundle["version"],
            }
        ]            
    }, file)
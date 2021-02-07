import csv

with open('stations.csv') as csvfile:
    spamreader = csv.reader(csvfile)
    coporation = None
    coporation_link = None
    with open('stations_clean.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(["country", "coporation", "coporation link", "station", "streams"])
        for row in spamreader:
            if row[0] != "" and (row[1] is None or row[1].strip() == "" or not row[1].strip().startswith("http")):
                coporation = row[0]
                coporation_link = row[2]
                continue
            if row[1] == "":
                continue
            station = row[0]
            if station.startswith("—"):
                station = coporation + " - " + station.replace("—", "").strip()
            streams = [url.strip() for url in row[1].split(",")]
            for stream in streams:
                spamwriter.writerow(["de", coporation, coporation_link, station, stream])
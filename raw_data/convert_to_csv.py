import xml.etree.ElementTree as ET
import csv

def clean(cell):
    if cell is None:
        return None
    return cell.replace("\n", "").strip()

def extract(td):
    if td.tag == "a" and td.text == "www":
        return td.attrib["href"]
    text = clean(td.text)
    if text is not None and text != "":
        return clean(td.text)
    for item in td:
        value = extract(item)
        if value is not None:
            return value
    return None

def is_empty(cells):
    for cell in cells:
        if cell is None:
            continue
        if cell == "":
            continue
        if cell.strip() == "":
            continue
        return False
    return True

def main():
    root = ET.parse('data.xml').getroot()
    with open('stations.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        for tr in root.find("tbody"):
            cells = [extract(td) for td in tr]
            if is_empty(cells):
                continue
            spamwriter.writerow(cells)
    

main()
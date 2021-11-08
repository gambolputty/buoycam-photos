from pathlib import Path

import requests
from fastkml import kml

STATIONS_KML_FILE_URL = 'https://www.ndbc.noaa.gov/kml/buoycams_as_kml.php' # is inside https://www.ndbc.noaa.gov/kml/buoycams.kml
STATIONS_KML_FILE_PATH = Path('buoycam_photos/tmp/stations.kml')
STATIONS_NAMES_FILE_PATH = Path('buoycam_photos/output/stations.txt')

def parse_stations(kml_document):
    placemarks = list(list(list(kml_document.features())[0].features())[0].features())
    result = []

    for placemark in placemarks:
        result.append(placemark.name)

    return result

def get_stations():
    # download latest station file
    # open in binary mode
    with open(STATIONS_KML_FILE_PATH, 'w+b') as file:
        # get request
        response = requests.get(STATIONS_KML_FILE_URL)
        # write to file
        file.write(response.content)

    # read kml file
    with open(STATIONS_KML_FILE_PATH, 'rt', encoding='utf-8') as file:
        doc=file.read()

    # parse stations
    k = kml.KML()
    k.from_string(doc.encode('utf-8')) # fix encoding error https://github.com/cleder/fastkml/issues/57
    stations = parse_stations(k)

    # write csv
    with open(STATIONS_NAMES_FILE_PATH, 'w') as file:
        file.write(','.join(stations))
        print(f'Saved {len(stations)} stations to csv file')

    return True
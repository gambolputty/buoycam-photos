from typing import List

import requests
from fastkml import kml

STATIONS_KML_FILE_URL = 'https://www.ndbc.noaa.gov/kml/buoycams_as_kml.php' # is inside https://www.ndbc.noaa.gov/kml/buoycams.kml

def parse_stations(kml_document: kml.KML) -> List[str]:
    placemarks: List[kml.Placemark] = list(list(list(kml_document.features())[0].features())[0].features())
    return [placemark.name for placemark in placemarks]

def get_stations() -> List[str]:
    # download latest station file content
    response = requests.get(STATIONS_KML_FILE_URL)
    doc = response.content

    # parse stations
    k = kml.KML()
    k.from_string(doc)
    stations = parse_stations(k)

    return stations

if __name__ == '__main__':
    get_stations()
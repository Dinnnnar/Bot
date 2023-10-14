from urllib.request import urlopen
from dataclasses import dataclass
import json
from geopy.geocoders import Nominatim


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def get_coordinates_for_city(city: str) -> Coordinates:
    geolocator = Nominatim(user_agent="Tester")
    location = geolocator.geocode(city)
    return Coordinates(latitude=location.latitude, longitude=location.longitude)



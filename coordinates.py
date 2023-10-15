from dataclasses import dataclass
from geopy.geocoders import Nominatim
import geonamescache
import re

gc = geonamescache.GeonamesCache()


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def get_coordinates_for_city(city: str) -> Coordinates:
    if is_valid_city(city):
        geolocator = Nominatim(user_agent="Tester")
        location = geolocator.geocode(city)
        return Coordinates(latitude=location.latitude, longitude=location.longitude)
    raise Exception("Введите название города")


async def is_valid_city(city):
    cities = gc.get_cities()
    city_names = [city_data['name'] for city_data in cities.values()]
    return city in city_names

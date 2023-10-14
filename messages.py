from coordinates import get_coordinates_for_city, Coordinates
from api_services import get_weather


def weather_for_city(city: str):
    wthr = get_weather(get_coordinates_for_city(city))
    return wthr


def weather(loc: Coordinates):
    wthr = get_weather(loc)
    return wthr

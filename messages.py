from coordinates import  get_coordinates_for_city
from api_services import get_weather


def weather_for_city(city: str) -> str:
    wthr = get_weather(get_coordinates_for_city(city))
    return wthr

def weather(lat: int, log: int) -> str:
    wthr = get_weather(lat, log)
    return wthr

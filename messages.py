from coordinates import  get_coordinates_for_city
from api_services import get_weather


def weather_for_city(city: str) -> str:
    """Returns a message about the temperature and weather description"""
    wthr = get_weather(get_coordinates_for_city(city))
    return wthr

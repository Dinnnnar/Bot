from typing import Literal, TypeAlias
from urllib.request import urlopen
from dataclasses import dataclass
import json

from coordinates import Coordinates

Celsius: TypeAlias = float
WEATHER_API_KEY = 'b9e15db53ab5f2d24c1dce7f4ce49632'
CURRENT_WEATHER_API_CALL = (
        'https://api.openweathermap.org/data/2.5/weather?'
        'lat={latitude}&lon={longitude}&'
        'appid=' + WEATHER_API_KEY + '&units=metric'
)


@dataclass(slots=True, frozen=True)
class Weather:
    location: str
    temperature: Celsius
    temperature_feeling: Celsius
    description: str


def get_weather(coordinates=Coordinates) -> Weather:
    """Requests the weather in OpenWeather API and returns it"""
    longitude = coordinates.longitude
    latitude = coordinates.latitude
    url = CURRENT_WEATHER_API_CALL.format(latitude=latitude, longitude=longitude)
    openweather_response = urlopen(url).read()
    openweather_dict = json.loads(openweather_response)
    weather = Weather(
        location=openweather_dict['name'],
        temperature=openweather_dict['main']['temp'],
        temperature_feeling=openweather_dict['main']['feels_like'],
        description=str(openweather_dict['weather'][0]['description']).capitalize(),
    )
    return weather




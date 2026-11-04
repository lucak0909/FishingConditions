"""Shared weather-fetching utilities used by the CLI, GUI and Lure Helper."""

import os

import requests

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def _load_dotenv():
    """Pull KEY=VALUE pairs from the repo-root .env file into the environment, if present."""
    package_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(package_dir)
    env_path = os.path.join(repo_root, ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()
API_KEY = os.environ.get("OPENWEATHER_API_KEY")


def get_weather_data(location):
    """Fetch current weather data from OpenWeatherMap for a location (e.g. 'Dublin,IE')."""
    if not API_KEY:
        raise RuntimeError(
            "No OpenWeatherMap API key found. Set the OPENWEATHER_API_KEY environment "
            "variable, or copy .env.example to .env and fill it in."
        )

    params = {"q": location, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise ValueError("City not found. Please check your spelling.")
    else:
        raise RuntimeError(f"Failed to fetch weather data: {response.status_code}, {response.text}")


def parse_weather_data(data):
    """Extract the fields the rest of the app cares about from a raw OpenWeatherMap response."""
    from datetime import datetime

    return {
        "temperature": data["main"]["temp"],
        "air_pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"] * 3.6,  # m/s -> km/h
        "cloud_cover": data["clouds"]["all"],
        "precipitation": data.get("rain", {}).get("1h", 0),  # mm
        "precipitation_type": "Rain" if "rain" in data else "None",
        "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).time(),
        "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).time(),
        "description": data["weather"][0]["description"],
    }


def classify_weather_tags(description, wind_speed_kmh):
    """Turn a free-text weather description + wind speed into a set of lure-matching tags."""
    desc = description.lower()
    tags = set()

    if "clear" in desc or "sun" in desc:
        tags.add("clear")
    if "cloud" in desc or "overcast" in desc:
        tags.add("overcast")
    if "rain" in desc or "drizzle" in desc or "storm" in desc or "thunder" in desc:
        tags.add("rain")
    if wind_speed_kmh is not None and wind_speed_kmh >= 20:
        tags.add("windy")

    if not tags:
        tags.add("overcast")

    return tags

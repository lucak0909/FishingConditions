import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import csv
import pandas as pd

API_KEY = "2fd4c84ae5dc94f364025a03e86b7926"  # Replace with your API key
LOCATION = "Limerick,IE"  # Replace with desired location
fileName = "Conditions.csv"


def get_weather_data(location):
    """Fetch current weather data from OpenWeatherMap."""
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"  # For temperature in Celsius
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code}, {response.text}")


def parse_weather_data(data):
    """Extract relevant weather data."""
    temperature = data["main"]["temp"]
    air_pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"] * 3.6  # Convert from m/s to km/h
    cloud_cover = data["clouds"]["all"]
    precipitation = data.get("rain", {}).get("1h", 0)  # mm
    precipitation_type = "Rain" if "rain" in data else "None"
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).time()
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).time()

    return {
        "temperature": temperature,
        "air_pressure": air_pressure,
        "wind_speed": wind_speed,
        "cloud_cover": cloud_cover,
        "precipitation": precipitation,
        "precipitation_type": precipitation_type,
        "sunrise": sunrise,
        "sunset": sunset
    }


def fishing_conditions(
        temperature, air_pressure, wind_speed, cloud_cover,
        precipitation, precipitation_type, sunrise, sunset
):
    fish_preferences = {
        "Pike": {
            "temperature": (10, 20),  # °C
            "air_pressure": (1010, 1030),  # hPa
            "wind_speed": (0, 15),  # km/h
            "cloud_cover": (20, 80),  # percentage
            "precipitation": (0, 5),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Perch": {
            "temperature": (15, 25),  # °C
            "air_pressure": (1015, 1025),  # hPa
            "wind_speed": (0, 10),  # km/h
            "cloud_cover": (10, 70),  # percentage
            "precipitation": (0, 3),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Brown Trout": {
            "temperature": (8, 16),  # °C
            "air_pressure": (1010, 1025),  # hPa
            "wind_speed": (0, 12),  # km/h
            "cloud_cover": (30, 90),  # percentage
            "precipitation": (0, 8),  # mm
            "precipitation_type": ["None", "Rain", "Drizzle"]
        },
        "Atlantic Salmon": {
            "temperature": (5, 15),  # °C
            "air_pressure": (1010, 1020),  # hPa
            "wind_speed": (0, 15),  # km/h
            "cloud_cover": (30, 100),  # percentage
            "precipitation": (0, 10),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Roach": {
            "temperature": (12, 22),  # °C
            "air_pressure": (1010, 1030),  # hPa
            "wind_speed": (0, 10),  # km/h
            "cloud_cover": (10, 60),  # percentage
            "precipitation": (0, 4),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Bream": {
            "temperature": (12, 22),  # °C
            "air_pressure": (1012, 1028),  # hPa
            "wind_speed": (0, 12),  # km/h
            "cloud_cover": (20, 70),  # percentage
            "precipitation": (0, 5),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Rudd": {
            "temperature": (15, 25),  # °C
            "air_pressure": (1010, 1030),  # hPa
            "wind_speed": (0, 8),  # km/h
            "cloud_cover": (10, 50),  # percentage
            "precipitation": (0, 2),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Tench": {
            "temperature": (16, 24),  # °C
            "air_pressure": (1010, 1028),  # hPa
            "wind_speed": (0, 10),  # km/h
            "cloud_cover": (15, 60),  # percentage
            "precipitation": (0, 3),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Eel": {
            "temperature": (10, 20),  # °C
            "air_pressure": (1010, 1025),  # hPa
            "wind_speed": (0, 12),  # km/h
            "cloud_cover": (30, 80),  # percentage
            "precipitation": (0, 5),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Dace": {
            "temperature": (12, 20),  # °C
            "air_pressure": (1010, 1025),  # hPa
            "wind_speed": (0, 10),  # km/h
            "cloud_cover": (10, 60),  # percentage
            "precipitation": (0, 4),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Chub": {
            "temperature": (10, 20),  # °C
            "air_pressure": (1010, 1025),  # hPa
            "wind_speed": (0, 15),  # km/h
            "cloud_cover": (20, 80),  # percentage
            "precipitation": (0, 6),  # mm
            "precipitation_type": ["None", "Rain"]
        },
        "Gudgeon": {
            "temperature": (10, 20),  # °C
            "air_pressure": (1010, 1030),  # hPa
            "wind_speed": (0, 8),  # km/h
            "cloud_cover": (20, 70),  # percentage
            "precipitation": (0, 2),  # mm
            "precipitation_type": ["None", "Rain"]
        }
    }

    def calculate_score(value, optimal_range, max_score=10):
        if optimal_range[0] <= value <= optimal_range[1]:
            return max_score
        elif value < optimal_range[0]:
            return max(0, max_score - (optimal_range[0] - value))
        else:
            return max(0, max_score - (value - optimal_range[1]))

    now = datetime.now()
    is_daytime = sunrise <= now.time() <= sunset

    results = {}
    for fish, prefs in fish_preferences.items():
        scores = [
            calculate_score(temperature, prefs["temperature"]),
            calculate_score(air_pressure, prefs["air_pressure"]),
            calculate_score(wind_speed, prefs["wind_speed"]),
            calculate_score(cloud_cover, prefs["cloud_cover"]),
            calculate_score(precipitation, prefs["precipitation"]),
            10 if precipitation_type in prefs["precipitation_type"] else 0,
            10 if is_daytime else 0
        ]
        results[fish] = sum(scores) / len(scores)

    return results


if __name__ == "__main__":
    try:
        weather_data = get_weather_data(LOCATION)
        parsed_data = parse_weather_data(weather_data)
        quality = fishing_conditions(**parsed_data)

        print(f"Fishing conditions for {LOCATION} on {datetime.now().strftime('%d/%m/%Y')}:")
        for fish, score in quality.items():
            print(f"{fish}: {score:.1f}/10")

        # Write the data to the CSV file (overwrites existing data)
        with open("Conditions.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Fish", "Score"])  # Write header row
            for fish, score in quality.items():
                now = datetime.now()
                writer.writerow([fish, f"{score:.1f}"])

        try:
            df = pd.read_csv(fileName)  # Read the CSV into a pandas DataFrame
        except FileNotFoundError:
            print(f"Error: File not found at '{fileName}'. Please check the path.")
            exit()

        # Create the bar graph
        plt.bar(df['Fish'], df['Score'])

        # Add labels and title
        plt.xlabel("Categories")
        plt.ylabel("Values")
        plt.title("Fishing Conditions in " + LOCATION)

        # Display the graph
        plt.show()

    except Exception as e:
        print(f"Error: {e}")

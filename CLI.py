import requests
from datetime import datetime
import matplotlib.pyplot as plt
import csv
import pandas as pd
import time
import preferences

API_KEY = "2fd4c84ae5dc94f364025a03e86b7926"  # Replace with your API key
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
    elif response.status_code == 404:  # City not found
        raise ValueError("City not found. Please check your spelling.")
    else:
        raise Exception(f"\nFailed to fetch weather data: {response.status_code}, {response.text}")

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

fish_preferences = preferences.get_fish_preferences()

def fishing_conditions(
        temperature, air_pressure, wind_speed, cloud_cover,
        precipitation, precipitation_type, sunrise, sunset, fish_preferences):

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

def listConditions(location, quality):
    print(f"\nFishing conditions for {location} on {datetime.now().strftime('%d/%m/%Y')}:")
    for fish, score in quality.items():
        print(f"{fish}: {score:.1f}/10")

def showGraph(dfs, locations):
    """Creating the bar graph visualization of the dataset"""
    plt.figure(figsize=(10, 6))

    num_locations = len(dfs)
    bar_width = 0.8 / num_locations  # Adjust bar width based on number of locations
    index = dfs[0].index

    # Define a list of 10 distinct colors
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'black', 'gray']

    for i, df in enumerate(dfs):
        # Use the color corresponding to the location's order in the list
        plt.bar(index + i * bar_width, df['Score'], bar_width, color=colors[i % len(colors)], label=locations[i])
        plt.draw()  # Force an update of the figure

    # Centering x-ticks correctly
    plt.xticks(index + bar_width * (num_locations - 1) / 2, dfs[0]['Fish'], rotation=45, ha="right")
    plt.legend()

    plt.style.use('dark_background')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xlabel("Fish", fontsize=12)
    plt.ylabel("Score", fontsize=12)
    plt.title(f"Fishing Conditions in {', '.join(locations)}", fontsize=14)
    plt.grid(axis='y', alpha=0.7)
    plt.ylim(0, 10)
    plt.tight_layout()
    plt.show()

def selectFish(df):
    while True:
        fish = input("\nEnter the name of the fish you want to see the data for (or enter 'exit' to return back to choices): \n>>> ").lower()
        while fish.lower() not in df["Fish"].str.lower().tolist() + ["exit"]:
            print(f"\nError: Fish '{fish}' not found in the data.\n")
            fish = input("Please enter a valid Irish freshwater fish species:"
                         "\n(Pike, Perch, Brown Trout, Atlantic Salmon, Roach, "
                         "Bream, Rudd, Tench, Eel, Dace, Chub, Gudgeon)\n>>> ").lower()

        if fish == "pike":
            print(f"\nFish: Pike\nScore: {df.loc[df['Fish'] == 'Pike', 'Score'].item():.1f}/10")
        elif fish == "perch":
            print(f"\nFish: Perch\nScore: {df.loc[df['Fish'] == 'Perch', 'Score'].item():.1f}/10")
        elif fish == "brown trout":
            print(f"\nFish: Brown Trout\nScore: {df.loc[df['Fish'] == 'Brown Trout', 'Score'].item():.1f}/10")
        elif fish == "atlantic salmon":
            print(f"\nFish: Atlantic Salmon\nScore: {df.loc[df['Fish'] == 'Atlantic Salmon', 'Score'].item():.1f}/10")
        elif fish == "roach":
            print(f"\nFish: Roach\nScore: {df.loc[df['Fish'] == 'Roach', 'Score'].item():.1f}/10")
        elif fish == "bream":
            print(f"\nFish: Bream\nScore: {df.loc[df['Fish'] == 'Bream', 'Score'].item():.1f}/10")
        elif fish == "rudd":
            print(f"\nFish: Rudd\nScore: {df.loc[df['Fish'] == 'Rudd', 'Score'].item():.1f}/10")
        elif fish == "tench":
            print(f"\nFish: Tench\nScore: {df.loc[df['Fish'] == 'Tench', 'Score'].item():.1f}/10")
        elif fish == "eel":
            print(f"\nFish: Eel\nScore: {df.loc[df['Fish'] == 'Eel', 'Score'].item():.1f}/10")
        elif fish == "dace":
            print(f"\nFish: Dace\nScore: {df.loc[df['Fish'] == 'Dace', 'Score'].item():.1f}/10")
        elif fish == "chub":
            print(f"\nFish: Chub\nScore: {df.loc[df['Fish'] == 'Chub', 'Score'].item():.1f}/10")
        elif fish == "gudgeon":
            print(f"\nFish: Gudgeon\nScore: {df.loc[df['Fish'] == 'Gudgeon', 'Score'].item():.1f}/10")
        elif fish == "exit":
            break
        time.sleep(5)

def compareLocations():
    num_locations = input("\nEnter how many locations do you want to compare:\n>>> ")
    while num_locations not in ["2","3","4","5","6","7","8","9","10"]:
        num_locations = input("\nInvalid input. Please enter a positive integer greater between 2 and 10:\n>>> ")
    num_locations = int(num_locations)
    locations = []
    dfs = []

    for i in range(num_locations):
        while True:
            try:
                location = input(f"\nEnter location {i + 1}: ").lower()
                while not location.isalpha():
                    location = input("\nInvalid input. Please enter your desired fishing location\n>>> ").lower()
                location = location[0].upper() + location[1:].lower() + ",IE"

                weather_data = get_weather_data(location)
                parsed_data = parse_weather_data(weather_data)
                quality = fishing_conditions(**parsed_data, fish_preferences=fish_preferences)

                with open("Conditions.csv", "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Fish", "Score"])  # Write header row
                    for fish, score in quality.items():
                        writer.writerow([fish, f"{score:.1f}"])

                df = pd.read_csv("Conditions.csv")
                dfs.append(df)
                locations.append(location)
                break  # Break the loop if no exception is raised

            except ValueError as e:
                print(f"\nError: {e}")
            except FileNotFoundError:
                print(f"\nError: File not found at 'Conditions.csv'. Please check the path.")
                exit()
            except Exception as e:
                print(f"Error: {e}")

    showGraph(dfs, locations)

def enterData():
    """Allows the user to manually enter weather data and get fishing condition scores."""

    while True:
        try:
            # Prompt for weather data input
            temperature = float(input("Enter current temperature in Celsius: "))
            air_pressure = float(input("Enter air pressure in hPa: "))
            wind_speed = float(input("Enter wind speed in km/h: "))
            cloud_cover = int(input("Enter cloud cover percentage (0-100): "))
            precipitation = float(input("Enter precipitation in mm (e.g., 0 for no rain, 2.5 for light rain): "))
            precipitation_type = input("Enter precipitation type ('Rain' or 'None'): ").capitalize()
            sunrise_str = input("Enter sunrise time (HH:MM:SS): ")
            sunset_str = input("Enter sunset time (HH:MM:SS): ")

            # Validate cloud cover input
            if not 0 <= cloud_cover <= 100:
                raise ValueError("Invalid cloud cover percentage. Please enter a value between 0 and 100.")

            # Validate precipitation type input
            if precipitation_type not in ["Rain", "None"]:
                raise ValueError("Invalid precipitation type. Please enter 'Rain' or 'None'.")

            # Convert sunrise and sunset strings to datetime.time objects
            try:
                sunrise = datetime.strptime(sunrise_str, "%H:%M:%S").time()
                sunset = datetime.strptime(sunset_str, "%H:%M:%S").time()
            except ValueError:
                raise ValueError("Invalid time format. Please use HH:MM:SS format for sunrise and sunset.")

            # Create a dictionary to store the manually entered weather data
            manual_weather_data = {
                "temperature": temperature,
                "air_pressure": air_pressure,
                "wind_speed": wind_speed,
                "cloud_cover": cloud_cover,
                "precipitation": precipitation,
                "precipitation_type": precipitation_type,
                "sunrise": sunrise,
                "sunset": sunset
            }

            # Calculate fishing conditions based on manual input
            quality = fishing_conditions(**manual_weather_data, fish_preferences=fish_preferences)

            # Display the results
            print("\nFishing conditions based on your input:")
            for fish, score in quality.items():
                print(f"{fish}: {score:.1f}/10")

            break  # Exit the loop if no exceptions are raised

        except ValueError as e:
            print(f"Error: {e}")


def main():
    mode = input("\nWould you like to do: 0. EXIT 1. List Data; 2. Graph Data; 3. Select Data; 4. Compare Locations; 5. Enter Data Yourself\n>>> ")
    if mode not in ["0", "1", "2", "3", "4", "5"]:
        mode = input("\nThis is not a valid input; Please enter either '0', '1', '2', '3', '4', or '5':\n>>> ")

    if mode == "0":
        print("\nExiting the program.", end="")
        time.sleep(0.5)
        print(".", end="")
        time.sleep(0.5)
        print(".", end="")
        time.sleep(0.5)
        print(".")
        exit()
    elif mode == "1":
        listConditions(location, quality)
        time.sleep(5)
        main()
    elif mode == "2":
        showGraph([df], [location])  # Pass single DataFrame as a list
        main()
    elif mode == "3":
        selectFish(df)
        main()
    elif mode == "4":
        compareLocations()
        main()
    elif mode == "5":
        enterData()
        main()


if __name__ == "__main__":
    while True:
        try:
            location = input("\nEnter your desired fishing location\n>>> ").lower()
            while not location.isalpha():
                location = input("\nInvalid input. Please enter your desired fishing location\n>>> ").lower()
            location = location[0].upper() + location[1:].lower() + ",IE"

            weather_data = get_weather_data(location)
            parsed_data = parse_weather_data(weather_data)
            fish_preferences = preferences.get_fish_preferences()
            quality = fishing_conditions(**parsed_data, fish_preferences=fish_preferences)

            with open("Conditions.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Fish", "Score"])  # Write header row
                for fish, score in quality.items():
                    now = datetime.now()
                    writer.writerow([fish, f"{score:.1f}"])

            try:
                df = pd.read_csv(fileName)  # Read the CSV into a pandas DataFrame
            except FileNotFoundError:
                print(f"\nError: File not found at '{fileName}'. Please check the path.")
                exit()

            main()
            break  # Break the loop if no exception is raised

        except ValueError as e:
            print(f"\nError: {e}")
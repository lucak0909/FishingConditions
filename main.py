import requests

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import csv
import pandas as pd
import time
import preferences

API_KEY = "2fd4c84ae5dc94f364025a03e86b7926"  # Replace with your API key
location = input("\nEnter your desired fishing location\n>>> ").lower()
while not location.isalpha():
    location = input("\nInvalid input. Please enter your desired fishing location\n>>> ").lower()
location = location[0].upper() + location[1:].lower() + ",IE"
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

def listConditions():
    print(f"\nFishing conditions for {location} on {datetime.now().strftime('%d/%m/%Y')}:")
    for fish, score in quality.items():
        print(f"{fish}: {score:.1f}/10")

def showGraph(df, df2=None):
    """Creating the bar graph visualization of the dataset"""
    plt.figure(figsize=(10, 6))

    if df2 is not None:  # Compare mode
        bar_width = 0.35
        index = df.index
        plt.bar(index, df['Score'], bar_width, color='skyblue', label=location)
        plt.bar(index + bar_width, df2['Score'], bar_width, color='lightcoral', label=location2)
        plt.xticks(index + bar_width / 2, df['Fish'], rotation=45, ha="right")
        plt.legend()
    else:  # Single location mode
        plt.bar(df['Fish'], df['Score'], color='skyblue', width=0.6)
        plt.xticks(rotation=45, ha="right")

    plt.style.use('dark_background')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xlabel("Fish", fontsize=12)
    plt.ylabel("Score", fontsize=12)
    plt.title(f"Fishing Conditions in {location}" if df2 is None else
              f"Fishing Conditions in {location} vs {location2}", fontsize=14)
    plt.grid(axis='y', alpha=0.7)
    plt.ylim(0, 10)
    plt.tight_layout()
    plt.show()

def selectFish():
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
    global location2  # Declare location2 as global
    choice = input("\nDo you want to compare the current location with another? (y/n): ").lower()
    if choice == 'y':
        location2 = input("\nEnter the second location: ").lower()
        while not location2.isalpha():
            location2 = input("\nInvalid input. Please enter your desired fishing location\n>>> ").lower()
        location2 = location2[0].upper() + location2[1:].lower() + ",IE"

        try:
            weather_data2 = get_weather_data(location2)
            parsed_data2 = parse_weather_data(weather_data2)
            quality2 = fishing_conditions(**parsed_data2, fish_preferences=fish_preferences)

            with open("Conditions2.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Fish", "Score"])  # Write header row
                for fish, score in quality2.items():
                    writer.writerow([fish, f"{score:.1f}"])

            try:
                df2 = pd.read_csv("Conditions2.csv")
                showGraph(df, df2)  # Pass both DataFrames to showGraph
            except FileNotFoundError:
                print(f"\nError: File not found at 'Conditions2.csv'. Please check the path.")
                exit()

        except Exception as e:
            print(f"Error: {e}")
    elif choice == 'n':
        main()
    elif choice == 'e':
        location = input("\nEnter your desired fishing location\n>>> ").lower()
        while not location.isalpha():
            location = input("\nInvalid input. Please enter your desired fishing location\n>>> ").lower()
        location = location[0].upper() + location[1:].lower() + ",IE"
        compareLocations()  # Call compareLocations again for a new location input
    else:
        print("\nInvalid input. Please enter 'y', 'n' or 'e'")
        compareLocations()

def main():
    mode = input("\nWould you like to do: (a) List Data; (b) Graph Data; (c) Select Data; (d) Compare Locations; (e) EXIT\n>>> ")
    if mode not in ["a", "b", "c", "d", "A", "B", "C", "D", "e", "E"]:
        mode = input("\nThis is not a valid input; Please enter either 'a', 'b', 'c', 'd', or 'e':\n>>> ")
    mode = mode.lower()

    if mode == "a":
        listConditions()
        time.sleep(5)
        main()
    elif mode == "b":
        showGraph(df)
        main()
    elif mode == "c":
        selectFish()
        main()
    elif mode == "d":
        compareLocations()
        main()
    elif mode == "e":
        print("\nExiting the program.", end="")
        time.sleep(0.5)
        print(".", end="")
        time.sleep(0.5)
        print(".", end="")
        time.sleep(0.5)
        print(".")
        exit()

if __name__ == "__main__":
    try:
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

    except Exception as e:
        print(f"Error: {e}")
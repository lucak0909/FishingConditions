from datetime import datetime
import csv
import time

import matplotlib.pyplot as plt
import pandas as pd

from . import lures, preferences, weather

fileName = "Conditions.csv"

fish_preferences = preferences.get_fish_preferences()


def fishing_conditions(
        temperature, air_pressure, wind_speed, cloud_cover,
        precipitation, precipitation_type, sunrise, sunset, fish_preferences, description=None):

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
    valid_fish = df["Fish"].str.lower().tolist()
    while True:
        fish = input("\nEnter the name of the fish you want to see the data for (or enter 'exit' to return back to choices): \n>>> ").lower()
        while fish not in valid_fish + ["exit"]:
            print(f"\nError: Fish '{fish}' not found in the data.\n")
            fish = input(f"Please enter a valid fish species ({', '.join(df['Fish'])}):\n>>> ").lower()

        if fish == "exit":
            break

        match = df.loc[df["Fish"].str.lower() == fish, ["Fish", "Score"]].iloc[0]
        print(f"\nFish: {match['Fish']}\nScore: {float(match['Score']):.1f}/10")


def lureHelper(description=None, wind_speed_kmh=None):
    """Tag-based lure recommendation. Reuses the current weather fetch if available,
    otherwise asks for enough info to classify the weather manually."""

    if description is None:
        description = input("\nBriefly describe the weather (e.g. 'clear', 'overcast', 'rain'): \n>>> ")
    if wind_speed_kmh is None:
        while True:
            try:
                wind_speed_kmh = float(input("Wind speed in km/h: \n>>> "))
                break
            except ValueError:
                print("Please enter a number.")

    weather_tags = weather.classify_weather_tags(description, wind_speed_kmh)

    species_options = lures.ALL_SPECIES
    print("\nTarget species:")
    for idx, species in enumerate(species_options, 1):
        print(f"{idx}. {species}")
    species_choice = input(f"Enter a number (1-{len(species_options)}): \n>>> ")
    while species_choice not in [str(i) for i in range(1, len(species_options) + 1)]:
        species_choice = input("Invalid choice. Try again: \n>>> ")
    species = species_options[int(species_choice) - 1]

    water_clarity = input("\nWater clarity - clear or murky? \n>>> ").strip().lower()
    while water_clarity not in ["clear", "murky"]:
        water_clarity = input("Please enter 'clear' or 'murky': \n>>> ").strip().lower()

    depth = input("\nWater depth - shallow or deep? \n>>> ").strip().lower()
    while depth not in ["shallow", "deep"]:
        depth = input("Please enter 'shallow' or 'deep': \n>>> ").strip().lower()

    recommendations = lures.recommend_lures(species, water_clarity, depth, weather_tags)

    if not recommendations:
        print("\nNo strong matches found for those conditions -- try a different combination.")
        return

    print(f"\nTop lure picks for {species} in {water_clarity} water ({depth}), weather tags: {', '.join(sorted(weather_tags))}:")
    for lure in recommendations:
        print(f"- {lure['name']} ({lure['style']})")


def compareLocations():
    num_locations = input("\nEnter how many locations do you want to compare:\n>>> ")
    while num_locations not in [str(i) for i in range(2, 11)]:
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

                weather_data = weather.get_weather_data(location)
                parsed_data = weather.parse_weather_data(weather_data)
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


def displayData(location, df, description=None, wind_speed_kmh=None):
    mode = input(
        "\nWould you like to do: 0. EXIT 1. List Data; 2. Graph Data; 3. Select Data; "
        "4. Compare Locations; 5. Enter Data Yourself; 6. Lure Helper\n>>> "
    )
    while mode not in [str(i) for i in range(7)]:
        mode = input("\nThis is not a valid input; Please enter a number from 0-6:\n>>> ")

    if mode == "0":
        print("\nExiting the program.", end="")
        time.sleep(0.5)
        print(".", end="")
        time.sleep(0.5)
        print(".", end="")
        time.sleep(0.5)
        print(".")
        return
    elif mode == "1":
        quality = dict(zip(df["Fish"], df["Score"]))
        listConditions(location, quality)
    elif mode == "2":
        showGraph([df], [location])  # Pass single DataFrame as a list
    elif mode == "3":
        selectFish(df)
    elif mode == "4":
        compareLocations()
    elif mode == "5":
        enterData()
    elif mode == "6":
        lureHelper(description, wind_speed_kmh)

    displayData(location, df, description, wind_speed_kmh)


def run_cli():
    while True:
        try:
            location = input("\nEnter your desired fishing location\n>>> ").lower()
            while not location.isalpha():
                location = input("\nInvalid input. Please enter your desired fishing location\n>>> ").lower()
            location = location[0].upper() + location[1:].lower() + ",IE"

            weather_data = weather.get_weather_data(location)
            parsed_data = weather.parse_weather_data(weather_data)
            quality = fishing_conditions(**parsed_data, fish_preferences=fish_preferences)

            with open(fileName, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Fish", "Score"])  # Write header row
                for fish, score in quality.items():
                    writer.writerow([fish, f"{score:.1f}"])

            df = pd.read_csv(fileName)  # Read the CSV into a pandas DataFrame

            displayData(location, df, parsed_data["description"], parsed_data["wind_speed"])
            break  # Break the loop if no exception is raised

        except ValueError as e:
            print(f"\nError: {e}")
        except RuntimeError as e:
            print(f"\nError: {e}")
            break


if __name__ == "__main__":
    run_cli()

"""Standalone entry point for the tag-based lure recommender.

See lures.py for the tag database/scoring logic and weather.py for the
weather fetch + classification shared with the rest of the app.
"""

import lures
import weather


def run_lure_picker():
    location = input("Enter the city to get the weather data: ").strip()
    if not location:
        print("No location entered.")
        return

    try:
        weather_data = weather.get_weather_data(location)
    except (ValueError, RuntimeError) as e:
        print(f"Error fetching weather data: {e}")
        return

    parsed = weather.parse_weather_data(weather_data)
    print(
        f"Weather in {location}: {parsed['description']}, "
        f"Temperature: {parsed['temperature']}°C, Wind Speed: {parsed['wind_speed']:.1f} km/h\n"
    )

    weather_tags = weather.classify_weather_tags(parsed["description"], parsed["wind_speed"])

    species_options = lures.ALL_SPECIES
    print("Target species:")
    for idx, species in enumerate(species_options, 1):
        print(f"{idx}. {species}")
    species_choice = input(f"Enter a number (1-{len(species_options)}): ")
    while species_choice not in [str(i) for i in range(1, len(species_options) + 1)]:
        species_choice = input("Invalid choice. Try again: ")
    species = species_options[int(species_choice) - 1]

    water_conditions = ["Clear Water", "Murky Water"]
    print("\nPlease select the water conditions:")
    for idx, condition in enumerate(water_conditions, 1):
        print(f"{idx}. {condition}")
    water_choice = input("Enter the number corresponding to the water conditions: ")
    while water_choice not in ["1", "2"]:
        water_choice = input("Invalid choice. Please enter 1 or 2: ")
    water_clarity = "clear" if water_choice == "1" else "murky"

    water_depths = ["Shallow (<2m)", "Deep (>3m)"]
    print("\nPlease select the water depth:")
    for idx, d in enumerate(water_depths, 1):
        print(f"{idx}. {d}")
    depth_choice = input("Enter the number corresponding to the water depth: ")
    while depth_choice not in ["1", "2"]:
        depth_choice = input("Invalid choice. Please enter 1 or 2: ")
    depth = "shallow" if depth_choice == "1" else "deep"

    recommendations = lures.recommend_lures(species, water_clarity, depth, weather_tags)

    if not recommendations:
        print("\nNo strong matches found for those conditions -- try a different combination.")
        return

    print(f"\nRecommended lures for {species}, {water_conditions[int(water_choice) - 1]}, {water_depths[int(depth_choice) - 1]}:")
    for lure in recommendations:
        print(f"- {lure['name']} ({lure['style']})")


if __name__ == "__main__":
    run_lure_picker()

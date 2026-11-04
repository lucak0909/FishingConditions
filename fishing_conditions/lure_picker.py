"""Standalone entry point for the lure suitability advisor.

See lures.py for the scoring logic and weather.py for the weather fetch +
classification shared with the rest of the app.
"""

from . import lures, weather


def _choose(options, label):
    print(f"\n{label}:")
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    choice = input(f"Enter a number (1-{len(options)}): ")
    while choice not in [str(i) for i in range(1, len(options) + 1)]:
        choice = input("Invalid choice. Try again: ")
    return options[int(choice) - 1]


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
        f"Temperature: {parsed['temperature']}°C, Wind Speed: {parsed['wind_speed']:.1f} km/h"
    )

    weather_tags = weather.classify_weather_tags(parsed["description"], parsed["wind_speed"])

    water_clarity = _choose(["clear", "murky"], "Water clarity")
    target_depth = _choose(["shallow", "deep"], "Target fishing depth")

    print("\nNow describe the lure you're considering:")
    colour = _choose(lures.COLOURS, "Colour")
    finish = _choose(lures.FINISHES, "Finish")
    action = _choose(lures.ACTIONS, "Action")
    depth = _choose(lures.DEPTHS, "Running depth")

    score, feedback = lures.assess_lure(colour, finish, action, depth, water_clarity, target_depth, weather_tags)

    print(f"\nSuitability score for these conditions ({', '.join(sorted(weather_tags))} weather): {score:.1f}/10")
    if feedback:
        print("Suggestions:")
        for tip in feedback:
            print(f"- {tip}")
    else:
        print("Good choice for these conditions!")


if __name__ == "__main__":
    run_lure_picker()

import requests


# Function to fetch weather data from OpenWeatherMap API
def get_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for non-200 status codes
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        return weather, temp, wind_speed
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None, None, None


# Function to match conditions and recommend lure
def get_lure_recommendation(api_key, city):
    # Fetch weather data
    weather, temp, wind_speed = get_weather_data(api_key, city)

    if weather is None:
        return

    print(f"Weather in {city}: {weather}, Temperature: {temp}°C, Wind Speed: {wind_speed} m/s\n")

    # Get user input for water conditions
    water_conditions = ["Clear Water", "Murky Water"]
    while True:
        print("Please select the water conditions:")
        for idx, condition in enumerate(water_conditions, 1):
            print(f"{idx}. {condition}")
        try:
            water_condition_choice = int(input("Enter the number corresponding to the water conditions: "))
            if 1 <= water_condition_choice <= len(water_conditions):
                water_condition = water_conditions[water_condition_choice - 1]
                break
            else:
                print("Invalid choice. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Get user input for water depth
    water_depths = ["Shallow (<2m)", "Deep (>3m)"]
    while True:
        print("\nPlease select the water depth:")
        for idx, depth in enumerate(water_depths, 1):
            print(f"{idx}. {depth}")
        try:
            water_depth_choice = int(input("Enter the number corresponding to the water depth: "))
            if 1 <= water_depth_choice <= len(water_depths):
                water_depth = water_depths[water_depth_choice - 1]
                break
            else:
                print("Invalid choice. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Combine weather, water conditions, and depth to determine the appropriate lure
    if 'clear' in weather.lower():
        if water_condition == "Clear Water":
            if water_depth == "Shallow (<2m)":
                recommended_lures = "McHybrid (Perch), Westin Swim (Golden 3D Perch), Westin Mike the Pike, Westin R&R ShadTeez Motoroil Burbot"
            else:
                recommended_lures = "Berkley Zilla Flanker (Ayu Green), Copper Abu Garcia Atom Spoon, Westin Mike the Pike"
        elif water_condition == "Murky Water":
            if water_depth == "Shallow (<2m)":
                recommended_lures = "Headbanger Shad (Firetiger), Firetiger Spinnerbait, Savage Gear Deviator Swim Firetiger"
            else:
                recommended_lures = "Storm RIP Curly Tail (Demon), Copper Abu Garcia Atom Spoon, Pike Chatterbait"
    elif 'cloud' in weather.lower() or 'overcast' in weather.lower():
        if water_condition == "Clear Water":
            if water_depth == "Shallow (<2m)":
                recommended_lures = "McMio Fegis, Abu Garcia Tormentor Jointed Crankbait"
            else:
                recommended_lures = "McMio Fegis, Abu Garcia Tormentor Jointed Crankbait, Westin Mike the Pike"
        elif water_condition == "Murky Water":
            if water_depth == "Shallow (<2m)":
                recommended_lures = "Storm RIP Curly Tail (Demon), Copper Abu Garcia Atom Spoon, Savage Gear Deviator Swim Firetiger"
            else:
                recommended_lures = "Pike Chatterbait, Storm RIP Curly Tail (Hot Pike), Savage Gear Deviator Swim Firetiger"
    else:  # Windy conditions or other cases
        if water_condition == "Clear Water":
            if water_depth == "Shallow (<2m)":
                recommended_lures = "Rapala XRap Otis (Hot Pike), White Spinnerbait, Westin R&R ShadTeez Motoroil Burbot"
            else:
                recommended_lures = "Rapala XRap Otis (Hot Pike), White Spinnerbait, Pike Chatterbait"
        elif water_condition == "Murky Water":
            if water_depth == "Shallow (<2m)":
                recommended_lures = "Pike Chatterbait, Storm RIP Curly Tail (Hot Pike), Savage Gear Deviator Swim Firetiger"
            else:
                recommended_lures = "Storm RIP Curly Tail (Demon/Hot Pike), Pike Chatterbait, Abu Garcia Beast Fegis, Savage Gear Deviator Swim Firetiger"

    print(f"\nRecommended lures for {weather} weather, {water_condition} with {water_depth}: {recommended_lures}")


# Example usage
if __name__ == "__main__":
    # Enter your OpenWeatherMap API key here
    api_key = "2fd4c84ae5dc94f364025a03e86b7926"
    city = input("Enter the city to get the weather data: ")

    get_lure_recommendation(api_key, city)

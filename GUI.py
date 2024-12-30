import requests
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import preferences

API_KEY = "2fd4c84ae5dc94f364025a03e86b7926"  # Replace with your API key


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
    elif response.status_code == 404:
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


def fishing_conditions(temperature, air_pressure, wind_speed, cloud_cover,
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


class FishingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fishing Conditions App")
        self.root.geometry("600x400")

        self.location = tk.StringVar()
        self.fish_preferences = preferences.get_fish_preferences()

        self.setup_ui()

    def setup_ui(self):
        # Input for location
        tk.Label(self.root, text="Enter location:").pack(pady=10)
        self.location_entry = tk.Entry(self.root, textvariable=self.location)
        self.location_entry.pack(pady=5)

        # Button to fetch and show weather data
        tk.Button(self.root, text="Get Fishing Conditions", command=self.fetch_weather_data).pack(pady=10)

        # Display area for conditions
        self.conditions_text = tk.Text(self.root, height=10, width=60)
        self.conditions_text.pack(pady=10)

        # Graph button
        tk.Button(self.root, text="Show Graph", command=self.show_graph).pack(pady=10)

    def fetch_weather_data(self):
        location = self.location.get()
        if location:
            try:
                location = location.capitalize() + ",IE"
                weather_data = get_weather_data(location)
                parsed_data = parse_weather_data(weather_data)
                quality = fishing_conditions(**parsed_data, fish_preferences=self.fish_preferences)

                # Display conditions in text box
                self.conditions_text.delete(1.0, tk.END)  # Clear previous data
                self.conditions_text.insert(tk.END, f"Fishing conditions for {location}:\n\n")
                for fish, score in quality.items():
                    self.conditions_text.insert(tk.END, f"{fish}: {score:.1f}/10\n")

            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter a location.")

    def show_graph(self):
        location = self.location.get()
        if location:
            try:
                location = location.capitalize() + ",IE"
                weather_data = get_weather_data(location)
                parsed_data = parse_weather_data(weather_data)
                quality = fishing_conditions(**parsed_data, fish_preferences=self.fish_preferences)

                # Create a bar graph
                fish = list(quality.keys())
                scores = list(quality.values())

                fig, ax = plt.subplots(figsize=(8, 6))
                ax.bar(fish, scores, color='skyblue')
                ax.set_title(f"Fishing Conditions for {location}")
                ax.set_xlabel("Fish Species")
                ax.set_ylabel("Condition Score (0-10)")

                # Embed the plot in Tkinter
                canvas = FigureCanvasTkAgg(fig, self.root)
                canvas.get_tk_widget().pack(pady=20)
                canvas.draw()

            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please enter a location.")


# Main function to run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = FishingApp(root)
    root.mainloop()

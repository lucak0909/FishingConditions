import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from . import lures, preferences, weather


def fishing_conditions(temperature, air_pressure, wind_speed, cloud_cover,
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


class FishingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fishing Conditions App")
        self.root.geometry("640x520")

        self.location = tk.StringVar()
        self.fish_preferences = preferences.get_fish_preferences()
        self.last_weather = None  # parsed weather dict from the most recent successful fetch

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        self.conditions_tab = ttk.Frame(notebook)
        self.lure_tab = ttk.Frame(notebook)
        notebook.add(self.conditions_tab, text="Fishing Conditions")
        notebook.add(self.lure_tab, text="Lure Helper")

        self.setup_conditions_tab()
        self.setup_lure_tab()

    def setup_conditions_tab(self):
        tab = self.conditions_tab

        tk.Label(tab, text="Enter location:").pack(pady=10)
        self.location_entry = tk.Entry(tab, textvariable=self.location)
        self.location_entry.pack(pady=5)

        tk.Button(tab, text="Get Fishing Conditions", command=self.fetch_weather_data).pack(pady=10)

        self.conditions_text = tk.Text(tab, height=10, width=60)
        self.conditions_text.pack(pady=10)

        tk.Button(tab, text="Show Graph", command=self.show_graph).pack(pady=10)

    def setup_lure_tab(self):
        tab = self.lure_tab

        tk.Label(
            tab,
            text="Uses the weather from the last fetch on the Fishing Conditions tab\n"
                 "(or falls back to manual entry below). Describe the lure you're\n"
                 "considering and get a suitability score for the current conditions.",
            justify="left",
        ).pack(pady=10)

        form = tk.Frame(tab)
        form.pack(pady=5)

        def add_row(row, label_text, var, values):
            tk.Label(form, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=5)
            ttk.Combobox(form, textvariable=var, values=values, state="readonly").grid(
                row=row, column=1, padx=5, pady=5
            )

        self.clarity_var = tk.StringVar(value="clear")
        add_row(0, "Water clarity:", self.clarity_var, ["clear", "murky"])

        self.target_depth_var = tk.StringVar(value="shallow")
        add_row(1, "Target fishing depth:", self.target_depth_var, ["shallow", "deep"])

        self.colour_var = tk.StringVar(value=lures.COLOURS[0])
        add_row(2, "Lure colour:", self.colour_var, lures.COLOURS)

        self.finish_var = tk.StringVar(value=lures.FINISHES[0])
        add_row(3, "Lure finish:", self.finish_var, lures.FINISHES)

        self.action_var = tk.StringVar(value=lures.ACTIONS[0])
        add_row(4, "Lure action:", self.action_var, lures.ACTIONS)

        self.lure_depth_var = tk.StringVar(value=lures.DEPTHS[0])
        add_row(5, "Lure running depth:", self.lure_depth_var, lures.DEPTHS)

        tk.Button(tab, text="Assess Lure", command=self.assess_lure).pack(pady=10)

        self.lure_text = tk.Text(tab, height=8, width=60)
        self.lure_text.pack(pady=10)

    def fetch_weather_data(self):
        location = self.location.get()
        if not location:
            messagebox.showwarning("Input Error", "Please enter a location.")
            return

        try:
            location = location.capitalize() + ",IE"
            weather_data = weather.get_weather_data(location)
            parsed_data = weather.parse_weather_data(weather_data)
            quality = fishing_conditions(**parsed_data, fish_preferences=self.fish_preferences)
            self.last_weather = parsed_data

            self.conditions_text.delete(1.0, tk.END)
            self.conditions_text.insert(tk.END, f"Fishing conditions for {location}:\n\n")
            for fish, score in quality.items():
                self.conditions_text.insert(tk.END, f"{fish}: {score:.1f}/10\n")

        except (ValueError, RuntimeError) as e:
            messagebox.showerror("Error", str(e))

    def show_graph(self):
        location = self.location.get()
        if not location:
            messagebox.showwarning("Input Error", "Please enter a location.")
            return

        try:
            location = location.capitalize() + ",IE"
            weather_data = weather.get_weather_data(location)
            parsed_data = weather.parse_weather_data(weather_data)
            quality = fishing_conditions(**parsed_data, fish_preferences=self.fish_preferences)
            self.last_weather = parsed_data

            fish = list(quality.keys())
            scores = list(quality.values())

            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(fish, scores, color='skyblue')
            ax.set_title(f"Fishing Conditions for {location}")
            ax.set_xlabel("Fish Species")
            ax.set_ylabel("Condition Score (0-10)")
            plt.xticks(rotation=45, ha="right")
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, self.conditions_tab)
            canvas.get_tk_widget().pack(pady=20)
            canvas.draw()

        except (ValueError, RuntimeError) as e:
            messagebox.showerror("Error", str(e))

    def assess_lure(self):
        if self.last_weather is not None:
            description = self.last_weather["description"]
            wind_speed_kmh = self.last_weather["wind_speed"]
        else:
            description = "overcast"
            wind_speed_kmh = 0

        weather_tags = weather.classify_weather_tags(description, wind_speed_kmh)
        score, feedback = lures.assess_lure(
            self.colour_var.get(),
            self.finish_var.get(),
            self.action_var.get(),
            self.lure_depth_var.get(),
            self.clarity_var.get(),
            self.target_depth_var.get(),
            weather_tags,
        )

        self.lure_text.delete(1.0, tk.END)
        self.lure_text.insert(
            tk.END,
            f"Suitability score ({', '.join(sorted(weather_tags))} weather): {score:.1f}/10\n\n",
        )
        if feedback:
            self.lure_text.insert(tk.END, "Suggestions:\n")
            for tip in feedback:
                self.lure_text.insert(tk.END, f"- {tip}\n")
        else:
            self.lure_text.insert(tk.END, "Good choice for these conditions!")


def run_gui():
    root = tk.Tk()
    FishingApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()

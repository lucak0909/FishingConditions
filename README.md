# Fishing Conditions App

A Python app that scores fishing conditions for freshwater fish species in Ireland based on
live weather data, and recommends lures using a tag-based matching system.

## Features

* Fetches live weather data for a specified location in Ireland (OpenWeatherMap).
* Scores fishing conditions for 12 fish species based on temperature, air pressure, wind
  speed, cloud cover, precipitation and time of day.
* Lure Helper recommends lures by scoring them against the current weather, target species,
  water clarity and depth -- see "Lure tagging system" below.
* CLI with listing, graphing, per-fish lookup, multi-location comparison, and manual data entry.
* GUI (Tkinter) with a Fishing Conditions tab and a Lure Helper tab.

## Requirements

* Python 3.9+
* Tkinter (usually included with Python)
* See `requirements.txt` for Python packages

## Setup

1. Clone the repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api).
3. Copy `.env.example` to `.env` and fill in your key:
   ```bash
   cp .env.example .env
   ```
   Alternatively, set the `OPENWEATHER_API_KEY` environment variable directly.

   **Never commit your real API key.** `.env` is already gitignored.

## Running it

```bash
python main.py
```

This lets you choose between the CLI and the GUI. Each entry point can also be run directly as
a module: `python -m fishing_conditions.cli`, `python -m fishing_conditions.gui`, or
`python -m fishing_conditions.lure_picker` for the standalone lure recommender.

## Project layout

```
main.py                       # entry point -- pick CLI or GUI
fishing_conditions/
    cli.py                    # command-line interface
    gui.py                    # Tkinter interface
    lure_picker.py            # standalone lure recommender
    weather.py                # OpenWeatherMap fetch/parse, shared by cli/gui/lure_picker
    lures.py                  # tagged lure database + recommender
    preferences.py            # per-species fishing condition ranges
```

## Lure tagging system

Lures live in `lures.py` as plain tagged dicts instead of a hardcoded decision tree:

```python
{
    "name": "Pike Chatterbait",
    "species": ["Pike"],
    "water_clarity": ["murky"],
    "depth": ["deep"],
    "weather": ["clear", "overcast", "windy"],
    "style": "chatterbait",
}
```

`lures.recommend_lures(species, water_clarity, depth, weather_tags)` scores every lure by how
many of the requested tags it matches and returns the top candidates. Weather is turned into
tags (`clear`, `overcast`, `windy`, `rain`) by `weather.classify_weather_tags`.

To add a lure, just append a new dict to `lures.LURES` -- no branching logic to update, and it
immediately becomes available to the CLI, GUI and standalone picker alike.

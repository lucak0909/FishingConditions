# Fishing Conditions App

A Python app that scores fishing conditions for freshwater fish species in Ireland based on
live weather data, and tells you how well a lure you describe suits those conditions.

## Features

* Fetches live weather data for a specified location in Ireland (OpenWeatherMap).
* Scores fishing conditions for 12 fish species based on temperature, air pressure, wind
  speed, cloud cover, precipitation and time of day.
* Lure Helper scores a lure you describe (colour, finish, action, running depth) against the
  current weather, water clarity and target depth -- see "Lure suitability advisor" below.
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
`python -m fishing_conditions.lure_picker` for the standalone lure advisor.

## Project layout

```
main.py                       # entry point -- pick CLI or GUI
fishing_conditions/
    cli.py                    # command-line interface
    gui.py                    # Tkinter interface
    lure_picker.py            # standalone lure advisor
    weather.py                # OpenWeatherMap fetch/parse, shared by cli/gui/lure_picker
    lures.py                  # lure suitability scoring
    preferences.py            # per-species fishing condition ranges
```

## Lure suitability advisor

Rather than picking from a fixed list of named products (which inevitably goes out of date),
you describe the lure you're considering -- colour, finish, action and running depth -- and
`lures.assess_lure(...)` scores (0-10) how well those attributes suit the current water
clarity, target depth and weather, with plain-English suggestions for anything that scores low:

```python
score, feedback = lures.assess_lure(
    colour="bright", finish="matte", action="vibrating", depth="deep",
    water_clarity="murky", target_depth="deep", weather_tags={"windy"},
)
# score == 9.25, feedback == []
```

The scoring rules (bright/noisy in murky water, natural/subtle in clear water, flash on sunny
days, matching the lure's running depth to the target depth, etc.) live in the small `_score_*`
helper functions in `lures.py` -- tune the lookup tables there to adjust the advice.

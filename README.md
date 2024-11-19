# Fishing Conditions App

This is a simple Python application that provides fishing condition scores for various fish species based on weather data for a given location in Ireland.

## Features

* Fetches weather data for a specified location in Ireland.
* Calculates fishing condition scores for different fish species based on:
    * Wind speed
    * Wind direction
    * Wave height
    * Air temperature
    * Precipitation
    * Time of day
* Displays the scores in a user-friendly GUI with a table and a bar graph.
* Automatically updates the data every minute.

## Requirements

* Python 3.6 or higher
* Tkinter (usually included with Python)
* Requests library
* Matplotlib library
* Pandas library

## Installation

1. Clone the repository or download the source code.
2. Install the required libraries:
   ```bash
   pip install requests matplotlib pandas
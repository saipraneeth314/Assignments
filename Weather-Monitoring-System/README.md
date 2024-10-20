# Weather Monitoring System

## Overview

The **Weather Monitoring System** is a Python-based application that retrieves real-time weather data for multiple cities using the OpenWeatherMap API. It provides features to display current weather conditions, visualize historical temperature trends, and alert users when specific temperature thresholds are exceeded.

## Features

- Fetches real-time weather data for selected cities.
- Converts temperatures between Celsius, Fahrenheit, and Kelvin.
- Displays current weather information including temperature, humidity, and wind speed.
- Saves historical weather data for visualizing trends over time.
- Provides alerts for temperatures exceeding a specified threshold.
- Summarizes weather data, calculating average, maximum, minimum temperatures, and dominant weather conditions.

## Requirements

- Python 3.6 or higher
- `requests` library for making API calls
- `matplotlib` library for plotting weather trends

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Weather-Monitoring-System.git
   cd Weather-Monitoring-System

2. Install the required dependencies:
   ```bash
   pip install requests   
   pip install matplotlib

3. Obtain an API key from OpenWeatherMap and replace the placeholder in the code:
   API_KEY = 'your_api_key_here'

## Usage

1. Run the application(.py):
   ```bash
   python3 Weather_Monitoring_System.py

2. Run the application(.ipynb):
   open Weather_Monitoring_System.ipynb using Jupyter Notebook


## Acknowledgments

- Thanks to the [OpenWeatherMap API](https://openweathermap.org/api) for providing weather data.

- The plotting is done using the [matplotlib](https://matplotlib.org/) library.


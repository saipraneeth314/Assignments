import requests
import time
import matplotlib.pyplot as plt
from datetime import datetime

# Obtain an API key from OpenWeatherMap
API_KEY = 'bbf35fe7594dcdafdbd68041e98f9702'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# List of cities to monitor
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
# Store historical weather data for visualization
historical_data = []

# Conversion Functions

# Convert Celsius to Fahrenheit.
def convert_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32
# Convert Celsius to Kelvin
def convert_to_kelvin(celsius):
    return celsius + 273.15

# Fetching weather data for a specific city
def get_weather(city, unit='metric'):
  # Prepare API request parameters based on the desired units
    if unit == 'metric':
        params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    elif unit == 'imperial':
        params = {'q': city, 'appid': API_KEY, 'units': 'imperial'}
    else:
        params = {'q': city, 'appid': API_KEY}

    # Send the API request
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json() # Return JSON data if successful
    else:
        print(f"Failed to retrieve data for {city}. Status Code: {response.status_code}, Response: {response.text}")
        return None # Return None if the request failed

# Display Weather Data
def display_weather_data(city, data, preferred_unit='Celsius'):
    # Displaying the weather data for a given city.
    temp_celsius = data['main']['temp'] # Extract temperature in Celsius
    humidity = data['main']['humidity'] # Extract humidity percentage
    wind_speed = data['wind']['speed']  # Extract wind speed in m/s

    # Convert temperature based on user's preferred unit
    if preferred_unit == 'Fahrenheit':
        temp = convert_to_fahrenheit(temp_celsius)
        unit = "°F"
    elif preferred_unit == 'Kelvin':
        temp = convert_to_kelvin(temp_celsius)
        unit = "K"
    else: # Default to Celsius
        temp = temp_celsius
        unit = "°C"
    # Print the weather data
    print(f"Weather in {city}: {temp}{unit}, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s")

# Save Historical Data for Visualization
def save_historical_data(weather_data):
    for data in weather_data:
        city = data['name'] # Get city name
        temp = data['main']['temp'] # Get temperature
        timestamp = datetime.now() # Get current timestamp
        # Append data to the historical_data list
        historical_data.append({'city': city, 'temp': temp, 'timestamp': timestamp})

# Plot temperature trends over time for the monitored cities.
def plot_weather_trends():
    if not historical_data:
        print("No historical data available to plot.")
        return

    # Get unique cities from historical data
    cities = set([entry['city'] for entry in historical_data])
    plt.figure(figsize=(10, 6)) # Create a new figure for plotting


    for city in cities:
        city_data = [entry for entry in historical_data if entry['city'] == city] # Filter data for the city
        timestamps = [entry['timestamp'] for entry in city_data] # Get timestamps
        temps = [entry['temp'] for entry in city_data] # Get temperatures
        plt.plot(timestamps, temps, marker='o', label=city) # Plot the data

    # Set plot title and labels
    plt.title("Weather Trends Over Time")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.xticks(rotation=45) # Rotate x-axis labels for better readability
    plt.tight_layout() # Adjust layout to prevent overlap
    plt.show()

# Summarize weather data for a list of weather responses.
def summarize_weather_data(data_list):
    if not data_list:
        print("No weather data available to summarize.")
        return None

    avg_temp = sum([data['main']['temp'] for data in data_list]) / len(data_list) # Calculating average temperature
    max_temp = max([data['main']['temp'] for data in data_list]) # Find maximum temperature
    min_temp = min([data['main']['temp'] for data in data_list]) # Find minimum temperature

    # Determine the dominant weather condition
    dominant_condition = max(set([data['weather'][0]['main'] for data in data_list]),
                             key=[data['weather'][0]['main'] for data in data_list].count)

    return {
        "average_temp": avg_temp,
        "max_temp": max_temp,
        "min_temp": min_temp,
        "dominant_condition": dominant_condition
    }

# Check Thresholds for Alerts
def check_thresholds(data, temp_threshold=35):
    # Check if the current temperature exceeds a specified threshold.
    if data['main']['temp'] > temp_threshold:
        print("Alert! Temperature threshold exceeded:", data['main']['temp'])

# Main Monitoring Function
def start_monitoring(max_iterations=2, preferred_unit='Celsius'):
    # Start monitoring the weather for specified cities.
    iteration = 0
    while iteration < max_iterations:
        weather_data = []
        for city in CITIES:
            data = get_weather(city)# Fetch weather data for the city
            if data:
                display_weather_data(city, data, preferred_unit) # Display the weather data
                weather_data.append(data) # Collect the data for summarization
                check_thresholds(data) # Check for temperature alerts

        if weather_data:
            save_historical_data(weather_data) # Save data for later visualization
            summary = summarize_weather_data(weather_data) # Summarize the collected data
            if summary:
                print("Daily Summary:", summary)
                plot_weather_trends()
        else:
            print("No data was retrieved for any of the cities.")

        iteration += 1
        time.sleep(180) # Wait for 3 minutes before the next iteration

if __name__ == "__main__":
    # Monitor for 10 iterations
    start_monitoring(max_iterations= 10, preferred_unit='Celsius')
    #preferred_unit = 'Celsius', 'Fahrenheit', or 'Kelvin'

"""# Test_Weather"""

import unittest

class WeatherMonitoringTestCase(unittest.TestCase):
    # Test the weather retrieval function.
    def test_get_weather(self):
        city = "Delhi"
        data = get_weather(city)
        self.assertIsNotNone(data, "Failed to retrieve data for the city")
    # Test the temperature conversion functions.
    def test_temperature_conversion(self):
        self.assertEqual(convert_to_fahrenheit(0), 32, "Conversion to Fahrenheit failed")
        self.assertEqual(convert_to_kelvin(0), 273.15, "Conversion to Kelvin failed")

    # Test the summarization of weather data.
    def test_summarize_weather_data(self):
        sample_data = [
            {'main': {'temp': 30}, 'weather': [{'main': 'Clear'}]},
            {'main': {'temp': 32}, 'weather': [{'main': 'Clear'}]},
            {'main': {'temp': 28}, 'weather': [{'main': 'Clouds'}]}
        ]
        summary = summarize_weather_data(sample_data)
        self.assertEqual(summary['average_temp'], 30, "Average temperature calculation failed")
        self.assertEqual(summary['max_temp'], 32, "Max temperature calculation failed")
        self.assertEqual(summary['min_temp'], 28, "Min temperature calculation failed")
        self.assertEqual(summary['dominant_condition'], 'Clear', "Dominant condition calculation failed")

# Run the unit tests if this script is executed directly
if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
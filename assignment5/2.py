import requests
import json # You'll need this to convert the data to a string for SQL

API_KEY = "52d28f3b78da31e08f6931d2a5d65a8c"

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
CITY_NAME = "NewYork"

def get_weather_data(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

raw_data = get_weather_data(CITY_NAME)
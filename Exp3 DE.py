import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from datetime import date

API_KEY = "OLkdUG85N3tMzBdoOECIgeZOXLRTadjq"   
CITY = "London"

# MySQL connection settings
USER = "root"
PASSWORD = "root"          # replace with your MySQL password
HOST = "127.0.0.1"                 # use 127.0.0.1 instead of 'localhost'
PORT = 3306
DB   = "sales_weatherinfo_db"

# Connection string (password is URL-encoded in case it has special chars)
MYSQL_CONN_STRING = f"mysql+pymysql://{USER}:{quote_plus(PASSWORD)}@{HOST}:{PORT}/{DB}"

def fetch_weather(api_key: str, city: str) -> dict:
    """Fetch current weather from OpenWeather API."""
    url = "https://api.tomorrow.io/v4/weather/forecast?location=42.3478,-71.0466&apikey=OLkdUG85N3tMzBdoOECIgeZOXLRTadjq"
    params = {"q": city, "appid": api_key.strip(), "units": "metric"}

    r = requests.get(url, params=params, timeout=20)
    if r.status_code != 200: #status_code = 200, returns success else error  
        try:
            print("OpenWeather error payload:", r.json())
        except Exception:
            print("OpenWeather non-JSON response:", r.text)
        r.raise_for_status()

    data = r.json()
    return {
        "weather_date": date.today(),
        "city": city,
        "temp_c": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
    }
def ensure_weather_table(engine) -> None:
    """Create table if not exists in MySQL."""
    #ddl - data definition language in MYSQL, CRUD operations performed on database 
    ddl = """
    CREATE TABLE IF NOT EXISTS weather (
        weather_date DATE NOT NULL,
        city VARCHAR(100) NOT NULL,
        temp_c DECIMAL(5,2),
        humidity INT,
        description VARCHAR(255)
    )
    """ 
    #connecting to mysql and uploading the data into mysql database
    with engine.begin() as conn:
        conn.execute(text(ddl))
def store_weather_to_db(weather_data: dict, conn_string: str) -> None:
    """Insert weather data into MySQL."""
    engine = create_engine(conn_string, pool_pre_ping=True) #pool_pre_ping - to insert data into the table at every instances
    ensure_weather_table(engine)
    try:
        df = pd.DataFrame([weather_data])
        df.to_sql("weather", engine, if_exists="append", index=False)
        print(f"Weather data for {weather_data['city']} stored successfully in MySQL.")
    finally:
        engine.dispose() #dispose is done to avoid garbage collection

def main():
    weather = fetch_weather(API_KEY, CITY)
    store_weather_to_db(weather, MYSQL_CONN_STRING)
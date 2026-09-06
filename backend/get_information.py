from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="Weather Forecast API Backend")

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search" #

@app.get("/geocode")
def get_coordinates(city_name: str):
    params = {"name": city_name, "count": 1, "format": "json"} #
    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("results")
        if not results:
            raise HTTPException(status_code=404, detail=f"City '{city_name}' not found.")
            
        # Extract the highest ranking match
        top_match = results[0]
        return {
            "city": top_match.get("name"),
            "country": top_match.get("country"),
            "latitude": top_match.get("latitude"),
            "longitude": top_match.get("longitude")
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Geocoding service error: {str(e)}")

@app.get("/weather")
def get_weather_forecast(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability",
        "timezone": "auto"
    }
    try:
        response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "current": data.get("current_weather"),
            "hourly_forecast": {
                "time": data.get("hourly", {}).get("time", []),
                "temperature": data.get("hourly", {}).get("temperature_2m", []),
                "humidity": data.get("hourly", {}).get("relative_humidity_2m", []),
                "rain_prob": data.get("hourly", {}).get("precipitation_probability", [])
            }
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch data from Open-Meteo: {str(e)}")


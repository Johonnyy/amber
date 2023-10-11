from app.moduleAPI import log, getCredential

import googlemaps
import requests
import datetime
import json


class GetWeather:
    def __init__(self):
        self.name = "GetWeather"
        self.description = "Get weather data."
        self.version = "1.0.0"
        self.parameters = {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city,state,and/or country to get the weather from. OPTIONAL. Not accepted values: tomorrow, today, next week, etc",
                }
            },
        }
        self.configOptions = [
            {
                "value": "googleMapsAPI",
                "title": "Google Maps API Key",
                "description": "The API key obtained from Google Cloud Maps Console.",
                "type": "text",
            },
            {
                "value": "openWeatherMap",
                "title": "Open Weather Map API Key",
                "description": "The API key obtained from https://openweathermap.org/. You must enable One Call API.",
                "type": "text",
            },
        ]
        self.requirements = ["googlemaps"]

    def handle(self, args):
        location = args.get("location", None)

        if not location:
            return "Prompt user for location and run again."

        gmapsKey = getCredential("base", "weather", self.name, "googleMapsAPI")

        if not gmapsKey:
            return "No Google Maps Key Set"

        gmaps = googlemaps.Client(key=gmapsKey)

        locationGeocode = gmaps.geocode(location)[0]
        locationCoords = {
            "lat": locationGeocode["geometry"]["location"]["lat"],
            "lon": locationGeocode["geometry"]["location"]["lng"],
        }

        log(locationCoords)

        apiKey = getCredential("base", "weather", self.name, "openWeatherMap")

        if not apiKey:
            return "No Weather API Key Provided"

        resultsHourlyResult = requests.get(
            f"https://api.openweathermap.org/data/3.0/onecall?lat={locationCoords['lat']}&lon={locationCoords['lon']}&appid={apiKey}&units=imperial&exclude=minutely,alerts,daily"
        )

        resultsHourlyResult = resultsHourlyResult.json()
        resultsHourly = resultsHourlyResult
        resultsHourly["hourly"] = resultsHourly["hourly"][::3]

        keys_to_remove = [
            "pressure",
            "humidity",
            "dew_point",
            "clouds",
            "visibility",
            "pop",
        ]

        for hour in resultsHourly["hourly"]:
            for key in keys_to_remove:
                if key in hour:
                    del hour[key]
            hour["time"] = datetime.datetime.fromtimestamp(hour["dt"]).strftime(
                "%d %B %Y %H:%M:%S"
            )

        resultsHourly["message"] = "Make answers concise and relevant."

        # FORMAT WEATHER

        resultsHourly["current"]["temp"] = round(resultsHourly["current"]["temp"])
        resultsHourly["current"]["feels_like"] = round(
            resultsHourly["current"]["feels_like"]
        )
        resultsHourly["current"]["uvi"] = round(resultsHourly["current"]["uvi"])

        for hour in resultsHourly["hourly"]:
            hour["temp"] = round(hour["temp"])
            hour["feels_like"] = round(hour["feels_like"])
            hour["uvi"] = round(hour["uvi"])
            hour["wind_speed"] = round(hour["wind_speed"])

        return json.dumps(resultsHourly, separators=(",", ":"))

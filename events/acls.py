from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import json
import requests

def get_photo(city, state):
    # pexels api request
    headers = {"Authorization": PEXELS_API_KEY}
    #  Create a dictionary for the headers to use in the request
    # Create the URL for the request with the city and state
    query = f'{city} {state}'
    url = f"https://api.pexels.com/v1/search?query={query}"
    response = requests.get(url, headers=headers)
    # Make the request
    # Parse the JSON response
    picture_url = response.json()["photos"][0]["src"]["original"]
    # Return a dictionary that contains a `picture_url` key and
    #   one of the URLs for one of the pictures in the response
    return {"picture_url": picture_url}


def get_weather_data(location):
    params = {
        "q": f'{location.city},{location.state.abbreviation},016',
        "appid": OPEN_WEATHER_API_KEY
    }
    url = 'http://api.openweathermap.org/geo/1.0/direct'
    response = requests.get(url, params)
    lat = response.json()[0]['lat']
    lon = response.json()[0]['lon']
    if lat == None or lon == None:
        return None

    params = {
        "units": "imperial",
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY,
    }
    url = 'https://api.openweathermap.org/data/2.5/weather'
    response = requests.get(url, params)
    description = response.json()["weather"][0]["description"]
    temperature = response.json()["main"]["temp"]
    return {
        "description": description,
        "temp": temperature
    }

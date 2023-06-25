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
def get_weather_data(city, state):
    pass
    # Create the URL for the geocoding API with the city and state
    # Make the request
    # Parse the JSON response
    # Get the latitude and longitude from the response

    # Create the URL for the current weather API with the latitude
    #   and longitude
    # Make the request
    # Parse the JSON response
    # Get the main temperature and the weather's description and put
    #   them in a dictionary
    # Return the dictionary

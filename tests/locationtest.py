from geopy.geocoders import Nominatim
import requests
import json
from typing import Tuple, Optional, Dict

def get_location():
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.geocode("me")

    if location:
        return location.latitude, location.longitude
    else:
        return None

latitude, longitude = get_location()

if latitude and longitude:
    print("Latitude:", latitude)
    print("Longitude:", longitude)
else:
    print("Unable to determine location.")




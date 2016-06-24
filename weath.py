from util import hook
from geopy.geocoders import Nominatim
from forecastiopy import *

APIKEY = '3cceb98d73bf72504f5c147ea6dcc97c'

def get_location(user_input):
    geolocator = Nominatim()
    location = geolocator.geocode(user_input)
    if not location:
        return False
    return location


def call_weather(location):
    loc_lat = location.latitude
    loc_lon = location.longitude
    fio = ForecastIO.ForecastIO(APIKEY,
                            units=ForecastIO.ForecastIO.UNITS_SI,
                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
                            latitude=loc_lat, longitude=loc_lon)
    return fio


@hook.command('w')
def get_weather(inp):
    user_loc = inp.lower().strip()
    location = get_location(user_loc)
    if not location:
        return 'I could not find weather for that location'
    fio = call_weather(location)
    daily = FIODaily.FIODaily(fio)
    return daily.summary
        # return '%s %s' %(location.latitude, location.longitude)

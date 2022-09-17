from geopy.geocoders import Nominatim


def convert_to_coord(adress_string):
    """takes a string and returns a tuple of coordinates using GeoNames"""
    geolocator = Nominatim(user_agent="GeoNames")
    location = geolocator.geocode(adress_string)
    try:
        return (location.latitude, location.longitude)
    except:
        return (None, None)
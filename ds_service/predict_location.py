import numpy as np

def predict_future_location(lat, long, speed, course, time):
    """
    Predicts the future location of a ship based on the current location, speed, course and time.
    """
    # Convert to radians
    lat = np.radians(lat)
    long = np.radians(long)
    course = np.radians(course)
    # Calculate the future distance travelled
    distance = speed * time
    # Calculate the new latitude, radius of earth=6371km
    new_lat = np.arcsin(np.sin(lat) * np.cos(distance / 6371) + np.cos(lat) * np.sin(distance / 6371) * np.cos(course))
    # Calculate the new longitude
    new_long = long + np.arctan2(np.sin(course) * np.sin(distance / 6371) * np.cos(lat), np.cos(distance / 6371) - np.sin(lat) * np.sin(new_lat))
    # Convert back to degrees
    new_lat = np.degrees(new_lat)
    new_long = np.degrees(new_long)
    return new_lat, new_long
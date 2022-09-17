import sys
import os
import time
from math import radians, cos, sin, asin, sqrt
import json
from service import get_shipment_information

import pandas as pd
import numpy as np

# Set sys path to search first in the project root
project_root = sys.path[0]
while os.path.basename(project_root) != "data_science":
    project_root = os.path.dirname(project_root)
sys.path.insert(0, project_root)

os.chdir(project_root)


def distance(lat1, lat2, lon1, lon2):

    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = np.radians(lon1)
    lon2 = np.radians(lon2)
    lat1 = np.radians(lat1)
    lat2 = np.radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2

    c = 2 * np.arcsin(np.sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return(c * r)
    
def check_if_ship_in_danger_zone(last_lat, last_long, pred_lat, pred_long, lat_w, long_w):
    x_lat = [last_lat + n/10*(pred_lat-last_lat) for n in range(10)]
    x_long = [last_long + n/10*(pred_long - last_long) for n in range(10)]
    dist_vector = [distance(x1, lat_w, x2, long_w) for (x1, x2) in zip(x_lat, x_long)]
    return min(dist_vector)


time_ = None
weather_warning_path = 'scraped_weather.csv'
pirates_warning_path = 'scraped_pirates.csv'
shipment_info = get_shipment_information(time_)

weather_warning = pd.read_csv(weather_warning_path)
pirates_warning = pd.read_csv

n_row = shipment_info.shape[0]
#shipment_info = shipment_info[:int(n_row/2)]

n_row = shipment_info.shape[0]
start_time = time.time()
for index, row in shipment_info[['last_latitude', 'last_longitude', 'predicted_latitude', 'predicted_longitude']].iterrows():
    last_lat, last_long = row['last_latitude'], row['last_longitude']
    pred_lat, pred_long = row['predicted_latitude'], row['predicted_longitude']

    for ct, loc in weather_warning[['geo_location']].iterrows():
        loc = loc['geo_location']
        # float(thetext.split(,)[0][1:]) and the other one float(thetext.split(,)[1][[:-1]])
        lat_w = float(loc.split(',')[0][1:])
        long_w =  float(loc.split(',')[1][1:-1])

        distance_computed = check_if_ship_in_danger_zone(last_lat, last_long, pred_lat, pred_long, lat_w, long_w)
        

        shipment_info.loc[ct, 'warning'] = weather_warning.loc[ct, 'Event_type']
        shipment_info.loc[ct, 'warning_distance'] = distance_computed
        shipment_info.loc[ct, 'Event'] = "Weather Warning"

    # for ct, loc in pirates_warning[['geo_location']].iterrows():
    #     loc = loc['geo_location']
    #     # float(thetext.split(,)[0][1:]) and the other one float(thetext.split(,)[1][[:-1]])
    #     lat_w = float(loc.split(',')[0][1:])
    #     long_w =  float(loc.split(',')[1][1:-1])

    #     distance_computed = check_if_ship_in_danger_zone(last_lat, last_long, pred_lat, pred_long, lat_w, long_w)
        

    #     shipment_info.loc[ct, 'warning'] = weather_warning.loc[ct, 'Event_type']
    #     shipment_info.loc[ct, 'warning_distance'] = distance_computed
    #     shipment_info.loc[ct, 'Event'] = "Weather Warning"

    if int((index/n_row)*1000) % 100 == 0:
        print(f"progress: {int((index/n_row)*100)}")

end_time = time.time()

print((end_time - start_time)/60)
# %%
# Analyze data to find treshold
shipment_info['warning_distance'].hist()

print(shipment_info.shape)
print(shipment_info['warning_distance'].unique())
print(shipment_info['warning_distance'].value_counts())
#%%

treshold_dist = 4000

shipment_info_red = shipment_info[shipment_info['warning_distance'] < treshold_dist]
print(shipment_info_red.shape)

#%%

shipment_info.to_pickle('data_for_backend/shipment_red_info_weather_warning.pkl')
shipment_info_red.to_pickle('data_for_backend/shipment_info_weather_warning.pkl')


#%%
# generate a json
print(shipment_info_red.columns)
shipment_json = dict()
warning_json = dict()

for idx, row in shipment_info_red.iterrows():
    shipment_json['warning_id'] = idx
    shipment_json['port_destination_name'] = row['pod_name']
    shipment_json['port_destination_country'] = row['pod_land']
    shipment_json['destination_location'] = row['empfaenger_ort']
    shipment_json['product_name'] = row['bb_name']

    warning_json['last_location'] = (row['last_latitude'], row['last_longitude'])
    warning_json['predicted_current_location'] = (row['predicted_latitude'], row['predicted_longitude'])
    warning_json['warning_text'] = row["warning"]
    warning_json['event'] = row['Event']
    warning_json['time'] = time_



print(shipment_json)
print(warning_json)


# %%

with open('data_for_backend/shipments.json', 'w') as fh:
    json.dump(shipment_json, fh)

with open('data_for_backend/warnings.json', 'w') as fh:
    json.dump(warning_json, fh)
# %%

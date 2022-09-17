#%%
import sys
import os
import time
from math import radians, cos, sin, asin, sqrt
import json

import pandas as pd
import numpy as np

#%% Set ds infrarstructure

##
# Set sys path to search first in the project root
project_root = sys.path[0]
while os.path.basename(project_root) != "data_science":
    project_root = os.path.dirname(project_root)
sys.path.insert(0, project_root)

os.chdir(project_root)



#%%
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


#%% read data

weather_warning_path = 'scraped_weather.csv'
shipment_info_path = 'current_shipment.csv'

weather_warning = pd.read_csv(weather_warning_path)
shipment_info = pd.read_csv(shipment_info_path)

#%%
n_row = shipment_info.shape[0]
#shipment_info = shipment_info[:int(n_row/2)]

n_row = shipment_info.shape[0]
start_time = time.time()
for index, row in shipment_info[['latitude', 'longitude']].iterrows():
    lat, long = row['latitude'], row['longitude']

    for ct, loc in weather_warning[['geo_location']].iterrows():
        loc = loc['geo_location']
        # float(thetext.split(,)[0][1:]) and the other one float(thetext.split(,)[1][[:-1]])
        lat_w = float(loc.split(',')[0][1:])
        long_w =  float(loc.split(',')[1][1:-1])

        distance_computed = distance(lat, long, lat_w, long_w)

        shipment_info.loc[ct, 'warning'] = weather_warning.loc[ct, 'Event_type']
        shipment_info.loc[ct, 'warning_distance'] = distance_computed

    if int((index/n_row)*100) % 10 == 0:
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
shipment_info_red['warning_id'] = shipment_info_red.index
print(shipment_info_red.shape)

##% Do some postprocessing

rename = {
    'pod_name': 'port_destination_name',
    'pod_land': 'port_destination_land',
    'pol_name': 'port_loading_name',
    'pol_land': 'port_loading_land',
}

shipment_info_red = shipment_info_red.rename(rename)

#%%

shipment_info.to_pickle('data_for_backend/shipment_red_info_weather_warning.pkl')
shipment_info_red.to_pickle('data_for_backend/shipment_info_weather_warning.pkl')


#%%
# generate a json
print(shipment_info_red.columns)
shipment_json = dict()
warning_json = dict()

for name, values in shipment_info_red.iteritems():

    if name in ['warning_id', '']
    shipment_json[name] =
    shipment_json['port_destination_name'] = row['pod_name']
    shipment_json['port_destination_land'] = row['pod_land']
    shipment_json['empfaenger_ort'] = row['empfaenger_ort']

    warning_json['location'] = (row['latitude'], row['longitude'])
    warning_json['warning_id'] = idx



print(shipment_json)
print(warning_json)


# %%

with open('data_for_backend/shipments.json', 'w') as fh:
    json.dump(shipment_json, fh)

with open('data_for_backend/warnings.json', 'w') as fh:
    json.dump(warning_json, fh)
# %%

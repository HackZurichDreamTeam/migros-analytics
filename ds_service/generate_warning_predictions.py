from datetime import datetime, timedelta
import pandas as pd
from service import get_shipment_information
import json
import numpy as np

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
    #this is not fully accurate, actually this should check on a geodescic line, but this works as an approximation
    x_lat = [last_lat + n/10*(pred_lat-last_lat) for n in range(10)]
    x_long = [last_long + n/10*(pred_long - last_long) for n in range(10)]
    dist_vector = [distance(x1, lat_w, x2, long_w) for (x1, x2) in zip(x_lat, x_long)]
    return min(dist_vector)

def generate_warning_predictions(weather_pred, current_time, threshold_dist): 
    current_time = pd.to_datetime(current_time)
    for pred_index, pred_row in weather_pred.iterrows():

        print("working on warning no.: " +str(pred_index))

        time_ = current_time + timedelta(hours=int(pred_row["time_from_now (h)"]))
        w_coord = pred_row["geo_location"]
        if w_coord == '(None, None)':
            continue
        lat_w = float(w_coord.split(',')[0][1:])
        long_w =  float(w_coord.split(',')[1][1:-1])
        shipment_info = get_shipment_information(time_)
        frames = []
        for index, row in shipment_info.iterrows():
            last_lat, last_long = row['last_latitude'], row['last_longitude']
            pred_lat, pred_long = row['predicted_latitude'], row['predicted_longitude']

            distance_computed = check_if_ship_in_danger_zone(last_lat, last_long, pred_lat, pred_long, lat_w, long_w)
            #distance_computed = distance(lat_w, pred_lat, long_w, pred_long)
            if distance_computed < threshold_dist:
                info = pd.DataFrame(row).T
                info['Event'] = "Weather Warning"
                info["Time"] = time_
                info["likelihood"] = pred_row["likelihood (%)"]
                info["Warning"] = pred_row["information"]
                frames.append(info)

    warnings_df = pd.concat(frames, axis=0)

    output_shipment = []
    output_warning = []
    pre_shipment_json_dict = {}
    pre_warning_json_dict = {}

    for idx, row in warnings_df.iterrows():
        pre_shipment_json_dict['warning_id'] = idx
        pre_shipment_json_dict['port_destination_name'] = row['pod_name']
        pre_shipment_json_dict['port_destination_country'] = row['pod_land']
        pre_shipment_json_dict['destination_location'] = row['empfaenger_ort']
        pre_shipment_json_dict['product_name'] = row['bb_name']
        pre_shipment_json_dict['route_coord'] = json.loads(row['route_coord'])

        pre_warning_json_dict['last_location'] = (row['last_latitude'], row['last_longitude'])
        pre_warning_json_dict['predicted_current_location'] = (row['predicted_latitude'], row['predicted_longitude'])
        pre_warning_json_dict['warning_text'] = row["Warning"]
        pre_warning_json_dict['event'] = row['Event']
        pre_warning_json_dict['time'] = str(time_)
        pre_warning_json_dict['likelihood'] = row["likelihood"]

        output_shipment.append(pre_shipment_json_dict)
        output_warning.append(pre_warning_json_dict)

    with open('data_for_backend/shipments_for_predicted_warnings.json', 'w') as fh:
        json.dump(output_shipment, fh)
    with open('data_for_backend/predicted_warnings.json', 'w') as fh:
        json.dump(output_warning, fh)


if __name__ == '__main__':
    current_time = "2021-08-15 00:00"
    weather_pred_path = 'scraped_weather_predictions.csv'
    weather_pred = pd.read_csv(weather_pred_path)

    threshold_dist = 4000
    generate_warning_predictions(weather_pred, current_time, threshold_dist)
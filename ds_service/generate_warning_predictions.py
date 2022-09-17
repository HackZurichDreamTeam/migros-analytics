import timedelta
import pandas as pd
from service import get_shipment_information
from generate_shipments_with_warnings import check_if_ship_in_danger_zone, distance, init_shipment_json

current_time = pd.to_datetime("2021-08-15 00:00")
weather_pred_path = 'scraped_weather_predictions.csv'
weather_pred = pd.read_csv(weather_pred_path)

threshold_dist = 4000

predicted_warnings_df = pd.DataFrame()

def init_predictions_json():
    warning_json = dict()
    warning_json['last_location'] = []
    warning_json['predicted_current_location'] = []
    warning_json['warning_text'] = []
    warning_json['event'] = []
    warning_json['time'] = []
    warning_json['likelihood'] = []

    return warning_json

for pred_index, pred_row in weather_pred.iterrows():

    time_ = current_time + timedelta(hours=pred_row["time_from_now (h)"]) 
    w_coord = row["geo_location"]
    lat_w = float(w_coord.split(',')[0][1:])
    long_w =  float(w_coord.split(',')[1][1:-1])
    shipment_info = get_shipment_information(time_)
    frames = []
    for index, row in shipment_info[['last_latitude', 'last_longitude', 'predicted_latitude', 'predicted_longitude']].iterrows():
        last_lat, last_long = row['last_latitude'], row['last_longitude']
        pred_lat, pred_long = row['predicted_latitude'], row['predicted_longitude']

        distance_computed = check_if_ship_in_danger_zone(last_lat, last_long, pred_lat, pred_long, lat_w, long_w)
        if distance_computed > threshold_dist:
            info = pd.DataFrame(row)
            info['Event'] = "Weather Warning"
            info["Time"] = time_
            info["likelihood"] = pred_row["likelihood (%)"]
            info["Warning"] = pred_row["information"]
            frames.append(info)

warnings_df = pd.concat(frames, axis=0)

shipment_json = init_shipment_json()
warning_json = init_predictions_json()

for idx, row in warnings_df.iterrows():
    shipment_json['warning_id'].append(idx)
    shipment_json['port_destination_name'].append(row['pod_name'])
    shipment_json['port_destination_country'].append(row['pod_land'])
    shipment_json['destination_location'].append(row['empfaenger_ort'])
    shipment_json['product_name'].append(row['bb_name'])
    shipment_json['route_coord'].append(row['route_coord'])

    warning_json['last_location'].append((row['last_latitude'], row['last_longitude']))
    warning_json['predicted_current_location'].append((row['predicted_latitude'], row['predicted_longitude']))
    warning_json['warning_text'].append(row["warning"])
    warning_json['event'].append(row['Event'])
    warning_json['time'].append(time_)



        
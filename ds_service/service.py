import os
import sys
import datetime as dt
import timedelta
import numpy as np

import pandas as pd

project_root = sys.path[0]
while os.path.basename(project_root) != "data_science":
    project_root = os.path.dirname(project_root)
sys.path.insert(0, project_root)

os.chdir(project_root)

from ds_service.predict_location import predict_future_location


def get_shipment_information(selected_date: str, current_time="2021-08-15 00:00") -> pd.DataFrame:
    """
    Returns the shipment information for the current_time (this is the "now"), selected_date should be 
    equal or after current_time, if a later date is given the location of ships for that later date will 
    be estimated.
    """
    if selected_date is None:
        selected_date = current_time

    selected_date = pd.to_datetime(selected_date)
    current_time = pd.to_datetime(current_time)
    
    assert selected_date >= current_time

    ##
    # Read data
    orders_path =  "data/gis_opex_international_bestellu.csv"
    raw_path = "data/gis_opex_international_raw.csv"
    shiptrac_path = "data/gis_opex_international_shiptrac.csv"


    bestellu = read_data(orders_path)
    raw = read_data(raw_path)
    shiptrack = read_data(shiptrac_path)

    ##get correct data -> active shipments which have not reached their destination
    raw["datum_abgang"]  = pd.to_datetime(raw["datum_abgang"])
    raw["datum_ankunft"]  = pd.to_datetime(raw["datum_ankunft"])
    active_shipments = raw[raw["datum_abgang"] <=current_time]
    active_shipments = active_shipments[active_shipments["datum_ankunft"] >current_time]

    # Get last recorded location of each shipment
    unique_ship_labels = np.unique(active_shipments['imo_nr'])
    shiptrack["date"] = pd.to_datetime(shiptrack["date"])
    shiptrack.sort_values(by="date", ascending = False, inplace=True)
    frames = []
    for ship_label in unique_ship_labels:
        last_info = shiptrack[shiptrack["imo_number"]==ship_label]
        last_info = last_info[last_info["date"]<=current_time]
        if len(last_info)>0:
            route_lat = np.array(last_info["latitude"])
            route_long = np.array(last_info["longitude"])
            info = pd.DataFrame(last_info.iloc[0]).T
            info['route_coord'] = str([(r_l, r_lo) for r_l, r_lo in zip(route_lat, route_long)])
            frames.append(info)
    shipment_info = pd.concat(frames, axis=0)
    shipment_info = shipment_info.rename(columns={'longitude': 'last_longitude', 'latitude': 'last_latitude'})


    # get shipment information
    shipment_info = shipment_info.merge(active_shipments, left_on='imo_number', right_on='imo_nr')
    shipment_info = shipment_info.merge(bestellu, left_on='bestellnummer', right_on='bestellnummer')

    shipment_info['predicted_location'] = shipment_info.apply(lambda x: predict_future_location(float(x.last_latitude), float(x.last_longitude), float(x.speed), float(x.course), timedelta.Timedelta(current_time - pd.to_datetime(x.date)).total.seconds/(60*60)), axis=1)
    shipment_info['predicted_latitude'] = shipment_info['predicted_location'].apply(lambda x: x[0])
    shipment_info['predicted_longitude'] = shipment_info['predicted_location'].apply(lambda x: x[1])

    col_to_keep = ['predicted_latitude', 'predicted_longitude', 'last_latitude', 'last_longitude', 'schiff', 'empfaenger', 'empfaenger_plz', 'empfaenger_ort', 'termin_empfaenger', 'bb_name', 'pod_name', 'pod_land', 'route_coord']

    shipment_info = shipment_info[col_to_keep]

    return shipment_info



def read_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";")

    return df

if __name__ == '__main__':
    project_root = sys.path[0]
    while os.path.basename(project_root) != "data_science":
        project_root = os.path.dirname(project_root)
    sys.path.insert(0, project_root)

    os.chdir(project_root)
    print(project_root)
    shipment_data = get_shipment_information("2021-08-15 00:00")
    shipment_data.to_csv("output.csv",mode='a', index=False, header=True)
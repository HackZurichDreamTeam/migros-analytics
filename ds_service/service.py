#%% Import packages
import os
import sys
import datetime as dt

import pandas as pd

#%% Set ds infrarstructure

##
# Set sys path to search first in the project root
project_root = sys.path[0]
while os.path.basename(project_root) != "data_science":
    project_root = os.path.dirname(project_root)
sys.path.insert(0, project_root)

os.chdir(project_root)


def get_shipment_information(selected_date: str) -> pd.DataFrame:
    if selected_date is None:
        selected_date = "2022-09-17"

    selected_date = pd.to_datetime(selected_date).date()

    ##
    # Read data
    orders_path =  "data/gis_opex_international_bestellu.csv"
    raw_path = "data/gis_opex_international_raw.csv"
    shiptrac_path = "data/gis_opex_international_shiptrac.csv"


    bestellu = read_data(orders_path)
    raw = read_data(raw_path)
    shiptrack = read_data(shiptrac_path)

    ##
    # Round the date only to a date now time
    shiptrack['date_round'] = pd.to_datetime(shiptrack['date']).date()

    ##
    # Get current shipment
    shipment_info = shiptrack[shiptrack['date_round'] == selected_date]

    shipment_info = shipment_info.merge(raw, left_on='imo_number', right_on='imo_nr')
    shipment_info = shipment_info.merge(bestellu, left_on='bestellnummer', right_on='bestellnummer')

    col_to_keep = ['longitude', 'latitude', 'shiff', 'empfaenger', 'empfaenger_plz', 'empfaenger_ort', 'termin_empfaenger', 'bb_name']

    shipment_info = shipment_info[col_to_keep]

    return shipment_info



def read_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";")

    return df

if __name__ == '__main__':

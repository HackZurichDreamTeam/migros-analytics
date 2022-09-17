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

##
# Set data science variables
orders_path =  "data/gis_opex_international_bestellu.csv"
raw_path = "data/gis_opex_international_raw.csv"
shiptrac_path = "data/gis_opex_international_shiptrac.csv"
#%%

bestellu = pd.read_csv(orders_path, sep=';')
raw = pd.read_csv(raw_path, sep=';')
shiptrack = pd.read_csv(shiptrac_path, sep=';')
print(bestellu.info())

#%%
print(raw.info())


#%% Do some preprocessing

shiptrack['date_round'] = pd.to_datetime(shiptrack['date']).apply(lambda dt_entry: dt_entry.round(freq="H"))



#%%
shiptrack['date_round'].max()




#%% Generate routes
selected_date_time = shiptrack['date_round'].max()

## select date
shiptrack_red = shiptrack[shiptrack['date_round'] == selected_date_time]

shiptrack_red = shiptrack_red.merge(raw, left_on='imo_number', right_on='imo_nr')
shiptrack_red = shiptrack_red.merge(bestellu, left_on='bestellnummer', right_on='bestellnummer')




# %%

# shiptrack join imo_nr raw join on bestellnummer on bestellu

shiptrack_red['name'].unique()


#%%
shiptrack_red.to_csv('current_shipment.csv', index=False)
# %%

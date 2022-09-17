#%% Import packages
import os
import sys

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

transport_info_path = "data/gis_opex_international_raw.csv"
#%%

orders = pd.read_csv(orders_path, sep=';')
trans_info = pd.read_csv(transport_info_path, sep=';')
print(orders.info())

#%%
print(orders.describe())


#%%
print(orders['bb_name'].value_counts())

print(orders[['termin_lieferant', 'termin_empfaenger']])

#%%
print(pd.to_datetime(orders['termin_lieferant']).max())




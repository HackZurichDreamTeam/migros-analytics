# Data Science Repository for the MIGROS CHALLENGE

To view our finished project see: [Supply Chain Resilience: Real-time Risk Warning at Hand](https://hackzurich22-4068.ew.r.appspot.com/admin/dashboard)

To use this repository download the migros shipping data ('gis_opex_international_bestellu.csv', etc.) in a folder called `data` inside data_science. Some basic analysis of this data can be found in the notebooks folder. 

As we did not have historical warning data but were only able to webscape current warnings for the purpose of this app and our analysis we have assumed that the current weather and piracy warnings that we have obtained are for the date "2021-08-15 00:00" which is in the middle of our migros data set. This allows us to show how real time warnings could be used to estimate real time shipment impacts. 

We have a separate repository [scraping-repo](https://github.com/HackZurichDreamTeam/scraping-repo) for data scraping. It is constantly scraping the web for data on storms and piracy information. Here we include the `csv` files from our initial web-scrapping runs in `scraped_data_example`.

The `ds_service` folder is where we generate json files with warnings and shipment details which are then used by the app, an example is shown in `data_for_backend` (using the scraped data in `scraped_data_example`). We apply a simple geographic algorithm to compute the most likely current location of ships based on their last transmitted locations and course information, this can be found in `predict_location`, an analysis of its accuracy and an explanation of its use can be explored in `notebooks/prediction_order_paths.ipynb`. 

The only exception is our shipment route delay estimate json files which are generated in `notebooks/analysis_delay.ipynb`.

Although this was not fully used by our app we additionally did web scaping on the `www.nhc.noaa.gov` weather warning website and this information can be used with our predictions of shipment location algorithms to predict if shipments will be effected by warnings in future. This can be seen in the `predictions` folder. 

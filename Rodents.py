import pandas as pd
from sodapy import Socrata
from secret import app_token,username,password
import folium
from folium.plugins import HeatMap



# Import necessary libraries
from sodapy import Socrata
import pandas as pd
import folium
from folium.plugins import HeatMap

def clean_rat_data(df_rodent, df_neighborhood):
    rodent = rodent.rename(columns={'date_trunc_y_inspection_date': 'inspection_date'})
    rodent['inspection_date'] = pd.to_datetime(rodent['inspection_date'])
    rodent['year'] = rodent.inspection_date.dt.to_period("Y")
    rodent['zip_code'] = rodent['zip_code'].astype(int)
    neighborhood['zip_code'] = neighborhood['zip_code'].astype(int)
    rodent = pd.merge(rodent, neighborhood, how="left", left_on='zip_code',right_on='zip_code')
    sightings = rodent[['zip_code', 'neighborhood', 'inspection_date', 'result', 'year']]
    return sightings

# Set up client authentication for Socrata API
client = Socrata("data.cityofnewyork.us",
                 app_token=app_token,
                 username=username,
                 password=password)

# Query data from the API and filter results by rat sightings in the past three years
results = client.get("p937-wjvj", select='date_trunc_y(inspection_date),zip_code,result,latitude,longitude',
                     order='date_trunc_y(inspection_date)',
                     where='result="Rat Activity" and latitude>0 and (date_trunc_y(inspection_date)="2019" or date_trunc_y(inspection_date)="2020" or date_trunc_y(inspection_date)="2021")',
                     limit=400000000)

# Convert the data to a pandas DataFrame for further processing
rodent = pd.DataFrame.from_records(results)

#Clean data
sightings = clean_rat_data(rodent, neighborhood)

# Group the data by neighborhood to get the count of rat sightings in each neighborhood
resultcount = sightings.groupby('neighborhood').result.count().reset_index()

# Create a new map object and add a heatmap layer to visualize the rat sightings
map_osm = folium.Map(location=[40.742, -73.956], zoom_start=11)
HeatMap(data=rodent[['latitude', 'longitude']].groupby(['latitude', 'longitude']).count().reset_index().values.tolist(),
        radius=7, max_zoom=10).add_to(map_osm)

# Save the map as an HTML file
map_osm.save('rat_heat_map.html')


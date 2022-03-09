import pandas as pd
from sodapy import Socrata
from secret import app_token,username,password
import folium
from folium.plugins import HeatMap



#API
client = Socrata("data.cityofnewyork.us",
                 app_token=app_token,
                 username=username,
                 password=password)

# QUERY RAT AND GROUP BY ZIP CODE, YEAR
results = client.get("p937-wjvj",select='date_trunc_y(inspection_date),zip_code,result,latitude,longitude',order= 'date_trunc_y(inspection_date)',where='result="Rat Activity" and latitude>0 and( date_trunc_y(inspection_date)="2019" or date_trunc_y(inspection_date)="2020" or date_trunc_y(inspection_date)="2021")', limit=400000000)
#print(results)
# # Convert to pandas DataFrame
rodent = pd.DataFrame.from_records(results)
#DATA CLEANING
rodent = rodent.rename(columns={'date_trunc_y_inspection_date': 'inspection_date'})
rodent['inspection_date'] = pd.to_datetime(rodent['inspection_date'])
rodent['year'] = rodent.inspection_date.dt.to_period("Y")
rodent['zip_code'] = rodent['zip_code'].astype(int)
neighborhood=pd.read_csv('nyc-zip-codes.csv')
neighborhood['zip_code'] = neighborhood['zip_code'].astype(int)
rodent = pd.merge(rodent, neighborhood, how="left", left_on='zip_code',right_on='zip_code')
sightings = rodent[['zip_code','neighborhood','inspection_date','result','year']]

#GROUP BY NEIGHBORHOOD
resultcount = sightings.groupby('neighborhood').result.count().reset_index()

#CREATE HEAT MAP AND SAVE
map_osm = folium.Map(location=[40.742, -73.956], zoom_start=11)
HeatMap(data=rodent[['latitude','longitude']].groupby(['latitude','longitude']).count().reset_index().values.tolist(), radius=7, max_zoom=10).add_to(map_osm)

map_osm.save('rat_heat_map.html')

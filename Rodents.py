import pandas as pd
from sodapy import Socrata
from secret import app_token,username,password
import json
import plotly.express as px


import seaborn as sns
import matplotlib.pyplot as plt

client = Socrata("data.cityofnewyork.us",
                 app_token=app_token,
                 username=username,
                 password=password)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("p937-wjvj",select='date_trunc_y(inspection_date),zip_code,result,count(result),latitude,longitude',order= 'date_trunc_y(inspection_date), count(result) desc',group="date_trunc_y(inspection_date),zip_code,result,latitude,longitude",where='result="Rat Activity" and latitude>0 and( date_trunc_y(inspection_date)="2020" or date_trunc_y(inspection_date)="2019" or date_trunc_y(inspection_date)="2018")', limit=2000000)
#print(results)
# # Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df = results_df.rename(columns={'date_trunc_y_inspection_date': 'inspection_date'}, index={'ONE': 'Row_1'})
results_df['inspection_date'] = pd.to_datetime(results_df['inspection_date'])
print(results_df)
sightings = results_df[['zip_code','inspection_date','count_result']]
print(sightings)


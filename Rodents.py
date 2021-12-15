import pandas as pd
from sodapy import Socrata
from secret import app_token,username,password



pd.set_option('display.max_columns', None)
client = Socrata("data.cityofnewyork.us",
                 app_token=app_token,
                 username=username,
                 password=password)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("p937-wjvj",select='date_trunc_y(inspection_date),zip_code,result,latitude,longitude',order= 'date_trunc_y(inspection_date)',where='result="Rat Activity" and latitude>0 and( date_trunc_y(inspection_date)="2018" or date_trunc_y(inspection_date)="2019" or date_trunc_y(inspection_date)="2020")', limit=3000)
#print(results)
# # Convert to pandas DataFrame
rodent = pd.DataFrame.from_records(results)
rodent = rodent.rename(columns={'date_trunc_y_inspection_date': 'inspection_date'})
rodent['inspection_date'] = pd.to_datetime(rodent['inspection_date'])
# print(rodent['inspection_date'])
rodent['year'] = rodent.inspection_date.dt.to_period("Y")
sightings = rodent[['zip_code','inspection_date','result','year']]
resultcount = sightings.groupby('zip_code')['result'].count()
print(resultcount)


print(sightings)
#
#enron= pd.merge(
#         results_df,
#         sightings,
#         how='left',
#         left_on=['inspection_date','zipcode'],
#         right_on=['inspection_date','zip_code']
#     )
# print(enron)
import pandas as pd
from sodapy import Socrata
from secret import app_token,username,password


client = Socrata("data.cityofnewyork.us",
                 app_token=app_token,
                 username=username,
                 password=password)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("43nn-pn8j", select='date_trunc_ymd(inspection_date),dba,zipcode,camis,cuisine_description,violation_code,grade,violation_description,score, critical_flag,inspection_type,latitude,longitude', limit=3000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df = results_df.rename(columns={'date_trunc_ymd_inspection_date': 'inspection_date'}, index={'ONE': 'Row_1'})
results_df['inspection_date'] = pd.to_datetime(results_df['inspection_date'])
results_df=results_df.dropna()

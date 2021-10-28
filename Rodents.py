import pandas as pd
from sodapy import Socrata
import datetime
import matplotlib.pyplot as plt
from secret import app_token,username,password
import seaborn as sns


client = Socrata("data.cityofnewyork.us",
                 app_token=app_token,
                 username=username,
                 password=password)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("p937-wjvj",select='date_trunc_ymd(inspection_date),zip_code,result,count(result)',order= 'date_trunc_ymd(inspection_date) desc',group="zip_code,date_trunc_ymd(inspection_date),result",where='result="Rat Activity"', limit=1000)
#print(results)
# # Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df = results_df.rename(columns={'date_trunc_ymd_inspection_date': 'inspection_date'}, index={'ONE': 'Row_1'})
results_df['inspection_date'] = pd.to_datetime(results_df['inspection_date'])
results_df = results_df.loc[results_df['inspection_date'].dt.year.isin([2017, 2018, 2019, 2020, 2021])]
#print(results_df['inspection_date'])



results = client.get("43nn-pn8j",select='camis,dba,boro,zipcode,cuisine_description,action,violation_code,violation_description,critical_flag,score,grade,inspection_type,date_trunc_ymd(inspection_date)',order= 'date_trunc_ymd(inspection_date) desc', where="boro='Manhattan'", limit=1000)

# Convert to pandas DataFrame
df_resto = pd.DataFrame.from_records(results)
df_resto = df_resto.rename(columns={'zipcode': 'zip_code','date_trunc_ymd_inspection_date': 'inspection_date'})
df_resto['inspection_date'] = pd.to_datetime(df_resto['inspection_date'])
df_resto = df_resto.loc[df_resto['inspection_date'].dt.year.isin([2017, 2018, 2019, 2020, 2021])]
#print(df_resto['zip_code'])#
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
result = df_resto.merge(results_df,how='left', on=["inspection_date","zip_code"])

import pandas as pd
from sodapy import Socrata
from matplotlib import pyplot as plt
import numpy as np
from secret import app_token,username,password
from datetime import datetime,date

def func(a_):
    if a_<=13:
        return 'A_rep'
    elif 13< a_<= 27:
        return 'B_rep'
    elif a_ > 27:
        return 'C_rep'

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
results_df['inspection_date']= pd.to_datetime(results_df['inspection_date'], errors='coerce').dt.date
results_df['score']=results_df['score'].dropna().astype(int)




results_df['c'] = results_df[['score']].apply(lambda x: func(x[0]), axis=1)
#print(results_df[['c', 'grade', 'score']])
#
# print(results_df['Range'])
#
# ## MISSING DATA
# # print(results_df.isna().sum())
#
#
results_df.isna().sum().reset_index(name="n").plot.bar(x='index', y='n', rot=45)
plt.show()
#
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
#
missing_grade=results_df[results_df['grade'].isnull()]


# cuisines = missing_grade.groupby('score').camis.count().reset_index().sort_values(by = 'score', ascending=False)
# print(cuisines)
#
# print(missing_grade['score'].unique())
not_missing=results_df[results_df['grade'].notnull()]

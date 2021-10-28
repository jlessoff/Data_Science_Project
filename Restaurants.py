import pandas as pd
from sodapy import Socrata
import matplotlib.pyplot as plt
from secret import app_token,username,password


client = Socrata("data.cityofnewyork.us",
                 app_token=app_token,
                 username=username,
                 password=password)

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("43nn-pn8j", where="boro='Manhattan'", limit=100)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df=results_df.drop(['phone', 'community_board', 'council_district', 'bin', 'bbl', 'nta'],axis=1)
results_df['inspection_date'] = pd.to_datetime(results_df['inspection_date'])
trim = results_df.loc[results_df['inspection_date'].dt.year.isin([2017, 2018, 2019, 2020, 2021])]
#

# plt.savefig('img/borosgrades.png')
count=results_df['grade'].value_counts().plot(kind='bar', color=['green','red','blue','yellow'])
plt.xlabel("Grade", labelpad=14)
plt.ylabel("Count of Grade", labelpad=14)
plt.show()

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
results = client.get("43nn-pn8j", where="boro='Manhattan'", limit=100)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df=results_df.drop(['phone', 'community_board', 'council_district', 'bin', 'bbl', 'nta'],axis=1)
results_df['inspection_date'] = pd.to_datetime(results_df['inspection_date'])
trim = results_df.loc[results_df['inspection_date'].dt.year.isin([2017, 2018, 2019, 2020, 2021])]
#
# plt.style.use('ggplot')
# sns.set(style='darkgrid')
# green = (0.3333333333333333, 0.6588235294117647, 0.40784313725490196)
# orange = (0.8666666666666667, 0.5176470588235295, 0.3215686274509804)


# plt.savefig('img/borosgrades.png')
count=results_df['grade'].value_counts().plot(kind='bar', color=['green','red','blue','yellow'])
plt.xlabel("Grade", labelpad=14)
plt.ylabel("Count of Grade", labelpad=14)
plt.show()

#results_df = results_df.loc[results_df['inspection_date'].dt.year.isin([2017, 2018, 2019, 2020,2021])]


#find highest number of critical flags per exam, grouping by inspection date and restaurant name
#results1=results_df.groupby(['critical_flag','dba','grade']).count().sort_values(by='grade', ascending=False)
#print(results_df)

#count of exams per restaurant
#results1=results_df.groupby(['dba']).count().sort_values(by='dba', ascending=False)


#
#
# results_df_critical=results_df[results_df['critical_flag'].isin(['Critical','Not Critical'])]
#
#
# print(results_df_critical)
#
# results=results_df['critical_flag']
# print(results)

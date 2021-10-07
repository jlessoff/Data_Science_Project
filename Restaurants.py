import pandas as pd
from sodapy import Socrata
from secret import app_token,username,password

client = Socrata("data.cityofnewyork.us",
                 app_token=app_token,
                 username=username,
                 password=password)


# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("43nn-pn8j", limit=100)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
print((results_df))
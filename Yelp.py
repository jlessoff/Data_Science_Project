# Define function to gather keys:
def get_keys(path):
    with open(path) as f:
        return json.load(f)


# Pull in keys and specifically draw out the api key. I have removed the specific path to the keys
# for security purposes:
keys = get_keys("/Users/'INSERTPATH'/yelp_api.json")
api_key = keys['J65Cnx9_2hwl_VndK1zLq4vK5b4GNwjwfmMz9RagM5gI4hUE_ZUifGEo9X1xj1LbqIMPSKbfj7rrK295GCAhjg6cwJItTpiK97oaMuMwSD0mgrT-_eyFw9m3d0tlYXYx']

# URL to pull data from:
url = 'https://api.yelp.com/v3/businesses/search'

# Identify headers:
headers = {'Authorization': 'Bearer {}'.format(api_key)}
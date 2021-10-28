import requests
import json


api_key='J65Cnx9_2hwl_VndK1zLq4vK5b4GNwjwfmMz9RagM5gI4hUE_ZUifGEo9X1xj1LbqIMPSKbfj7rrK295GCAhjg6cwJItTpiK97oaMuMwSD0mgrT-_eyFw9m3d0tlYXYx'
headers = {'Authorization': 'Bearer %s' % api_key}

url='https://api.yelp.com/v3/businesses/search'

params = {'term':'seafood','location':'New York City'}
req = requests.get(url, headers=headers)
parsed = json.loads(req.text)


#

url = 'https://api.yelp.com/v3/businesses/search'

params = {'location':'New York City'}
req = requests.get(url, params=params, headers=headers)

parsed = json.loads(req.text)
businesses = parsed["businesses"]
for business in businesses:
    print("Name:", business["name"])
    print("Rating:", business["rating"])
    print("Address:", " ".join(business["location"]["display_address"]))
    print("Phone:", business["phone"])
    print("\n")
    id = business["id"]
    url = "https://api.yelp.com/v3/businesses/" + id + "/reviews"
    req = requests.get(url, headers=headers)
    parsed = json.loads(req.text)
    reviews = parsed["reviews"]
    for review in reviews:
        print("User:", review["user"]["name"], "Rating:", review["rating"], "Review:", review["text"], "\n")







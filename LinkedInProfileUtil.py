import json
import pprint
import requests as req
from bs4 import BeautifulSoup as bs
from credentials import GOOGLE_CUSTOM_SEARCH_API_KEY, CUSTOM_SEARCH_ENGINE_ID

REQUEST_URL=  "https://www.googleapis.com/customsearch/v1"

params = {
    "key": GOOGLE_CUSTOM_SEARCH_API_KEY,
    "cx": CUSTOM_SEARCH_ENGINE_ID,
    "q": "l-birnbaum@northwestern.edu"
}

pp = pprint.PrettyPrinter(indent=4)

r = req.get(REQUEST_URL, params=params)
results = r.json()

# print json.dumps(results, indent=2)

profiles = [{
    "profile_url":item["formattedUrl"], 
    # "info":item["pagemap"]["person"][0],
    "hcard": item["pagemap"]["hcard"][0]
    } 
    for item in results["items"] if "www.linkedin.com/in" in item["formattedUrl"]]

# profiles = [ item for item in results["items"] if "www.linkedin.com/in" in item["formattedUrl"]]

print json.dumps(profiles, indent=2)
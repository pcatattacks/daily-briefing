# import pprint
import requests as req
# from bs4 import BeautifulSoup as bs
from config.search_credentials import GOOGLE_CUSTOM_SEARCH_API_KEY, CUSTOM_SEARCH_ENGINE_ID
import json

# REQUEST_URL=  "https://www.googleapis.com/customsearch/v1"

# params = {
#     "key": GOOGLE_CUSTOM_SEARCH_API_KEY,
#     "cx": CUSTOM_SEARCH_ENGINE_ID,
#     "q": "l-birnbaum@northwestern.edu"
# }

# pp = pprint.PrettyPrinter(indent=4)

# r = req.get(REQUEST_URL, params=params)
# results = r.json()

# # print json.dumps(results, indent=2)

# profiles = [{
#     "profile_url":item["formattedUrl"],
#     # "info":item["pagemap"]["person"][0],
#     "hcard": item["pagemap"]["hcard"][0]
#     }
#     for item in results["items"] if "www.linkedin.com/in" in item["formattedUrl"]]

# profiles = [ item for item in results["items"] if "www.linkedin.com/in" in item["formattedUrl"]]

# print json.dumps(profiles, indent=2)
# this works ^


def get_linkedin_profiles_by_query(query):
    REQUEST_URL=  "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_CUSTOM_SEARCH_API_KEY,
        "cx": CUSTOM_SEARCH_ENGINE_ID,
        "q": query
    }
    r = req.get(REQUEST_URL, params=params)
    # print(r)
    results = r.json()
    profiles = None
    try:
        profiles = [ {"profile_url":item["formattedUrl"], "hcard": item["pagemap"]["hcard"][0] } for item in results["items"] if "www.linkedin.com/in" in item["formattedUrl"]]
    except:
        # print "Something went wrong! The result of the request was:"
        # print(json.dumps(results, indent=2))
        pass
    return profiles

def get_job_title_from_linked_in(name):
    # print("get_job_title_from_linked_in", name)
    job_title = "No Job Title Found"

    linkedin_profiles = get_linkedin_profiles_by_query(name)

    if linkedin_profiles:

        # print(linkedin_profiles)

        hcard = linkedin_profiles[0]['hcard']

        if 'title' in hcard:
            job_title = hcard['title']

    return job_title


# This doesn't work, linkedin's gotten a lot smarter about preventing scraping.
# def get_linkedin_profile_details(profile_url):
#     headers = {
#         'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3",
#         # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         # 'accept-encoding': 'gzip, deflate, sdch, br'
#     }

#     res = req.get(profile_url, headers=headers)
#     data = res.text
#     print data
#     # print res.headers
#     # print dir(res)
#     # print res.status_code
#     soup = bs(data, features="html.parser")
#     print soup.find_all("div", id="summary")

# print profiles[0]["profile_url"]

# get_linkedin_profile_details(profiles[0]["profile_url"])

# import json, sys
# print json.dumps(get_linkedin_profiles_by_query(sys.argv[1]), indent=2)

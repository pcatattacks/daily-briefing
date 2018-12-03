#linkedin_interface.py

from linkedin import linkedin

API_KEY = '864xzehg34hjoc'
API_SECRET = 'UbrEYNPn2hMGLA7S'
RETURN_URL = 'https://github.com/pcatattacks/daily-briefing/'

authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
print(authentication.authorization_url)  # open this url on your browser
application = linkedin.LinkedInApplication(authentication)

result = application.search_profile(selectors=[{'people': ['andre', 'ehrlich']}], params={'keywords': 'northwestern'})

print(result)

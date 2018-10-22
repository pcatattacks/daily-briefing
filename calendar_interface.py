from __future__ import print_function
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

# Daily Breifing: Functional Architecture for Google Calendar

# Each Calendar is a list of Events
class Calendar:

    # events is a dictionary, of arrays
    events = {
        "daily": [], # List of events
        # "weekly": [], # list of days
        # "monthly": [] # list of weeks
        }

    ''' Initiate authorized service for gmail API with specified account '''
    def __init__(self, service, user_id, maxResults):
        self.service = service
        self.user_id = user_id
        self.maxResults = maxResults

    def get_next_ten_events(self):

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        print('Getting the upcoming 10 events')

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=self.maxResults,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            # print(start, "|", event['status'].upper(),"|", event['location'], "|", event['summary'])
        #     print('----------------------------------------------------------------------')


    # Reads out events of the Day
    # Time, Title, (maybe, Description and participants, or leave out til they ask)
    def get_daily_briefing(self):
        return 0

    # Keyword match to events in daily calendar.
    def tell_me_more_about_event(self, keywords_to_match, part_of_event):
        return 0




# Event is an object
class Event:

    time = "" # what format is time? UTC
    title = ""
    location = "" # (address)
    description = ""
    link = ""
    participants = []

    def __init__(self, time, title, location, description, link, participants):
        if time:
            self.time = time
        if title:
            self.title = title
        if location:
            self.location = location
        if description:
            self.description = description
        if link:
            self.link = link
        if participants:
            self.participants = participants

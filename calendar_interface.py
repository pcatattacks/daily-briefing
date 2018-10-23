# Daily Breifing: Functional Architecture for Google Calendar

from __future__ import print_function
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

# text to speech
# Text to Speech Modules
from gtts import gTTS
import os

# def speak(string, slow=False):
#     tts = gTTS(text=string, lang='en', slow=slow)
#     tts.save("daily_briefing_out.mp3")
#     os.system("mpg321 daily_briefing_out.mp3 -q")

# Each Calendar is a list of Events
class Calendar:

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

    ''' Get the next ten upcoming events'''
    def get_next_ten_events(self):

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        # print('Getting the upcoming 10 events')

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
            # print(start + ": " +event['summary'])
            # print(start, "|", event['status'].upper(),"|", event['location'], "|", event['summary'])
            return start + ": " + event['summary']

    ''' Reads out events of the Day '''
    def get_todays_events(self):
        # TODO THIS IS THE MAIN POINT
        return 0

    ''' Keyword match to events in daily calendar. '''
    def tell_me_more_about_event(self, keywords_to_match, part_of_event):
        return 0




class Event:

    time = "" # what format is time? UTC
    title = ""
    location = "" # (address)
    description = ""
    link = ""
    participants = []
    emails = []

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

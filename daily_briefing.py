''' Google API Modules '''
from __future__ import print_function
from googleapiclient.discovery import build
# from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools

'''
    This seems to avoid encoding errors, but notice that there are
    ascii codes in emails that are still not being encoded
    (e.g. "they#39;ll" should be "they'll"). NEED TO FIX

'''
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


from select import select

''' Text to Speech Modules '''
from gtts import gTTS
import os

''' Helper Modules '''
import datetime

''' Daily Briefing Modules '''
from mail_interface import *
from calendar_interface import *
from conversation_interface import *


''' The Daily Briefing Interface '''
# TODO Datetime formatting for timestamps
# TODO Interaction between calendar and mail information!! IMPORTANT
# TODO Handle encoding/decoding to avoid errors like the following ...
#  `UnicodeEncodeError: 'ascii' codec can't encode character u'\xe9' in position 46: ordinal not in range(128)`
# TODO Find good examples of emails that bolster calendar events in your personal email
# and write functions to create a good demo of our Daily Briefing app.

'''
    The DailyBriefing class
    * This is the center of our 'intelligent information system'.
    * It authorizes our use of google's calendar and mail apis.
    * Makes calls to our calendar interface to get information on upcoming events.
    * Makes calls to our mail interface (and # TODO LinkedIn) to get information
        relevant to calendar events.
'''

def dummy_func():
    return 0

class DailyBriefing:
    ''' If modifying these scopes, delete the file token.json. '''
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/calendar.readonly'
    ]

    ''' The user's email address. The special value 'me' used to indicate the authenticated user. '''
    user_id = 'me'

    ''' maxResults limits the number of items returned by api call '''
    maxResults = 5

    ''' Initiate authorized service for gmail API with specified account '''
    def __init__(self):
        store = file.Storage('config/token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('config/credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, store)

        ''' Authenticate api services to Google Mail and Calendar '''
        self.mail_service = build('gmail', 'v1', http=creds.authorize(Http()))
        self.cal_service = build('calendar', 'v3', http=creds.authorize(Http()))

        ''' Create a Mail & Calendar object '''
        self.mail = Mail(self.mail_service, self.user_id, self.maxResults)
        self.cal = Calendar(self.cal_service, self.user_id, self.maxResults)

    def test(self):

        print(''' Next 10 events on the Calendar ''')
        events = self.cal.get_next_ten_events()
        for event in events:
            speak(repr(event))

        # speak("Listing labels used by this gmail account!")
        # for label in self.mail.get_labels(): speak(label)


        ''' List messages that match query '''
        query_terms = ['hike', 'meet', 'see you']

        for query in query_terms:
            print("\n\n Querying messages for \""+ query +"\" ...\n\n" )
            for msg in self.mail.ListMessagesMatchingQuery(query): speak(msg)


        ''' The following labels yield good results for calendar events '''
        label_terms = ['IMPORTANT', 'CATEGORY_PERSONAL', 'STARRED', 'UNREAD']

        speak(''' Get messages that have a certain Label ''')
        for label in label_terms:
            # speak("Getting all "+ label+" messages \n\n")
            self.mail.ListMessagesWithLabels([label])


    '''
        Get information from email to bolster a calendar event
        Employ semantic 'cheap' tricks!
    '''
    def get_information_from_email_related_to_event(self, cal_event):
        # TODO This is the crux of the project
        pass

    def create_calendar_event_from_email(self, email_id):
        # TODO This is bonus points
        pass

    def converse(self):
        speak("Hello!")

        briefing_subject = ""
        events_to_brief = []
        # files_to_read = []
        event_counter = 0

        timeout = 3 # seconds

        while True:

            # Select what's ready to read/write/exceptions
            r, w, e = select([sys.stdin], [], [], 3)

            if sys.stdin in r:
                # Read user input and follow commands
                user_in = sys.stdin.readline()
                print("You printed ", user_in)

                if "schedule" in user_in and "today" in user_in:
                    briefing_subject = "Here are today's events...\n"
                    events_to_brief = self.cal.get_next_ten_events()

                # if "evening" in user_in and "week" in user_in:
                #     briefing_subject = "Here are this week's events after 5pm...\n"
                #     events_to_brief = self.cal.get_weeks_events_time_of_day("evening")

                events_to_brief = map(repr, events_to_brief)
                # files_to_read = map(create_file_to_speak, events_to_brief)

            # Read out next event
            if events_to_brief:
                # Introduce list of events (e.g. events for today/)
                if event_counter == 0:
                    speak(briefing_subject)

                # Read the next event in list
                speak(events_to_brief[event_counter])
                event_counter += 1



def main():

    daily_briefing = DailyBriefing()

    # daily_briefing.converse()

    # speak('''Good morning. Would you like to go over your agenda for
    # today? The weather outside is 70 degrees and sunny. you have a meeting with Dwayne The Rock
    # Johnson this morning at 6 A.M. Followed by a 2 hour lecture on the nature of space-time And
    # the possibility of a godless universe. At noon you have lunch with the General Secretary of the
    # United Nations. That is all of you scheduled events for the day.''', duration=10)

    # events = daily_briefing.cal.get_next_ten_events()
    # for event in events: speak(repr(event))

    messages = daily_briefing.mail.ListMessagesMatchingQuery('meeting')
    for m in messages:
        print(m)



if __name__ == '__main__':
    main()

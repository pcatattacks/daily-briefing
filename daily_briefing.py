''' Google API Modules '''
from __future__ import print_function
from googleapiclient.discovery import build
# from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools

from config.search_credentials import GOOGLE_CUSTOM_SEARCH_API_KEY, CUSTOM_SEARCH_ENGINE_ID
from LinkedInProfileUtil import get_linkedin_profiles_by_query
import json

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

        ''' Example usage of linkedin feature. '''
        print(get_linkedin_profiles_by_query("Pranav Dhingra"))

        print(''' Next 10 events on the Calendar ''')
        events = self.cal.get_next_ten_events()
        for i, event in enumerate(events):
            print(repr(event))


        speak(text='''Good morning. Would you like to go over your agenda for
        today? The weather outside is 70 degrees and sunny. you have a meeting with Dwayne The Rock
        Johnson this morning at 6 A.M. Followed by a 2 hour lecture on the nature of space-time And
        the possibility of a godless universe. At noon you have lunch with the General Secretary of the
        United Nations. That is all of you scheduled events for the day.''', title="long_read")

        events = daily_briefing.cal.get_next_ten_events()
        for event in events: print(repr(event))

        messages = daily_briefing.mail.ListMessagesMatchingQuery('meeting')
        for m in messages:
            print(repr(m))


        msgs = daily_briefing.mail.ListMessagesMatchingQuery("photos")
        for m in msgs:
            print(m)

        print("Listing labels used by this gmail account!")
        for label in self.mail.get_labels():
            print(label)


        '''
        List messages that match query
        '''

        query_terms = ['hike', 'meet', 'see you']

        for query in query_terms:
            print("\n\n Querying messages for \""+ query +"\" ...\n\n" )
            for msg in self.mail.ListMessagesMatchingQuery(query):
                print(msg)


        '''
        The following labels yield good results for calendar events
        '''

        label_terms = ['IMPORTANT', 'CATEGORY_PERSONAL', 'STARRED', 'UNREAD']

        print(''' Get messages that have a certain Label ''')
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

    # def create_calendar_event_from_email(self, email_id):
    #     # TODO This is bonus points
    #     pass

    def converse(self):

        ''' What is the user asking to be briefed on?'''
        briefing_subject = ""

        '''
        Initialize event_counter to -1 to start off with a prompt
        before reading list of todays events
        '''
        event_counter = -1

        ''' Timeout in seconds to wait for user input '''
        timeout = 3

        ''' the big loop that runs the show '''
        while True:

            ''' new_events_flag marks when user has made a request for a different set of events to be briefed on'''
            new_events_flag = 0

            ''' At start-up, ask the user for a commmand
            the default command is to list the events for today '''
            if event_counter < 0:
                speak("Hello! Would you like your daily briefing?", "intro_0")
                print(">>> (yes/no)")

                ''' Wait indefinitely for user input '''
                r, w, e = select([sys.stdin], [], [])
                event_counter = 0

            else:
                ''' If we've passed the introduction, wait 1.5 seconds for user input '''
                r, w, e = select([sys.stdin], [], [], 1.5)

            ''' If the user has said something, parse user input and follow their commands '''
            if sys.stdin in r:

                user_in = sys.stdin.readline()

                ''' the default is get_next_ten_events '''
                if "go" in user_in or "yes" in user_in: # "schedule" in user_in and "today" in user_in:
                    briefing_subject = "Ok, preparing today's events...\n"
                    # events_type = 'day'
                    new_events = self.cal.get_next_ten_events()
                    new_events_flag = 1

                ''' user input e.g.:  what are my events at tech? '''
                if "events at " in user_in:
                    location = user_in.split("events at ")[1] # location = tech
                    new_events = self.cal.getEventsAtLocation(location)
                    new_events_flag = 1

                ''' user input e.g.: what is my 10AM? '''
                if "AM" in user_in or "PM" in user_in:
                    words = user_in.split(" ")
                    time = words[len(words)-1]
                    new_events = self.cal.getEventsAtTime(time)
                    new_events_flag = 1

                ''' get more information about event from additional sources '''
                if "more info on last event" in user_in:
                    speak("getting more info on this event", "more_info_status")
                    # if events_to_brief:
                    #     speak(self.mail.get_information_from_email_related_to_event(events_to_brief[event_counter-1]))

                #''' get all nightly events '''
                # if "evening" in user_in and "week" in user_in:
                #     briefing_subject = "Here are this week's events after 5pm...\n"
                #     events_to_brief = map(repr, self.cal.get_weeks_events_time_of_day("evening"))

                if "stop" in user_in:
                    speak("stopping...", "stopping_status")
                    break

                if new_events_flag:
                    prepared_events = prepare_list_of_events_to_brief(new_events)

            ''' If there are events loaded for briefing... '''
            if prepared_events:

                ''' Read out next event '''
                skip = False
                while event_counter < len(prepared_events):

                    this_event = prepared_events[event_counter]

                    ''' If first event, introduce type of list of events (e.g. events for today/this week/meetings) '''
                    if event_counter == 0:
                        speak(text=briefing_subject, title="briefing_subject")

                    ''' Get sumplementary information from emails matching terms from summary '''
                    longest_word_in_summary = max(this_event.summary.split(" "), key=len)
                    if len(this_event.summary.split(" ")) > 3:
                        query = longest_word_in_summary
                    else:
                        query = this_event.summary
                    msgs = self.mail.ListMessagesMatchingQuery(query)

                    ''' Read event line-by-line so we can interrupt them and ask for more info to skip to next event'''
                    event_line_counter = 0
                    # while event_line_counter < len(this_event_text):

                    ''' print and read the event out loud '''
                    print_text_and_play_audio(repr(this_event), this_event.filename)

                    ''' Handling interruptions...
                    Listen for user input for 1.5 seconds '''
                    r, w, e = select([sys.stdin], [], [], 1.5) # wait for 1.5 seconds

                    '''
                    If user said something, read user input and follow commands
                    '''
                    if sys.stdin in r:
                        user_in = sys.stdin.readline()
                        # print("You entered ", user_in)

                        # TODO Sketch out what functionality for interrupting the event...
                        #       like asking for more information on the location or time or subject.

                        if "next event" in user_in or "skip" in user_in:
                            skip = True
                            break

                    ''' For this event, pull up the latest email related to it '''

                    speak("Pulling up the latest relevant email for " + query + "\n " + msgs[0].subject, "relevant_email_status_0")
                    speak(repr(msgs[0]), "relevant_email")

                    linkedin_profiles = get_linkedin_profiles_by_query(msgs[0].recipients[0])
                    if linkedin_profiles:
                        job_title = linkedin_profiles[0]['hcard']['title']
                        speak(job_title, 'job_title')

                    speak("Pulling up the latest relevant email for " + longest_word_in_summary + "\n ", "relevant_email_status_0")
                    # speak(repr(msgs[0]), "relevant_email")

                    ''' increment counter to read next event '''
                    event_counter += 1

                ''' We have read all the events prepared for the briefing '''
                speak(text="That concludes your briefing", title="conclusion")
                break


''' main() Runs when you type `$ python daily_briefing.py` in the cmd line '''
def main():
    ''' Initialize a DailyBriefing object, google api services, and our calendar and mail objects'''
    daily_briefing = DailyBriefing()

    ''' Test run api calls without dealing with the daily_briefing.converse() protocol '''
    # daily_briefing.test()

    daily_briefing.converse()

if __name__ == '__main__':
    main()

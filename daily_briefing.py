''' Google API Modules '''
from __future__ import print_function
from googleapiclient.discovery import build
# from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools

from config.search_credentials import GOOGLE_CUSTOM_SEARCH_API_KEY, CUSTOM_SEARCH_ENGINE_ID
from LinkedInProfileUtil import get_linkedin_profiles_by_query
import json

from user_profile import *

import sys


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
    def __init__(self, demo=False):

        token_path = 'config/token.json'
        credentials_path = 'config/credentials.json'
        if demo:
            token_path = 'demo_' + token_path
            credentials_path = 'demo_' + credentials_path

        store = file.Storage(token_path)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(credentials_path, self.SCOPES)
            creds = tools.run_flow(flow, store)

        ''' Authenticate api services to Google Mail and Calendar '''
        self.mail_service = build('gmail', 'v1', http=creds.authorize(Http()))
        self.cal_service = build('calendar', 'v3', http=creds.authorize(Http()))

        ''' create our little handmade user profile '''
        self.user = User("Andre", "email", "Northwestern", "-6:00")

        ''' Create a Mail & Calendar object '''
        self.mail = Mail(self.mail_service, self.user_id, self.maxResults, self.user)
        self.cal = Calendar(self.cal_service, self.user_id, self.maxResults, self.user)

        ''' Get user's email from google API'''
        profile = self.mail.get_user_profile()
        self.user.email = profile['emailAddress']


    def test(self):

        speak("\n\nTESTING DAILY BRIEFING INTERFACE\n\n", "test_0")

        # print(''' Example usage of linkedin feature. ''')
        # print(get_linkedin_profiles_by_query("Pranav Dhingra"))

        speak(''' Next 10 events on the Calendar ''', "test_0")
        events = self.cal.get_next_ten_events()
        for i, event in enumerate(events):
            speak(repr(event), "test_0")

        # print(''' Example of text to speech ''')
        # speak(text='''Good morning. Would you like to go over your agenda for
        # today? The weather outside is 70 degrees and sunny. you have a meeting with Dwayne The Rock
        # Johnson this morning at 6 A.M. Followed by a 2 hour lecture on the nature of space-time And
        # the possibility of a godless universe. At noon you have lunch with the General Secretary of the
        # United Nations. That is all of you scheduled events for the day.''', title="long_read")



        speak("get_next_ten_events", "test_0")
        events = self.cal.get_next_ten_events()
        for event in events: speak(repr(event), "test_1")

        print("ListMessagesMatchingQuery meeting ")
        messages = self.mail.ListMessagesMatchingQuery('meeting')
        for m in messages:
            speak(repr(m), "test_2")


        speak("ListMessagesMatchingQuery photos", "test_3")
        msgs = self.mail.ListMessagesMatchingQuery("photos")
        for m in msgs:
            speak(m, "test_4")

        speak("Listing labels used by this gmail account!", "test_5")
        for label in self.mail.get_labels():
            speak(label, "test_6")


        speak('''List messages that match query''', "test_7")
        query_terms = ['hike', 'meet', 'see you']

        for query in query_terms:
            speak("\nterm \""+ query +"\" ...\n\n" , "test_8")
            for msg in self.mail.ListMessagesMatchingQuery(query):
                speak(msg, "test_9")


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

    # input: timeout (integer): specify number of seconds to wait, 0 = no timeout
    def listen_for_user_input(self, timeout=120):

        # print("\n\n>>>")

        user_in = ""
        ''' Wait indefinitely for user input '''
        r, w, e = select([sys.stdin], [], [], timeout)

        ''' If the user has said something, parse user input and follow their commands '''
        if sys.stdin in r:

            user_in = sys.stdin.readline().lower() # make userinput all lowercase

        return user_in


    def get_job_title_from_linked_in(self, name):
        linkedin_profiles = get_linkedin_profiles_by_query(name)
        # speak(linkedin_profiles, "linkedin_status_0")
        if linkedin_profiles:
            hcard = linkedin_profiles[0]['hcard']
            if 'title' in hcard:
                job_title = hcard['title']
            else:
                job_title = "No Job Title Found"

        return job_title


    '''
        The parse_user_input function:
        input arg: user_in (string)
        Parses for keywords to make the appropriate Google API call
    '''
    def parse_user_input(self, user_in):

        new_events_flag = 0
        new_events = []
        briefing_subject = ""
        immediate_response = ""

        if not user_in:
            return new_events_flag, new_events, "No user input"

        if any(word in user_in for word in ["daily briefing", "today", "schedule"]):
            ''' the default is get_next_ten_events '''
            speak("Ok, preparing today's events...", "daily_briefing_response_0")
            # events_type = 'day'
            new_events = self.cal.get_todays_events()
            new_events_flag = 1
            briefing_subject = "Here are today's events"

        elif "events at " in user_in:
            ''' user input e.g.:  what are my events at tech? '''
            location = user_in.split("events at ")[1].rstrip() # location = tech
            new_events = self.cal.getEventsAtLocation(location)
            new_events_flag = 1
            briefing_subject = "Here are events at {}".format(location)

        elif "events with " in user_in:
            person = user_in.split("events with ")[1].rstrip() # location = tech
            new_events = self.cal.getEventsWithAttendees(person)
            new_events_flag = 1
            briefing_subject = "Here are events with {}".format(person)
        elif "evening" in user_in:
            new_events = self.cal.getEventsInRange("18", "23:59")
            new_events_flag = 1
            briefing_subject = "Here are events in the evening"
        elif "afternoon" in user_in:
            new_events = self.cal.getEventsInRange("12:01","17:59")
            new_events_flag = 1
            briefing_subject = "Here are the events in the afternoon"
        elif "morning" in user_in:
            new_events = self.cal.getEventsInRange("8","12")
            new_events_flag = 1
            briefing_subject = "Here are events in the morning"
        elif "events related to" in user_in:
            keyword = user_in.split("events related to ")[1].rstrip()
            new_events = self.cal.getEventsWithKeywordsInDescription(keyword)
            new_events_flag = 1
            briefing_subject = "Here are events related to {}".format(keyword)
        elif any(word in user_in for word in ["am", "pm"]):
            ''' user input e.g.: what is my 10AM? '''
            words = user_in.split()
            time = words[len(words)-1]
            if "am" in time:
                time = time.split("am")[0]
            else:
                time = time.split("pm")[0] + 12
            new_events = self.cal.getEventsAtTime(time)
            new_events_flag = 1
            briefing_subject = "Here is your event at {}".format(time)

        elif "last event" in user_in:
            ''' get more information about event from additional sources '''
            speak("getting more info on this event", "more_info_status")
            # getmoreinfofunc

        # ''' Parse requests for more information on something '''
        elif "tell me more about" in user_in:
            words = user_in.split()
            index = words.index("about")
            person_name = words[index+1:].join(" ")
            if event_counter == -1: # if events not pulled yet
                pass # TODO
            elif event_counter >= 0: # if we have events
                pass # TODO
            pass
        elif "who is" in user_in:
            words = user_in.split()
            index = words.index("is")
            person_name = words[index+1:].join(" ")
            if event_counter == -1: # if events not pulled yet
                pass # TODO
            elif event_counter >= 0: # if we have events
                pass # TODO
            pass
        # elif "wait" in user_in:
        else:
            speak("sorry, I don't know what to do for {}".format(user_in), "response_0")

        return new_events_flag, new_events, briefing_subject


    def preprocess_list_of_events(self, events):
        ''' preprocess new events before converting to spoken word '''
        for event in events:
            '''Remove your name from attendee list'''
            for attendee in event.attendees:
                if self.user.name == attendee:
                    event.attendees.remove(self.user.name)
                else:
                    ''' Linkedin for attendees '''
                    attendee += " ({})".format(self.get_job_title_from_linked_in(attendee))
            if event.creator == self.user.name:
                event.creator = "you"

            ''' Get sumplementary information from emails matching terms from summary '''
            if event.keyword:
                query = this_event.keyword
            else:
                longest_word_in_summary = max(event.summary.split(" "), key=len)
                if len(event.summary.split(" ")) > 3:
                    query = longest_word_in_summary
                else:
                    query = event.summary
            msgs = self.mail.ListMessagesMatchingQuery(query)

            ''' Pull up the latest email related to this event'''
            linkedin_profiles = None
            if msgs:
                event.related_email = "\n EMAIL RELATED TO QUERY \"" + query + "\":\n" + msgs[0].subject + "\n"
                # speak("\nRELATED EMAIL TO QUERY \"" + query + "\":\n" + msgs[0].subject + "\n", "relevant_email_status_0")
                # speak(repr(msgs[0]), "relevant_email")

        return events

    def converse(self):

        ''' What is the user asking to be briefed on?'''
        new_events_flag, new_events, briefing_subject = 0, [], "No results"

        ''' Timeout in seconds to wait for user input '''
        prepared_events = []

        ''' At start-up, wait for the user to give a commmand
            the default command should be to list the events for today '''
        speak("Hello, {}!".format(self.user.name.split()[0]), "intro_0")

        ''' Wait indefinitely for user input '''
        user_in = self.listen_for_user_input()

        ''' the big loop that runs the show '''
        while True:

            if not user_in:
                ''' If we've passed the introduction, wait 10.5 seconds for user input '''
                user_in = self.listen_for_user_input(10.5)

            ''' new_events_flag marks when user has made a request for a different set of events to be briefed on'''
            new_events_flag, new_events, briefing_subject = self.parse_user_input(user_in)
            user_in = ""

            if new_events_flag:
                new_events = self.preprocess_list_of_events(new_events)
                prepared_events = prepare_list_of_events_to_brief(new_events)
                new_events_flag = 0 # reset flag

            ''' If there are event files loaded for briefing... '''
            if prepared_events:

                ''' Read out next event '''
                for event_counter, this_event in enumerate(prepared_events):

                    ''' If first event, introduce type of list of events (e.g. events for today/this week/meetings) '''
                    if event_counter == 0:
                        speak(text=briefing_subject, title="briefing_subject")

                    print("\n\nEVENT ", event_counter)

                    ''' print and read the event out loud line by line '''
                    for i, line in enumerate(this_event.filenames):
                        print_text_and_play_audio(repr(this_event.lines[i]), this_event.filenames[i])

                        ''' Handling interruptions... '''
                        user_in = self.listen_for_user_input(timeout=5)
                        new_events_flag, new_events, briefing_subject = self.parse_user_input(user_in)
                        user_in = ""
                        if new_events_flag:
                            break

                    if new_events_flag:
                        break

                # If we have finished going through all prepared_events, reset the list of prepared events
                prepared_events = []

                ''' We have read all the events prepared for the briefing '''
                #speak(text="That concludes your briefing", title="conclusion")



''' main() Runs when you type `$ python daily_briefing.py` in the cmd line '''
def main():

    ''' Initialize a DailyBriefing object, google api services, and our calendar and mail objects'''

    num_args = len(sys.argv)

    if num_args > 1:
        if sys.argv[1] == 'demo':
            daily_briefing = DailyBriefing(demo=True)
    else:
        daily_briefing = DailyBriefing(demo=False)

    ''' Test run api calls without dealing with the daily_briefing.converse() protocol '''
    # daily_briefing.test()

    ''' Interactive Conversation with Daily Briefing Agent '''
    daily_briefing.converse()

if __name__ == '__main__':
    main()

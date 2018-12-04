''' Google API Modules '''
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

''' Linkedin Search '''
from config.search_credentials import GOOGLE_CUSTOM_SEARCH_API_KEY, CUSTOM_SEARCH_ENGINE_ID
from LinkedInProfileUtil import *
import json

'''
    This seems to avoid encoding errors,
    TODO Fix ascii codes in emails that are still not being encoded (e.g. "they#39;ll" should be "they'll").
'''
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

''' Text to Speech Modules '''
from gtts import gTTS
import os

''' Helper Modules '''
import datetime

''' Daily Briefing Modules '''
from mail_interface import *
from calendar_interface import *
from conversation_interface import *
from user_profile import *


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

    ''' Initiate authorized service for gmail API with specified account '''
    def __init__(self, demo=False):

        ''' If demo, The George McGovern Test email is used, and credentials already exist in demo_config'''
        if demo:
            token_path = 'demo_config/token.json'
            credentials_path = 'demo_config/credentials.json'
            self.user = user_dict["George"]

        else:
            ''' Config must be set up manually, see readme. '''
            token_path = 'config/token.json'
            credentials_path = 'config/credentials.json'

            ''' TODO create our little internal hand-made user profile automatically '''
            self.user = user_dict["Andre"]

        ''' Google API Authorization for EECS 338 Project'''
        store = file.Storage(token_path)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(credentials_path, self.SCOPES)
            creds = tools.run_flow(flow, store)

        ''' Authenticate api services to Google Mail and Calendar '''
        self.mail_service = build('gmail', 'v1', http=creds.authorize(Http()))
        self.cal_service = build('calendar', 'v3', http=creds.authorize(Http()))

        ''' Create Time Service '''
        self.time_service = time_interface.TimeService(demo)

        ''' Create a Mail & Calendar object '''
        self.mail = Mail(self.mail_service, self.user_id, self.user, self.time_service)
        self.cal = Calendar(self.cal_service, self.user_id, self.user, self.time_service)

        ''' Get user's email from google API'''
        profile = self.mail.get_user_profile()
        self.user.email = profile['emailAddress']


    def test(self):

        speak("\n\nTESTING DAILY BRIEFING INTERFACE\n\n", "test_0")

        print(self.mail.ListMessagesWithLabels(["UNREAD"]))

        # messages = self.mail.ListMessagesMatchingQuery("coffee")
        # for x in messages:
        #     print(x)
        # messages = self.mail.ListMessagesMatchingQuery("discussion")
        # for x in messages:
        #     print(x)
        # messages = self.mail.ListMessagesMatchingQuery("Lunch")
        # for x in messages:
        #     print(x)
        # messages = self.mail.ListMessagesMatchingQuery("Finance")
        # for x in messages:
        #     print(x)
        # messages = self.mail.ListMessagesMatchingQuery("Dinner")
        # for x in messages:
        #     print(x)

        # print(''' Example usage of linkedin feature. ''')
        print(get_linkedin_profiles_by_query("Pranav Dhingra"))
        print(get_job_title_from_linked_in("andreehrlich2019@u.northwestern.edu"))
        print(get_job_title_from_linked_in("PranavDhingra2019@u.northwestern.edu"))
        print(get_job_title_from_linked_in("Jeff Bezos"))

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


        speak("Listing labels used by this gmail account!", "test_5")
        speak(" ".join(self.mail.get_labels()), "test_6")


        speak('''List messages that match query''', "test_7")
        query_terms = ['Coffee', 'meet', 'Kellog', 'discuss', 'naf naf']

        for query in query_terms:
            print("\nterm \""+ query +"\" ...\n\n" , "test_8")
            messages = self.mail.ListMessagesMatchingQuery(query)
            if messages:
                for m in messages:
                    print(m, "test_9")


        '''
        The following labels yield good results for calendar events
        '''

        label_terms = ['IMPORTANT', 'CATEGORY_PERSONAL', 'STARRED', 'UNREAD']

        print(''' Get messages that have a certain Label ''')
        for label in label_terms:
            # speak("Getting all "+ label+" messages \n\n")
            print(self.mail.ListMessagesWithLabels([label]))



    '''
        The parse_user_input:
            Parses for keywords to make the appropriate Google API calls
        input:
            user_in: string
        output:
            new_events: list of events (can be empty)
            briefing_subject: string, phrase that ends with "{num_events} events {unique description of event list}"
            command: string, word to control daily_breifing playback.
    '''
    def parse_user_input(self, user_in):


        # ''' Input variables '''
        # user_in_keywords = []
        # api_call = "function to call"
        # breifing_subject_string = "You have {} events at/with {}".format(number_events, briefing_subject)



        ''' Initialize output variables'''
        new_events = []
        briefing_subject = ""
        command = None

        if not user_in:
            return new_events, "No user input", command

        if any(word in user_in for word in ["daily briefing", "today", "schedule"]):
            new_events = self.cal.get_todays_events()
            briefing_subject = "You have {} events today".format(len(new_events))

        elif "events at" in user_in:
            ''' user input e.g.:  what are my events at tech? '''
            words = user_in.split()
            index = words.index("at")
            location = " ".join(words[index+1:])
            new_events = self.cal.getEventsAtLocation(location)
            # if not new_events:
                # speak("No events at found.".format(location), "404")
            briefing_subject = "You have {} events at {}".format(len(new_events), location)

        elif "events with " in user_in:
            person = user_in.split("events with ")[1].rstrip() # location = tech
            new_events = self.cal.getEventsWithAttendees(person)
            briefing_subject = "You have {} events with {}".format(len(new_events), person)

        elif "free time" in user_in:
            new_events = self.cal.get_free_time()
            briefing_subject = "Here are times you have available:"

        elif "evening" in user_in:
            new_events = self.cal.getEventsInRange("18", "23:59")
            briefing_subject = "You have {} events in the evening".format(len(new_events))

        elif "afternoon" in user_in:
            new_events = self.cal.getEventsInRange("12:01","17:59")
            briefing_subject = "You have {} events in the afternoon".format(len(new_events))

        elif "morning" in user_in:
            new_events = self.cal.getEventsInRange("8","12")
            briefing_subject = "You have {} events in the morning".format(len(new_events))

        elif "events related to" in user_in:
            keyword = user_in.split("events related to ")[1].rstrip()
            new_events = self.cal.getEventsWithKeywordsInDescription(keyword)
            briefing_subject = "You have {} events related to {}".format(len(new_events), keyword)

        elif any(word in user_in for word in ["am", "pm", "AM", "PM"]):
            ''' user input e.g.: what is my 10AM? '''
            words = user_in.split()
            time = words[len(words)-1]
            if "am" in time:
                time = time.split("am")[0]
            else:
                time = time.split("pm")[0] + 12
            new_events = self.cal.getEventsAtTime(time)
            briefing_subject = "You have {} events at {}".format(len(new_events), time)

        elif "last event" in user_in:
            ''' get more information about event from additional sources '''
            speak("getting more info on this event", "more_info_status")

        #''' Parse requests for more information on something '''
        elif "about" in user_in:
            words = user_in.split()
            index = words.index("about")
            proper_noun = " ".join(words[index+1:]).lower()

            print("finding information about {}...".format(proper_noun))
            for contact_name in self.cal.contacts: # check if proper noun is a contact name
                # checking full name and first name
                if proper_noun in contact_name or proper_noun.split(" ")[0] in contact_name:
                    email, events = self.cal.contacts[contact_name]
                    linkedin_profiles = get_linkedin_profiles_by_query(email) # try
                    if not linkedin_profiles:
                        linkedin_profiles = get_linkedin_profiles_by_query(contact_name)
                    if not linkedin_profiles:
                        linkedin_profiles = get_linkedin_profiles_by_query(proper_noun)
                    if not linkedin_profiles:
                        speak("No linkedin profiles found related to {}.".format(proper_noun), "linked_in")
                    else:
                        speak(" --------------------------------------------------------------------", "linked_in")
                        speak("I found these profiles on linkedin related to {}:".format(proper_noun), "linked_in")
                        speak(json.dumps(linkedin_profiles, indent=2), "linked_in")
                        speak(" --------------------------------------------------------------------", "linked_in")
                        # speak(, linkedin_profiles)
                        # TODO - the above needs to be spoken

            for location in self.cal.locations:
                if proper_noun in location or proper_noun.split(" ")[0] in location:
                    events = self.cal.locations[location]
                    print(" ------------------------------------------------- ")
                    print("I found the following events at {}:".format(location))
                    for event in events:
                        print(Event(event))
                    print(" ------------------------------------------------- ")
                    # TODO - the above needs to be spoken and formatted

        elif "who is" in user_in:
            words = user_in.split()
            index = words.index("is")
            proper_noun = " ".join(words[index+1:]).lower()

            print("finding information about {}...".format(proper_noun))
            for contact_name in self.cal.contacts: # check if proper noun is a contact name
                # checking full name and first name
                if proper_noun in contact_name or proper_noun.split(" ")[0] in contact_name:
                    email, events = self.cal.contacts[contact_name]
                    linkedin_profiles = get_linkedin_profiles_by_query(email) # try
                    if not linkedin_profiles:
                        linkedin_profiles = get_linkedin_profiles_by_query(contact_name)
                    if not linkedin_profiles:
                        linkedin_profiles = get_linkedin_profiles_by_query(proper_noun)
                    if not linkedin_profiles:
                        print("No linkedin profiles found related to {}.".format(proper_noun))
                    else:
                        print(" --------------------------------------------------------------------")
                        print("I found these profiles on linkedin related to {}:".format(proper_noun))
                        print(json.dumps(linkedin_profiles, indent=2))
                        print(" --------------------------------------------------------------------")
                        # speak(, linkedin_profiles)

        elif "wait" in user_in:
            user_in_2 = listen_for_user_input()
            prepared_events, briefing_subject, command = self.parse_user_input(user_in_2)

        elif "resume" in user_in:
            pass
        elif any(word in user_in for word in ["skip", "next"]):
            command = "skip"
        elif any(word in user_in for word in ["stop", "quit", "exit"]):
            command = "stop"
        else:
            speak("sorry, I don't know what to do for {}".format(user_in), "response_0")

        ''' Preproccess and prepare events to speak out loud '''
        new_events = self.preprocess_list_of_events(new_events)

        # prepared_events = prepare_list_of_events_to_speak(new_events, briefing_subject)
        # if not prepared_events:
        #     speak(briefing_subject, "response_0")
        return prepared_events, briefing_subject, command


    # def get_events_at_location(user_in, subject):
    #     ''' user input e.g.:  what are my events at tech? '''
    #     words = user_in.split()
    #     index = words.index("at")
    #     location = " ".join(words[index+1:])
    #     new_events = self.cal.getEventsAtLocation(location)
    #     briefing_subject = "{} "events at {}".format(len(new_events), location)
    #     return new_events, briefing_subject
    #
    # def handle_user_input(self, user_in):
    #
    #     ''' List of dicts that contain the keywords to call different functions '''
    #     user_input_cases = [
    #         # {
    #         #     "subject": "example_format",
    #         #     "keywords": [],
    #         #     "function_call": None,
    #         #     "briefing_subject": "You have {} events at/with {}"
    #         # },
    #         {
    #             "subject": "events_today"
    #             "keywords": ["daily briefing", "today", "schedule"],
    #             "function_call": self.cal.get_todays_events
    #         },
    #         {
    #             "subject": "events_at_location",
    #             "keywords": ["events at"],
    #             "function_call": self.get_events_at_location
    #         }
    #     ]
    #
    #     ''' initialize output '''
    #     events = []
    #     briefing_subject = "No Events Found"
    #
    #     for case in user_input_cases:
    #         if any(word in user_in for word in case['keywords']):
    #             events = case['function_call']()
    #             briefing_subject = "{} ".format(len(events)) + case["subject"].format(len(events))
    #             break
    #
    #     ''' Preproccess events to get related email, replace user's name with 'you' '''
    #     preprocessed_events = self.preprocess_list_of_events(events)
    #
    #     return preprocessed_events, briefing_subject

    def preprocess_list_of_events(self, events):

        if not events:
            return events

        ''' preprocess new events before converting to spoken word '''

        for event_number, event in enumerate(events):

            '''Remove your name from attendee list'''
            for attendee in event.attendees:

                if self.user.name == attendee:
                    event.attendees.remove(self.user.name)

            if event.creator == self.user.name:
                event.creator = "you"

            ''' Get sumplementary information from emails matching terms from summary '''
            if not event.keywords:
                ''' get keywords from longest word in event summary '''
                queries = [max(event.summary.split(" "), key=len)]
            else:
                queries = event.keywords

            ''' Try to get an email that matches all queries together'''
            query = " ".join(queries)
            emails_matching_query = self.mail.ListMessagesMatchingQuery(query)
            if emails_matching_query:
                for email in emails_matching_query:
                    if email not in event.related_emails:
                        event.related_emails.append(email)
            else:
                ''' Else get emails by queries individually '''
                for query in queries:
                    emails_matching_query = self.mail.ListMessagesMatchingQuery(query)
                    if emails_matching_query:
                        for email in emails_matching_query:
                            if email not in event.related_emails:
                                event.related_emails.append(email)

            ''' # TODO Get list of LinkedIn Profiles from attendees and emails'''
            linkedin_profiles = None

            ''' Turn event into a list of strings that can be read by google text-to-speech '''
            event.generate_lines(event_number)

        return events

    def converse(self):

        ''' What is the user asking to be briefed on?'''
        new_prepared_events = []
        prepared_events = []
        briefing_subject = "No results"
        command = None

        ''' Introduce Yourself '''
        speak("Hello, {}! Welcome to Daily Briefing.".format(self.user.name.split()[0]), "intro_0")

        ''' Wait indefinitely for user input '''
        user_in = listen_for_user_input()

        ''' the big loop that runs the show '''
        while True:

            ''' If there were new events (say from an interruption) transfer to prepared_events variable '''
            if new_prepared_events:
                prepared_events = new_prepared_events
            else:
                ''' Else, we need to figure out what events to prepare.
                    If user hasn't said anything, wait for them to say something '''
                if not user_in:
                    ''' If we've passed the introduction, wait 10 seconds for user input '''
                    user_in = listen_for_user_input(10)

                ''' Parse user input to determine which events to brief'''
                prepared_events, briefing_subject, command = self.parse_user_input(user_in)

            ''' Clear user_in variable '''
            user_in = ""

            ''' If there are event files loaded for briefing... '''
            if prepared_events:

                ''' Introduce list of events '''
                speak(text=briefing_subject, title="briefing_subject")

                ''' Read out the events '''
                for event_counter, this_event in enumerate(prepared_events):

                    print("\n")
                    command = None

                    ''' print and read the event out loud line by line '''
                    for line_number, line in enumerate(this_event.filenames):

                        print_text_and_play_audio(repr(this_event.lines[line_number]), this_event.filenames[line_number])

                        ''' Handling interruptions... '''
                        user_in = listen_for_user_input(timeout=0.5)

                        ''' Parse user input to determine which events to brief'''
                        new_prepared_events, briefing_subject, command = self.parse_user_input(user_in)

                        if command == "stop" or command == "skip":
                            break

                        ''' If the user did ask for a new set of events, break '''
                        if new_prepared_events:
                            break

                    if command == "stop":
                        speak("Stopping", "conclusion_3")
                        command = None
                        break

                    if new_prepared_events:
                        break

                ''' If we have finished going through all prepared_events, clear the list '''
                prepared_events = []

                if not new_prepared_events:
                    ''' We have read all the events prepared for the briefing '''
                    speak(text="That is all of the events you requested.\nWould you like to go over something else?\n", title="conclusion_0")

            # elif user_in:
            #     speak(text="No related events found.\n\n", title="conclusion_1")



''' main() Runs when you type `$ python daily_briefing.py` in the cmd line '''
def main():

    ''' Parse command line arguments for demo and test'''
    use_demo_config = False
    run_test = False
    speak = False

    arguments = sys.argv
    if "demo" in arguments:
        use_demo_config = True
    if "test" in arguments:
        run_test = True
    if "speak" in arguments:
        speak = True

    ''' Initialize a DailyBriefing object, google api services, and our calendar and mail objects'''
    daily_briefing = DailyBriefing(demo=use_demo_config)


    if run_test:
        ''' Test run api calls without dealing with the daily_briefing.converse() protocol '''
        daily_briefing.test()
    else:
        ''' Interactive Conversation with Daily Briefing Agent '''
        daily_briefing.converse()

if __name__ == '__main__':
    main()

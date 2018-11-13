# Daily Breifing: Functional Architecture for Google Calendar
# TODO Proper api calls for events of the day
# TODO Api calls for events matching a query (like meetings, tests, trips, etc...)
# TODO Parse calendar obj returned from google into a simpler custom 'Event'
# object for easier use by our DailyBriefing class.

# Modules
from datetime import *
from apiclient import errors


''' Helper Functions '''
''' Convert timestamps into human readable format

    e.g.    Start time: 2014-06-03 09:00 AM
            End time: 2014-06-03 10:00 AM

'''
def cal_datetime_to_readable(datetime_in):
    s = datetime.strptime(datetime_in,"%Y-%m-%dT%H:%M:%S-06:00")

    ss = "{} {}".format(s.date(),s.time().strftime( "%I:%M %p" ))

    return s


'''
    The Calendar Class
    # TODO Proper api calls for events of the day
    # TODO Api calls for events matching a query (like meetings, tests, trips, etc...)

'''
class Calendar:

    now = datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
    end_of_day = now + timedelta(days=1)
    end_of_day = (now + timedelta(hours=24)).isoformat() + 'Z'

    events = {
        "daily": [], # List of events
        # "weekly": [], # list of days
        # "monthly": [] # list of weeks
        }

    ''' Initiate authorized service for gmail API with specified account '''
    def __init__(self, service, user_id, maxResults, user):
        self.service = service
        self.user_id = user_id
        self.user = user
        self.maxResults = maxResults

    ''' Get the next ten upcoming events'''
    def get_next_ten_events(self):

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        # end_of_day = now + timedelta()
        # print('Getting the upcoming 10 events')

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=self.maxResults,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        events_processed = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            events_processed.append(Event(event))

        return events_processed

    ''' Reads out events of the Day '''
    def get_todays_events(self):
        # Call the Calendar API
        now = datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        end_of_day = now + timedelta(days=1)

        now = now.isoformat() + 'Z'
        end_of_day = end_of_day.isoformat() + 'Z'
        # print('Getting the upcoming 10 events')

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
            # maxResults=self.maxResults,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        events_processed = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            events_processed.append(Event(event))

        return events_processed

    ''' Keyword match to events in daily calendar. '''
    def tell_me_more_about_event(self, keywords_to_match, part_of_event):
        return 0

    def getEventsWithAttendees(self, attendee):
        print('getEventsWithAttendees ', attendee)
        now = datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        end_of_day = now + timedelta(days=1)

        now = now.isoformat() + 'Z'
        end_of_day = end_of_day.isoformat() + 'Z'
        # print('Getting the upcoming 10 events')

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
            # maxResults=self.maxResults,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        resultEvents = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            for personAttend in event['attendees']:
                realPerson = personAttend.get('displayName')
                print(personAttend)
                if attendee.upper() == realPerson.upper():
                    resultEvents.append(event)
                    break;
        events_processed = []
        for event in resultEvents:
            events_processed.append(Event(event))
        return events_processed


    def getEventsAtTime(self, time):
        print('getEventsAtTime', time)
        now = datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        end_of_day = now + timedelta(days=1)

        now = now.isoformat() + 'Z'
        end_of_day = end_of_day.isoformat() + 'Z'
        # print('Getting the upcoming 10 events')

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
            # maxResults=self.maxResults,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        resultEvents = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start)
            if time == start:
                resultEvents.append(event)
        events_processed = []
        for event in resultEvents:
            events_processed.append(Event(event))
        return events_processed

    def getEventsAtLocation(self, location):
        now = datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        end_of_day = now + timedelta(days=1)

        now = now.isoformat() + 'Z'
        end_of_day = end_of_day.isoformat() + 'Z'
        # print('Getting the upcoming 10 events')

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
            # maxResults=self.maxResults,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        resultEvents = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            if location.upper() == event['location'].upper():
                resultEvents.append(event)
        events_processed = []
        for event in resultEvents:
            events_processed.append(Event(event))
        return events_processed


    def getEventsWithKeywordsInTitle(self, keywords):


        print('getEventsWithKeywordsInTitle, ', keywords)
        now = datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        end_of_day = now + timedelta(days=1)

        now = now.isoformat() + 'Z'
        end_of_day = end_of_day.isoformat() + 'Z'
        # print('Getting the upcoming 10 events')

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
            # maxResults=self.maxResults,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        resultEvents = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            for word in keywords:
                if word in event['summary']:
                    resultEvents.append(event)
        events_processed = []
        for event in resultEvents:
            events_processed.append(Event(event))
        return events_processed


    def getEventsWithKeywordsInDescription(self, keywords):


        print('getEventsWithKeywordsInDescription', keywords)
        now = datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        end_of_day = now + timedelta(days=1)

        now = now.isoformat() + 'Z'
        end_of_day = end_of_day.isoformat() + 'Z'
        # print('Getting the upcoming 10 events')

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
            # maxResults=self.maxResults,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        resultEvents = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            for word in keywords:
                if word in event['description']:
                    resultEvents.append(event)
        events_processed = []
        for event in resultEvents:
            events_processed.append(Event(event))
        return events_processed

    def eventIsConfirmed(self, eventTitle):


        print('eventIsConfirmed,' + eventTitle + "?")
        now = datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        end_of_day = now + timedelta(days=1)

        now = now.isoformat() + 'Z'
        end_of_day = end_of_day.isoformat() + 'Z'
        # print('Getting the upcoming 10 events')

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
            # maxResults=self.maxResults,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        for event in events:
            print(eventTitle)
            if event['summary'] == eventTitle:
                if event['status'] == "confirmed":
                    print('True')
                else:
                    print('False')



# TODO Parse calendar obj returned from google into a simpler custom 'Event'
# object for easier use by our DailyBriefing class.


'''
    The Calendar Class
    # TODO Parse calendar obj returned from google into a simpler custom 'Event'
        object for easier use by our DailyBriefing class.

'''

class Event:

    summary = ''
    start = "" # what format is time? UTC
    end = ""
    location = "" # (address)
    description = ""
    creator = ""
    # organizer = ""
    attendees = []
    # link = ""
    # source = ""
    # attachments = []
    keyword = ""
    # relevant_emails = []

    def __init__(self, event):

        self.start = cal_datetime_to_readable(event['start']['dateTime'])
        self.end = cal_datetime_to_readable(event['start']['dateTime'])
        self.id = event['id']

        if 'summary' in event:
            self.summary = event['summary']
            if "meeting with" in self.summary:
                self.attendees.append(self.summary.split("with")[1].split("to discuss")[0])
                self.keyword = self.summary.split("with")[1].split("to discuss")[1]
        if 'location' in event:
            self.location = event['location']
        if 'description' in event:
            self.description = event['description']
        if 'link' in event:
            self.link = event['link']
        if 'attendees' in event:
            for x in event['attendees']:
                if 'displayName' in x:
                    event_attendee = x['displayName'].encode('utf-8')
                    if event_attendee not in self.attendees:
                        self.attendees.append(event_attendee)


    def __repr__(self, type='day'):
        out_str = '{} at {}\n' #'start: {}\nend: {}\n'
        format_arg_list = [self.summary, self.start.time().strftime( "%I:%M %p" )] #, self.start, self.end]

        if self.location:
            out_str += 'Location: {}\n'
            format_arg_list.append(self.location.split(",")[0])

        if self.description:
            out_str += 'Description: {}\n'
            format_arg_list.append(self.description)

        if self.creator:
            out_str += 'Creator: {}\n'
            format_arg_list.append(self.creator)

        if self.attendees:
            out_str += 'Attendees: {}\n'
            format_arg_list.append(self.attendees)

        return out_str.format(*format_arg_list)

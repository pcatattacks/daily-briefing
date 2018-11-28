# Daily Breifing: Functional Architecture for Google Calendar
# TODO Proper api calls for events of the day
# TODO Api calls for events matching a query (like meetings, tests, trips, etc...)
# TODO Parse calendar obj returned from google into a simpler custom 'Event'
# object for easier use by our DailyBriefing class.

# Modules
from datetime import *
from apiclient import errors
import pytz
import datetime
import time_interface

'''
    The Calendar Class
    # TODO Proper api calls for events of the day
    # TODO Api calls for events matching a query (like meetings, tests, trips, etc...)

'''
class Calendar:

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
        # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        now = time_interface.datetime_now_fake
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

    def getEventsInRange(self, timeStart, timeEnd):
        time_zone = pytz.timezone('America/Chicago')
        date = datetime.datetime.now().date()
        if ":" in timeStart:
            minute = int(timeStart.split(":")[1])
            hour = int(timeStart.split(":")[0])
        else:
            minute = 0
            hour = int(timeStart)

        if ":" in timeEnd:
            minuteEnd = int(timeEnd.split(":")[1])
            hourEnd = int(timeEnd.split(":")[0])
        else:
            minuteEnd = 0
            hourEnd = int(timeEnd)
        timeStartF = datetime.time(hour, minute)
        timeEndF = datetime.time(hourEnd, minuteEnd)
        date_time_end = datetime.datetime.combine(date, timeEndF)
        date_time = datetime.datetime.combine(date, timeStartF)
        date_time_end = time_zone.localize(date_time_end)
        date_time = time_zone.localize(date_time)
        date_time_end = date_time_end.strftime('%Y-%m-%dT%H:%M:%S-06:00')
        date_time = date_time.strftime('%Y-%m-%dT%H:%M:%S-06:00')

        # Call the Calendar API
        # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        now = time_interface.datetime_now_fake
        endOfDay = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat() + 'Z'

        print('Getting today\'s events')
        events_result = self.service.events().list(calendarId='primary', timeMin=date_time, timeMax = date_time_end,
                                            singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
        events_processed = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            events_processed.append(Event(event))
        return events_processed

    def get_todays_events(self):
        # Call the Calendar API
        # now = datetime.datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        # now = time_interface.datetime_now_fake
        # end_of_day = now + timedelta(days=1)

        # now = now.isoformat() + 'Z'
        now = time_interface.datetime_now_fake
        end_of_day = now + timedelta(days=1)
        now = now.isoformat() + "Z"
        end_of_day = end_of_day.isoformat() + 'Z'
        # print('Getting the upcoming 10 events')

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
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
        # now = datetime.datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        # now = time_interface.datetime_now_fake
        end_of_day = now + timedelta(days=1)

        # now = now.isoformat() + 'Z'
        now = time_interface.datetime_now_fake
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
        # now = datetime.datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        # end_of_day = now + timedelta(days=1)

        # now = now.isoformat() + 'Z'
        now = time_interface.datetime_now_fake.isoformat() + "Z-06:00"
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
        now = datetime.datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        end_of_day = now + timedelta(days=1)

        # now = now.isoformat() + 'Z'
        now = time_interface.datetime_now_fake
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
        # now = datetime.datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        now = time_interface.datetime_now_fake
        # end_of_day = now + timedelta(days=1)

        # now = now.isoformat() + 'Z'
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
        now = datetime.datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        end_of_day = now + timedelta(days=1)

        # now = now.isoformat() + 'Z'
        now = time_interface.datetime_now_fake
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
        now = datetime.datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
        end_of_day = now + timedelta(days=1)

        # now = now.isoformat() + 'Z'
        now = time_interface.datetime_now_fake
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

    def __init__(self, event):
        self.summary = ''
        self.start = "" # what format is time? UTC
        self.end = ""
        self.location = "" # (address)
        self.description = ""
        self.creator = ""
        # self.organizer = ""
        self.attendees = []
        # self.link = ""
        # self.source = ""
        # self.attachments = []
        self.keyword = ""
        # self.relevant_emails = []

        event_start = event['start']
        event_end = event['end']

        if 'dateTime' in event_start:
            self.start = time_interface.string_to_datetime(event_start['dateTime'], 'dateTime')
        elif 'date' in event_start:
            self.start = time_interface.string_to_datetime(event_start['date'], 'date')
        if 'dateTime' in event_end:
            self.start = time_interface.string_to_datetime(event_end['dateTime'], 'dateTime')
        elif 'date' in event_end:
            self.start = time_interface.string_to_datetime(event_end['date'], 'date')
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
                    self.attendees.append(x['displayName'].encode('utf-8'))


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

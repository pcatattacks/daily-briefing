# Daily Breifing: Functional Architecture for Google Calendar
# TODO Proper api calls for events of the day
# TODO Api calls for events matching a query (like meetings, tests, trips, etc...)
# TODO Parse calendar obj returned from google into a simpler custom 'Event'
# object for easier use by our DailyBriefing class.

# Modules
from apiclient import errors
import pytz
import time_interface
import datetime
import json  # debug

'''
    The Calendar Class
    # TODO Proper api calls for events of the day
    # TODO Api calls for events matching a query (like meetings, tests, trips, etc...)

'''
class Calendar:


    ''' Initiate authorized service for gmail API with specified account '''
    def __init__(self, service, user_id, user, time_service):
        self.service = service
        self.user_id = user_id
        self.user = user
        self.time_service = time_service
        # self.contacts = {} # key: value of name: (email, [event])
        # self.locations = {} # key: value of location: [event]

    ''' Get the next ten upcoming events'''
    def get_next_ten_events(self):
        # print('Getting the upcoming 10 events')

        now, end_of_day = self.time_service.get_time_now_and_eod()

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
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


    def getEventsInRange(self, timeStart, timeEnd):
        time_zone = pytz.timezone('America/Chicago')
        date = (self.time_service.get_time_now_and_eod()[0]).date()

        ''' Parse given start and end times to generate datetime objects '''
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

        ''' Combine start and end times with today's date '''
        date_time_end = datetime.datetime.combine(date, timeEndF)
        date_time = datetime.datetime.combine(date, timeStartF)

        ''' Time-zone localization '''
        date_time_end = time_zone.localize(date_time_end)
        date_time = time_zone.localize(date_time)

        ''' String from time '''
        date_time_end = date_time_end.strftime('%Y-%m-%dT%H:%M:%S-06:00')
        date_time = date_time.strftime('%Y-%m-%dT%H:%M:%S-06:00')

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=date_time,
            timeMax = date_time_end,
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

        # print('get_todays_events')  # debug

        now, end_of_day = self.time_service.get_time_now_and_eod()

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        # print (json.dumps(events, indent=2))  # debug
        events_processed = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            events_processed.append(Event(event))

        return events_processed

    def getEventsWithAttendees(self, attendee):

        # print('getEventsWithAttendees ', attendee)

        now, end_of_day = self.time_service.get_time_now_and_eod()

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
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

        # print('getEventsAtTime', time)
        time_zone = pytz.timezone('America/Chicago')
        if ":" in time:
            minute = int(time.split(":")[1])
            hour = int(time.split(":")[0])
        else:
            minute = 0
            hour = int(time)
        time = datetime.time(hour, minute)
        now, end_of_day = self.time_service.get_time_now_and_eod_date()
        date_time = datetime.datetime.combine(now[0], time)
        now = now[0].strftime('%Y-%m-%dT%H:%M:%S-06:00')
        end_of_day = end_of_day.strftime('%Y-%m-%dT%H:%M:%S-06:00')
        date_time = time_zone.localize(date_time)
        time = date_time.strftime('%Y-%m-%dT%H:%M:%S-06:00')
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        resultEvents = []
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            if time == start:
                resultEvents.append(event)
        events_processed = []
        for event in resultEvents:
            events_processed.append(Event(event))
        return events_processed


    def getEventsAtLocation(self, location):

        # print("getEventsAtLocation", location)

        now, end_of_day = self.time_service.get_time_now_and_eod()

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
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

        # print('getEventsWithKeywordsInTitle, ', keywords)

        now, end_of_day = self.time_service.get_time_now_and_eod()

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
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

        # print('getEventsWithKeywordsInDescription', keywords)

        now, end_of_day = self.time_service.get_time_now_and_eod()

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
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

        # print('eventIsConfirmed,' + eventTitle + "?")

        now, end_of_day = self.time_service.get_time_now_and_eod()

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end_of_day,
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

class Event():

    def __init__(self, event):
        self.summary = ''
        self.start = "" # what format is time? UTC
        self.end = ""
        self.location = "" # (address)
        self.description = ""
        self.creator = ""
        self.attendees = []
        self.keywords = []
        self.related_emails = []
        # self.organizer = ""
        # self.link = ""
        # self.source = ""
        # self.attachments = []

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

            if "with" in self.summary:
                summary_list = self.summary.split() # split by space
                with_index = summary_list.index("with")

                self.keywords.append(summary_list[with_index-1].encode('utf-8'))
                self.attendees.append(summary_list[with_index+1].encode('utf-8'))

                if "to" in summary_list:
                        to_index = summary_list.index("to")
                        self.keywords.append(summary_list[to_index+1:])

        if 'location' in event:
            self.location = event["location"].lower()

            # if location in self.locations:
            #     corresponding_events = self.locations[location]
            #     if event not in corresponding_events:
            #         corresponding_events.add(event)
            # else:
            #     self.locations[location] = [event]

        if 'description' in event:
            self.description = event['description']

        if 'link' in event:
            self.link = event['link']

        if 'attendees' in event:
            for x in event['attendees']:
                if 'displayName' in x:
                    for i in self.attendees:
                        if i == (x['displayName'].encode('utf-8')) or i == ((x['displayName'].encode('utf-8')).split(' ')[0]):
                            #remove duplicate names, assuming first names are dups if they are equal
                            self.attendees.remove(i)
                    self.attendees.append((x['displayName'].encode('utf-8')))


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
            newList = ",".join(self.attendees)
            format_arg_list.append(newList)
        return out_str.format(*format_arg_list)

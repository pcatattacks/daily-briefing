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
    s = datetime.strptime(datetime_in,"%Y-%m-%dT%H:%M:%S-08:00")

    ss = "{} {}".format(s.date(),s.time().strftime( "%I:%M %p" ))

    return s


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
    def __init__(self, service, user_id, maxResults):
        self.service = service
        self.user_id = user_id
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

    # relevant_emails = []

    def __init__(self, event):

        self.start = cal_datetime_to_readable(event['start']['dateTime'])
        self.end = cal_datetime_to_readable(event['start']['dateTime'])
        self.id = event['id']

        if 'summary' in event:
            self.summary = event['summary']
        if 'location' in event:
            self.location = event['location']
        if 'description' in event:
            self.description = event['description']
        if 'link' in event:
            self.link = event['link']
        if 'attendees' in event:
            for x in event['attendees']:
                self.attendees.append(x['displayName'].encode('utf-8'))

        # self.speech =

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

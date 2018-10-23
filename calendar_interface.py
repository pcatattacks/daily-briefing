# Daily Breifing: Functional Architecture for Google Calendar
# TODO Proper api calls for events of the day
# TODO Api calls for events matching a query (like meetings, tests, trips, etc...)
# TODO Parse calendar obj returned from google into a simpler custom 'Event'
# object for easier use by our DailyBriefing class.

# Modules
import datetime
from apiclient import errors


''' Helper Functions '''
''' Convert timestamps into human readable format

    e.g.    Start time: 2014-06-03 09:00 AM
            End time: 2014-06-03 10:00 AM

'''
def cal_datetime_to_readable(datetime_in):
    s = datetime.datetime.strptime(datetime_in,"%Y-%m-%dT%H:%M:%S-07:00")

    ss = "{} {}".format(s.date(),s.time().strftime( "%I:%M %p" ))

    return ss


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
        events_processed = []
        if not events:
            print('No upcoming events found.')
        for event in events:

            events_processed.append(Event(event))
        return events_processed

    ''' Reads out events of the Day '''
    def get_todays_events(self):
        # TODO THIS IS THE MAIN POINT
        return 0

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
    organizer = ""
    attendees = []
    link = ""
    source = ""
    attachments = []

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
            self.attendees = event['attendees']

    def __repr__(self):
        out_str = '''
        EVENT
        summary {}
        start {}
        end {}
        location {}
        description {}
        creator {}
        attendees {}
        '''.format(self.id, self.summary, self.start, self.end,
        self.location, self.description, self.creator, self.attendees)

        return out_str

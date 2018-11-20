from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pytz
# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """


    getEventsInRange("19:30", "23")

def getEventsWithAttendees(attendees):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('config/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    endOfDay = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat() + 'Z'

    print('Getting today\'s events')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax = endOfDay,
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    resultEvents = []
    if not events:
        print('No upcoming events found.')
    for event in events:
        for person in attendees:
            for personAttend in event['attendees']:
                realPerson = personAttend.get('displayName')
                if person == realPerson:
                    resultEvents.append(event)
                    break;
    for event in resultEvents:
        print(event['summary']);

def getEventsInRange(timeStart, timeEnd):
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

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('config/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    endOfDay = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat() + 'Z'

    print('Getting today\'s events')
    events_result = service.events().list(calendarId='primary', timeMin=date_time, timeMax = date_time_end,
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    resultEvents = events
    if not events:
        print('No upcoming events found.')
    for event in resultEvents:
        print(event['summary']);

def getEventsAtTime(time):
    time_zone = pytz.timezone('America/Chicago')
    date = datetime.datetime.now().date()
    if ":" in time:
        minute = int(time.split(":")[1])
        hour = int(time.split(":")[0])
    else:
        minute = 0
        hour = int(time)
    time = datetime.time(hour, minute)
    date_time = datetime.datetime.combine(date, time)
    date_time = time_zone.localize(date_time)
    date_time = date_time.strftime('%Y-%m-%dT%H:%M:%S-06:00')
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('config/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    endOfDay = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat() + 'Z'

    print('Getting today\'s events')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax = endOfDay,
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    resultEvents = []
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if date_time == start:
            resultEvents.append(event)
    for event in resultEvents:
        print(event['summary']);

def getEventsAtLocation(location):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    endOfDay = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat() + 'Z'

    print('Getting today\'s events')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax = endOfDay,
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    resultEvents = []
    if not events:
        print('No upcoming events found.')
    for event in events:
        if location == event['location']:
            resultEvents.append(event)
    for event in resultEvents:
        print(event['summary']);


def getEventsWithKeywordsInTitle(keywords):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    endOfDay = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat() + 'Z'

    print('Getting today\'s events')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax = endOfDay,
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    resultEvents = []
    if not events:
        print('No upcoming events found.')
    for event in events:
        for word in keywords:
            if word in event['summary']:
                resultEvents.append(event)
    for event in resultEvents:
        print(event['summary']);


def getEventsWithKeywordsInDescription(keywords):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    endOfDay = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat() + 'Z'

    print('Getting today\'s events')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax = endOfDay,
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    resultEvents = []
    if not events:
        print('No upcoming events found.')
    for event in events:
        for word in keywords:
            if word in event['description']:
                resultEvents.append(event)
    for event in resultEvents:
        print(event['summary']);

def eventIsConfirmed(eventTitle):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    endOfDay = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat() + 'Z'

    print('Getting today\'s events')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax = endOfDay,
                                         singleEvents=True,
                                        orderBy='startTime').execute()
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
if __name__ == '__main__':
    main()

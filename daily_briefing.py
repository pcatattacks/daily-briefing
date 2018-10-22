# the Daily Breifing interface

# Google API Modules
from __future__ import print_function
from googleapiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools

# Text to Speech Modules
from gtts import gTTS
import os

''' Helper Modules '''
import datetime

''' Daily Briefing Modules '''
from gmail_api import *
from calendar_interface import *

def speak(string, slow=False):
    tts = gTTS(text=string, lang='en', slow=slow)
    tts.save("daily_briefing_out.mp3")
    os.system("mpg321 daily_briefing_out.mp3 -q")


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
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            creds = tools.run_flow(flow, store)

        ''' Authenticate api services to Google Mail and Calendar '''
        self.mail_service = build('gmail', 'v1', http=creds.authorize(Http()))
        self.cal_service = build('calendar', 'v3', http=creds.authorize(Http()))

        ''' Create a Mail & Calendar object '''
        self.mail = Mail(self.mail_service, self.user_id, self.maxResults)
        self.cal = Calendar(self.cal_service, self.user_id, self.maxResults)

    def test(self):


        # speak(''' Next 10 events on the Calendar ''')
        # self.cal.get_next_ten_events()
        #
        # print('\n\n')

        # speak("Listing all labels for this gmail account...\n\n")
        # self.mail.get_labels()

        # print('\n\n')

        # speak(''' Query messages by term ''')
        # query_terms = ['hike', 'meet', 'see you']
        # for query in query_terms:
        #     speak("\n\n Querying messages for \""+ query +"\" ...\n\n", slow=True )
        #     self.mail.ListMessagesMatchingQuery(query)

        # speak(''' Get messages by Label ''')
        label_terms = ['IMPORTANT', 'CATEGORY_PERSONAL', 'STARRED', 'UNREAD']

        for label in label_terms:
            speak("Getting all "+ label+" messages \n\n")
            self.mail.ListMessagesWithLabels([label])




def main():

    daily_briefing = DailyBriefing()

    daily_briefing.test()

if __name__ == '__main__':
    main()

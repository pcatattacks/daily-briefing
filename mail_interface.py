# Daily Breifing: Functional Architecture for Google mail
# TODO get full body of email (parse mimetype)
# TODO get endpoints from calendar to try to put together with email querying
# TODO Extract specific information relevant to cal events
# TODO Handle email threads
# TODO Represent information differently for text and speech


# Modules
import datetime


'''
    Gmail message timestamp conversion to human readable date
    Convert gmail's internalDate long to a datetime str
'''
def internalDate_to_timestamp(internalDate):
    s = long(internalDate) / 1000.0
    # return datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')
    return datetime.datetime.fromtimestamp(s).strftime('%A %B %d, %Y %H:%M')



'''
    The Mail Class:
    Makes gmail api calls for messages (emails, threads, and chats) via
    query matching and by message labels.
'''
class Mail:

    ''' Get authorized service for gmail API with specified account from DailyBriefing.py'''
    def __init__(self, service, user_id, maxResults):
        self.service = service
        self.user_id = user_id
        self.maxResults = maxResults


    ''' Get message matching id '''
    def get_message_by_id(self, msg_id):

        message = self.service.users().messages().get(
            userId=self.user_id,
            id=msg_id['id']
        ).execute()

        ''' Parse message and return a new message object '''
        return repr(Message(message))


    '''Lists the user's Gmail labels'''
    def get_labels(self):
        results = self.service.users().labels().list(userId=self.user_id).execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])

        return labels


    ''' List all Messages of the user's mailbox matching the query. '''
    def ListMessagesMatchingQuery(self, query=''):
        try:
            response = self.service.users().messages().list(
                userId=self.user_id,
                maxResults=self.maxResults,
                q=query
            ).execute()

            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

                for x in messages:
                    self.get_message_by_id(x)

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(
                    userId=self.user_id,
                    q=query,
                    maxResults=self.maxResults,
                    pageToken=page_token
                ).execute()

                messages.extend(response['messages'])

                for x in messages:
                    self.get_message_by_id(x)

                return messages
        except errors.HttpError, error:
            print('An error occurred: %s' % error)


    ''' List all Messages of the user's mailbox with label_ids applied '''
    def ListMessagesWithLabels(self, label_ids=[]):
        try:
            response = self.service.users().messages().list(
                userId=self.user_id,
                maxResults=self.maxResults,
                labelIds=label_ids
            ).execute()

            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

                for x in messages:
                    self.get_message_by_id(x)

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(
                    userId=self.user_id,
                    maxResults=self.maxResults,
                    labelIds=label_ids,
                    pageToken=page_token
                ).execute()
                messages.extend(response['messages'])

                for x in messages:
                    self.get_message_by_id(x)

                return messages
        except errors.HttpError, error:
            print('An error occurred: %s' % error)


'''
    The Message Class
    * Initialized w/ message returned by gmail api.
    * Parse returned information and create simplified message represenation
    * Represents messages for speech and text output.
'''
class Message:

    id = None
    sender = ""
    recipients = []
    subject = ""
    snippet = ""
    body = ""
    timestamp = ""
    thread = None
    labels = []
    important = False


    ''' Parse gmail api's returned message into object we an easily work with '''
    def __init__(self, message):

        self.id = message['id']

        ''' Get labels, e.g. ['CHAT', 'IMPORTANT', 'CATEGORY_PERSONAL', 'INBOX'] '''
        if 'labelIds' in message:
            self.labels = message['labelIds']

            ''' Skip spammy marketing emails '''
            if u'CATEGORY_UPDATES' in message['labelIds'] or \
            u'CATEGORY_PROMOTIONS' in message['labelIds']:
                return None

        self.timestamp = internalDate_to_timestamp(message['internalDate'])

        self.snippet = message['snippet']

        ''' Message Payload... '''
        # TODO Depending on mimetype, we will parse the body differently
        msg_payload = message['payload']

        ''' Get To, From, and Subject from Headers '''
        for pair in msg_payload['headers']:
            if pair['name'] == 'From':
                self.sender = pair['value']

            if pair['name'] == 'To':
                self.recipients = pair['value']

            if pair['name'] ==  'Subject':
                self.subject = pair['value']


    def __repr__(self):
        out_str = '''
        MESSAGE {}
        timestamp: {}
        labels: {}
        sender: {}
        recipients: {}
        subject: {}
        snippet: {}
        '''.format(self.id, self.timestamp, self.labels, self.sender,
        self.recipients, self.subject, self.snippet)

        return out_str

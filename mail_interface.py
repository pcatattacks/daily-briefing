# Daily Breifing: Functional Architecture for Google mail
# TODO get full body of email (parse mimetype)
# TODO get endpoints from calendar to try to put together with email querying
# TODO Extract specific information relevant to cal events
# TODO Handle email threads
# TODO Represent information differently for text and speech


# Modules
import datetime
from apiclient import errors


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


    ''' API call GET message matching id, then parse it into string represenation '''
    def get_message_by_id(self, msg_id):

        message = self.service.users().messages().get(
            userId=self.user_id,
            id=msg_id['id']
        ).execute()

        ''' Parse message into object, return as string represenation of the object '''
        return Message(message)


    '''Lists the user's Gmail labels'''
    def get_labels(self):
        results = self.service.users().labels().list(userId=self.user_id).execute()
        labels = results.get('labels', [])

        labels_processed = []
        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                labels_processed.append(label['name'])

        return labels_processed


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

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(
                    userId=self.user_id,
                    q=query,
                    maxResults=self.maxResults,
                    pageToken=page_token
                ).execute()

                messages.extend(response['messages'])

                ''' Get the actual message content,
                convert it to simple Message object
                '''
                messages = map(self.get_message_by_id, messages)
                for m in messages:
                    if not m.subject and not m.snippet:
                        messages.remove(m)
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

                ''' Get the actual message content,
                convert it to simple Message object
                '''
                messages = map(self.get_message_by_id, messages)

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

            ''' Skip spammy marketing emails '''
            if u'CATEGORY_UPDATES' in message['labelIds'] or \
            u'CATEGORY_PROMOTIONS' in message['labelIds']:
                return None

            self.labels = []
            labels = message['labelIds']

            for l in labels:
                if "CATEGORY_" in l:
                    self.labels.append(l[9:].capitalize())
                else:
                    self.labels.append(l.capitalize())

        self.timestamp = internalDate_to_timestamp(message['internalDate'])

        self.snippet = message['snippet']

        ''' Message Payload... '''
        # TODO Depending on mimetype, we will parse the body differently
        msg_payload = message['payload']

        ''' Get To, From, and Subject from Headers '''
        for pair in msg_payload['headers']:
            if pair['name'] == 'From':
                sender = pair['value'].split(",")
                self.sender = ''
                for x in sender:
                    self.sender += " ".join(x.split()[:-1]) + ", "
                self.sender = self.sender[:-2]

            if pair['name'] == 'To':
                # self.recipients = pair['value'].split(",")
                # for x in self.recipients:
                #     x = x.split()[:-1]
                recipients = pair['value'].split(",")
                self.recipients = ''
                for x in recipients:
                    self.recipients += " ".join(x.split()[:-1]) + ", "
                self.recipients = self.recipients[:-2]

            if pair['name'] ==  'Subject':
                self.subject = pair['value']

    def __repr__(self):
        format_args = self.labels + [self.timestamp, self.sender,
        self.recipients, self.subject, self.snippet]
        out_str = "\n\nMESSAGE ["+ len(self.labels) * "{}, "
        out_str = out_str[:-2] + "]\n"
        out_str += '''{}
From: {}
To: {}

{}

{}

        '''
        return out_str.format(*format_args)

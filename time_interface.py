#time_interface.py
from datetime import *

'''
    Convert timestamps into human readable format
    e.g.    Start time: 2014-06-03 09:00 AM
            End time: 2014-06-03 10:00 AM
'''
def string_to_datetime(datetime_str, date_format):
    if date_format == 'dateTime':
        s = datetime.strptime(datetime_str,"%Y-%m-%dT%H:%M:%S-06:00")
    elif date_format == 'date':
        s = datetime.strptime(datetime_str, "%Y-%m-%d")
    else:
        s = datetime.strptime(datetime_str, date_format)

    ss = "{} {}".format(s.date(),s.time().strftime( "%I:%M %p" ))

    return s

'''
    Date object to string
'''
def datetime_to_string(datetime):
    return datetime.isoformat + "Z"

'''
    Gmail message timestamp conversion to human readable date
    Convert gmail's internalDate long to a datetime str
'''
def internalDate_to_timestamp(internalDate):
    s = long(internalDate) / 1000.0
    # return datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')
    return datetime.fromtimestamp(s).strftime('%A %B %d, %Y %H:%M')


class TimeService:

    '''
        Initialize datetimes for "Now" and "End of Day".
    '''
    def __init__(self, demo=False):
        self.demo = demo

        # Coby's calendar date full of meetings: "NOW" is 6AM on Nov 20th, 2018
        coby_calendar_date = "2018-11-20T06:00:00-06:00"
        self.demo_now = string_to_datetime(coby_calendar_date, "dateTime")
        self.demo_end_of_day = self.demo_now + timedelta(days=1)

        # else:
        #     self.real_now = datetime.utcnow()
        #     self.real_end_of_day = now + timedelta(days=1)
        #     self.real_now = time_interface.datetime_now_fake
        #     self.real_end_of_day = end_of_day.isoformat() + 'Z'

    '''
        Return a tuple (now, end_of_day)
    '''
    def get_time_now_and_eod(self):

        # If self.demo is True, then we use our fake value for "now" to reference our demo calendar
        if self.demo:
            now = self.demo_now
        else:
            now = datetime.utcnow()

        end_of_day = now + timedelta(days=1)
        now = now.isoformat() + "Z"
        end_of_day = end_of_day.isoformat() + 'Z'

        # now = self.string_to_datetime(now, '%Y-%m-%dT%H:%M:%SZ'),
        # end_of_day = self.string_to_datetime(end_of_day, '%Y-%m-%dT%H:%M:%SZ')

        return now, end_of_day

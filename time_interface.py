#time_interface.py
import datetime

''' Convert timestamps into human readable format

    e.g.    Start time: 2014-06-03 09:00 AM
            End time: 2014-06-03 10:00 AM

'''
def string_to_datetime(datetime_str, date_format):
    if date_format == 'dateTime':
        s = datetime.datetime.strptime(datetime_str,"%Y-%m-%dT%H:%M:%S-06:00")
    elif date_format == 'date':
        s = datetime.datetime.strptime(datetime_str, "%Y-%m-%d")

    ss = "{} {}".format(s.date(),s.time().strftime( "%I:%M %p" ))

    return s


'''
    Gmail message timestamp conversion to human readable date
    Convert gmail's internalDate long to a datetime str
'''
def internalDate_to_timestamp(internalDate):
    s = long(internalDate) / 1000.0
    # return datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')
    return datetime.datetime.fromtimestamp(s).strftime('%A %B %d, %Y %H:%M')

coby_calendar_date = "2018-11-20T08:00:00-06:00"  # Coby's calendar date full of times

datetime_now_fake = string_to_datetime(coby_calendar_date, "dateTime")


datetime_now_real = datetime.datetime.utcnow() #.isoformat() + 'Z' # # 'Z' indicates UTC time
# end_of_day = now + timedelta(days=1)
# end_of_day = (now + timedelta(hours=24)).isoformat() + 'Z'

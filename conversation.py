# conversation.py

from daily_briefing import *

# Text to Speech Modules
from gtts import gTTS
import os


# Global Variables
user_interrupt_flag = False
length_of_deliberate_pause = 3 # seconds



def speak(string, slow=False):
    print(string)
    tts = gTTS(text=string, lang='en', slow=slow)
    tts.save("daily_briefing_out.mp3")
    os.system("mpg321 daily_briefing_out.mp3 -q")

def pause_for_response():
    # TODO count for 3 seconds
    wait()

    # TODO how to handle interruptions
    listen_for_interruption()


def conversation():
    # speaker = "db" # or "user"

    db = daily_briefing()

    ''' Get ordered list of events '''
    list_of_events = db.cal.get_todays_events()


    # Main event loop
    for count, event in enumerate(list_of_events):
        speak(''' Your {} event is {} at {}. '''.format(str(count), event.title, event.start_time)

        pause_for_response()

        while user_interrupt_flag:
            pause_for_response()
            user_interrupt_flag = parse_user_commands(input_string)

    speak(''' That is all of the events on your calendar for today ''')



def parse_user_commands(input_string):
    flag = True
    if "what" is in input_string:
        if "time" is in input_string:
            speak(event.time)
        if "day" is in input_string:
            speak(day(event.time))
        # if "meetings" is in input_string:

    elif "who" is in input_string:
        # TODO get names from event and search email
        names = db.parse_names(event)
        for name in names:
            db.mail.ListMessagesMatchingQuery(name)
        pass
    elif "where" is in input_string:
        speak(event.location)
    elif "more" is in input_string:
        db.get_information_from_email_related_to_event(event)
    elif "wait" is in input_string:
        pause_for_response()
    else:
    # elif "continue" or "go on" or "next" in input_string:
        flag = False
    return flag

}

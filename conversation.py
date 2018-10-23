# conversation.py

from daily_briefing import *

# Text to Speech Modules
from gtts import gTTS
import os



def speak(string, slow=False):
    print(string)
    tts = gTTS(text=string, lang='en', slow=slow)
    tts.save("daily_briefing_out.mp3")
    os.system("mpg321 daily_briefing_out.mp3 -q")

def pause_for_response():
    # TODO count for 3 seconds
    # TODO how to handle interruptions


def conversation():
    speaker = "db" # or "user"
    length_of_deliberate_pause = 3 # seconds

    db = daily_briefing()

    ''' Get ordered list of events '''
    list_of_events = db.cal.get_todays_events()



    # Main event loop
    for count, event in enumerate(list_of_events):
        speak(''' Your {} event is {} at {}. '''.format(str(count), event.title, event.start_time)

        wait()

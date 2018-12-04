# Daily Briefing: Functional Architecture for Conversation Interface.py

# Text-to-Speech (TTS) Modules
from gtts import gTTS
import os

# Speech Recognition
# import speech_recognition as sr

# For reading userinput when given
from select import select
import sys

# Use computer microphone as input audio source
# mic = sr.Microphone()
# recognizer = sr.Recognizer()


# def listen_to_user():
#     print(sr.Microphone.list_microphone_names())
#     with mic as source:
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)
#     print("bar")
#     return recognizer.recognize_google(audio)


''' list files in a specified directory '''
def list_files_in_directory(mypath):
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    return onlyfiles


'''
    listen_for_user_input
    input: timeout (integer): specify number of seconds to wait, 0 = no timeout

'''
def listen_for_user_input(timeout=120):

    user_in = ""

    ''' Wait indefinitely for user input '''
    r, w, e = select([sys.stdin], [], [], timeout)

    ''' If the user has said something, parse user input and follow their commands '''
    if sys.stdin in r:
        user_in = sys.stdin.readline()

    return user_in.lower()


order_dict = {
                0: "first",     1: "second",    2: "third",
                3: "fourth",    4: "fifth",     5: "sixth",
                6: "seventh",   7: "eighth",    8: "ninth",
                9: "tenth"
            }


'''
    prepare_list_of_events_to_speak
    Takes a list of events and subject string (e.g. "You have 10 events today").
    Generates audio files from text-to-speech.
    We'll save these files in a cached folder for the demo, to read from if called again
'''
def prepare_list_of_events_to_speak(events, subject):

    if not events:
        return events

    ''' Translate subject string into '''
    # subject = subject.translate(None, string.punctuation) # remove punctuation

    subject = subject.split("events")[1].split()
    cache_dir_path = "demo/events_" + "_".join(subject) + "/"

    ''' Check if the events have already been prepared and cached'''
    cached_files = []

    if os.path.exists(cache_dir_path):
        cached_files = list_files_in_directory(cache_dir_path)

    if cached_files:
        ''' Add names of cached files to event object'''
        for event_number, event in enumerate(events):
            event_num_string = "event" + str(event_number)
            event.filenames = [cache_dir_path + f for f in cached_files if event_num_string in f]
            event.filenames.sort()
    else:
        ''' make directory to cache events for this subject'''
        os.makedirs(cache_dir_path)

        ''' Convert each event into a list of mp3 speech files '''
        for event_number, event in enumerate(events):

            ''' For each line in the event, create a tts mp3 file and print the line in a txt file'''
            for line_number, line in enumerate(event.lines):

                ''' Format filename e.g demo/todays_events/event0_line0'''
                this_filename = cache_dir_path + "event" + str(event_number) + "_line" + str(line_number)

                ''' Create a speech mp3 file of the line'''
                event.filenames.append(create_file_to_speak(line, title=this_filename))

    return events


def speak(text, title):
    mp3_filename = create_file_to_speak(text=text, title=title) # dont need if not speaking
    print_text_and_play_audio(text, mp3_filename)

# def speak(text, title):
#     print_text_and_play_audio(text)


def create_file_to_speak(text, title, slow=False):

    if not text or not title:
        return "Error: No text or title given."

    mp3_filename = title + ".mp3"

    ''' Google Text-To-Speech'''
    tts = gTTS(text=text, lang='en', slow=slow)
    tts.save(mp3_filename)
    return mp3_filename


def mpg321_mp3_call_quiet(filename):
    mpg321_mp3_call_quiet1 = "mpg321 " + filename + " -q"
    os.system(mpg321_mp3_call_quiet1)


def print_text_and_play_audio(text, mp3_filename, slow=False, duration=False):

    ''' Print the text to accompany speech '''
    # print(mp3_filename)
    print(text)

    ''' Load and playlatest daily_briefing mp3 file'''
    mpg321_mp3_call_quiet(mp3_filename) # commented this out for Coby


# # redefining it here without speaking - taking mp3_filename arg out.
# # while this is here, it will override the previous function.
# def print_text_and_play_audio(text, slow=False, duration=False):
#     print(text)

# Daily Briefing: Functional Architecture for Conversation Interface.py

# Text-to-Speech (TTS) Modules
from gtts import gTTS
import os

# Speech Recognition
import speech_recognition as sr

# Use computer microphone as input audio source
# mic = sr.Microphone()
# recognizer = sr.Recognizer()


# def listen_to_user():
#     print(sr.Microphone.list_microphone_names())
#     print("Foo")
#     with mic as source:
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)
#     print("bar")
#     return recognizer.recognize_google(audio)

order_dict = {
                0: "first",     1: "second",    2: "third",
                3: "fourth",    4: "fifth",     5: "sixth",
                6: "seventh",   7: "eighth",    8: "ninth",
                9: "tenth"
            }

def prepare_list_of_events_to_brief(events):

    for x, event in enumerate(events):

        # print(x, event)

        ''' Say which number event in the list this is '''
        event_str = "Your {} event is ".format(order_dict[x]) + repr(event)

        event.lines = event_str.split("\n")

        ''' Attach a relevant email subject and snippet to end of event '''
        if event.related_emails:
            first_email = event.related_emails[0]
            email_strings = ["Related Email:", first_email.subject, first_email.snippet]
            for email_str in email_strings:
                email_str.encode('utf-8')
            event.lines += email_strings

        if "" in event.lines:
            event.lines.remove("")

        event.filenames = []

        for i, line in enumerate(event.lines):
            event.filenames.append(create_file_to_speak(line, title="event_"+str(x)+"_line"+str(i)))

    return events


def speak(text, title):
    mp3_filename = create_file_to_speak(text=text, title=title)
    print_text_and_play_audio(text, mp3_filename)


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

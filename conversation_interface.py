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

def create_file_to_speak(string, slow=False):

    if not string:
        return None
    ''' Google Text-To-Speech'''
    # mp3_file_name = string.split("\n")[0].split()
    # "_".join(mp3_file_name)+ ".mp3"
    mp3_file_name = "db_out.mp3"
    tts = gTTS(text=string, lang='en', slow=slow)
    tts.save(mp3_file_name)
    return mp3_file_name


def mpg321_mp3_call_quiet(filename):
    mpg321_mp3_call_quiet1 = "mpg321 " + filename + " -q"
    os.system(mpg321_mp3_call_quiet1)


def speak(string="This is a test of the text-to-speach interface", slow=False, duration=False):

    mp3_file_name = create_file_to_speak(string, slow)

    if not mp3_file_name:
        return None
    # ''' Speak, print '''
    # playAudioAndListenForUserInput(mp3_file_name, string)

    ''' Print the text to accompany speech '''
    print(string)

    ''' Load and playlatest daily_briefing mp3 file'''
    mpg321_mp3_call_quiet(mp3_file_name)


# # Multiprocess/multithread Modules (to play audio and listen for user interruptions)
# from subprocess import Popen, PIPE, STDOUT #
# # from mutagen.mp3 import MP3
#
# def write_proc_stdin(proc, stdin_str):
#     stdin_str += "\n"
#     proc.stdin.write(stdin_str)
#     proc.stdin.flush()
#     return read_proc_stdout(proc)
#
# def read_proc_stdout(proc):
#     x = proc.stdout.readline()
#     proc.stdout.flush()
#     return x
#
# '''
#     This function will play audio and respond to user input.
#     Right now it's through text, but we should be able to hook up a
#     Audio input, convert to text, and send it in as stdin.
#
# '''
# def playAudioAndListenForUserInput(voice_mp3, text):
#     voice = None
#     loop = True
#
#     ''' mpg321 remote control to play audio interactively '''
#     # remote_control_cmd = 'mpg321 -R foo'
#
#     ''' Open a subprocess with remote_control_cmd '''
#     # voice = Popen(remote_control_cmd.split(' '), stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
#
#     ''' Print the text to accompany speech '''
#     print(text)
#
#     ''' Load and playlatest daily_briefing_out.mp3 file'''
#     # play_audio_cmd = 'load ' + voice_mp3
#     # write_proc_stdin(voice, play_audio_cmd)
#     os.system("mgp321 daily_briefing_out.mp3 -q")
#
#     while loop:
#
#         ''' Check if proc is terminated '''
#         x = write_proc_stdin(voice, "\n\n")
#         # print(x)
#         if "@P" in x or "3" in x:
#             loop = False
#             write_proc_stdin(voice, 'stop')
#             voice.kill()
#             voice = None
#             break
#         else:
#             ''' Listen for user input '''
#             user_cmd = raw_input('> ')
#
#         if user_cmd.lower() == 'pause' or user_cmd.lower() == 'play':
#
#             write_proc_stdin(voice, 'pause')
#
#         elif user_cmd.lower() == 'stop':
#             try:
#                 write_proc_stdin(voice, 'stop')
#                 voice.stdout.close()
#                 voice.stdin.close()
#                 voice.kill()
#             except:
#                 pass
#             voice = None
#             loop = False
#             break
#     if voice:
#         voice.kill()


# def pause_for_response():
#     # TODO count for 3 seconds
#     wait()
#
#     # TODO how to handle interruptions
#     listen_for_interruption()
#

# def conversation():
#     # speaker = "db" # or "user"
#
#     db = daily_briefing()
#
#     ''' Get ordered list of events '''
#     list_of_events = db.cal.get_todays_events()
#
#
#     # Main event loop
#     for count, event in enumerate(list_of_events):
#         speak(''' Your {} event is {} at {}. '''.format(str(count), event.title, event.start_time))
#
#         pause_for_response()
#
#         while user_interrupt_flag:
#             pause_for_response()
#             user_interrupt_flag = parse_user_commands(input_string)
#
#     speak(''' That is all of the events on your calendar for today ''')



# def parse_user_commands(input_string):
#     flag = True
#     if "what" in input_string:
#         if "time" in input_string:
#             speak(event.time)
#         if "day" in input_string:
#             speak(day(event.time))
#         # if "meetings" in input_string:
#
#     elif "who" in input_string:
#         # TODO get names from event and search email
#         names = db.parse_names(event)
#         for name in names:
#             db.mail.ListMessagesMatchingQuery(name)
#     elif "where" in input_string:
#         speak(event.location)
#     elif "more" in input_string:
#         db.get_information_from_email_related_to_event(event)
#     elif "wait" in input_string:
#         pause_for_response()
#         pass
#     else:
#     # elif "continue" or "go on" or "next" in input_string:
#         flag = False
#     return flag

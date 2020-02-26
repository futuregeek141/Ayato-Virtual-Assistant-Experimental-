from gtts import gTTS
import speech_recognition as sr
import pygame.mixer as mx 
import random
import os
import re
import webbrowser
import datetime as dt
import playsound as ps

def talk(audio):
    print(audio)
    for line in audio.splitlines():
        
        text_to_speech = gTTS(text=line, lang='en-us')
        date_string = dt.datetime.now().strftime("%d%m%Y%H%M%S")
        filename = "voice"+date_string+".mp3"
        text_to_speech.save(filename)
        ps.playsound(filename)
        #text_to_speech.save('audio.mp3')
        print(audio)
        mx.init()    
        mx.music.load("audio.mp3")
        mx.music.play()
        """
        r1 = random.randint(1,10000000)
        r2 = random.randint(1,10000000)

        randfile = str(r2)+"randomtext"+str(r1) +".mp3"

        tts = gTTS(text='hey, STOP It!!', lang='en', slow=True)
        tts.save(randfile)

        print(randfile)
        os.remove(randfile)
        """


def myCommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ayato is Ready...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source,duration=1)

        audio = r.listen(source)
    
    try:
        command = r.recognize_google(audio).lower()
        print('YOu said: ' + command + '\n')


    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand()

    return command

def Ayato(command):
    errors = [
        "I don\'t know what you mean!",
        "Excuse me?",
        "Can you repeat it please?`",
    ]
    
    if 'open google' in command:
    #mactching commmand..
        reg_ex = re.search('open google (.*)',command)
        url = 'https://www.google.com/'
        if reg_ex:
            subgoogle = reg_ex.group(1)
            url = url + 'r/' + subgoogle
        webbrowser.open(url)
        print('Done!')
    elif 'hello' in command:
        talk('Howdy! Ayato desu.. How can i help you?')
    else:
        error = random.choice(errors)
        talk(error)


talk('Ayato is ready!')

while True:
    Ayato(myCommand())


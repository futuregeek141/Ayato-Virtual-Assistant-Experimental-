from gtts import gTTS
import urllib.request #used to make requests
import urllib.parse #used to parse values into the url
import speech_recognition as sr
import pygame.mixer as mx 
import random
from googlesearch import search
import sys
from pyowm import OWM #to know weather details of city
import os
import re
import webbrowser
import bs4
import requests
import smtplib
from selenium import webdriver
import time
import datetime as dt
import multiprocessing
import playsound as ps

count = 0
end = 0

def send_mail(country_element, total_cases, new_cases, total_deaths, active_cases, total_recovered, serious_critical):    
    subject = 'Coronavirus stats in your country today!'
    
    body = 'Today in ' + country_element + '\
    \nThere is new data on coronavirus:\
    \nTotal cases: ' + total_cases +'\
    \nNew cases: ' + new_cases + '\
    \nTotal deaths: ' + total_deaths + '\
    \nActive cases: ' + active_cases + '\
    \nTotal recovered: ' + total_recovered + '\
    \nSerious, critical cases: ' + serious_critical  + '\
    \nCheck the link: https://www.worldometers.info/coronavirus/'

    content = 'Subject: {}\n\n{}'.format(subject, body)

    mail = smtplib.SMTP('smtp.gmail.com', 587) #port used by smtp to listen for specific host

    #identify to server
    mail.ehlo()
    #encrypt session
    mail.starttls()
        #login
    mail.login('14125114np@gmail.com', 'glucose@141')
    g = input("Enter reciever email : ") 
        #send message
    mail.sendmail('14125114np@gmail.com', g, content)
        #end mail connection
    mail.close()
    talk('Email sent.')

class Coronavirus():
  def __init__(self):
    self.driver = webdriver.Chrome()
    country = input("Enter country to search: ")
    self.driver.get('https://www.worldometers.info/coronavirus/')
    table = self.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
    country_element = table.find_element_by_xpath("//td[contains(., 'India')]")
    row = country_element.find_element_by_xpath("./..")

    data = row.text.split(" ")
    total_cases = data[1]
    new_cases = data[2]
    total_deaths = data[3]
    active_cases = data[5]
    total_recovered = data[6]
    serious_critical = data[7]
    print('Here I quote latest stats on Corona in %s:total cases rise to %s, %s new cases recorded, %s have died till now, Active cases are %s, total_recoveries are %s while %s are critical' % (country,total_cases,new_cases,total_deaths,active_cases,total_recovered,serious_critical))
    talk('Here I quote latest stats on Corona in %s:total cases rise to %s, %s new cases recorded, %s have died till now, Active cases are %s, total_recoveries are %s while %s are critical' % (country,total_cases,new_cases,total_deaths,active_cases,total_recovered,serious_critical))
    talk('Type yes to get a copy of report in your email..')
    inp = input('Type yes to get a copy of report in your email..')
    if 'yes' in inp:
        send_mail(country, total_cases, new_cases, total_deaths, active_cases, total_recovered, serious_critical)

def talk(audio):
    for line in audio.splitlines():

        print(count)
        text_to_speech = gTTS(text=line, lang='en-us')
        print(count)
        date_string = dt.datetime.now().strftime("%d%m%Y%H%M%S")
        filename = "voice"+date_string+".mp3"
        text_to_speech.save(filename)
        ps.playsound(filename)
        #text_to_speech.save('audio.mp3')
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
    #Code for microphone
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ayato is Ready...')
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source,duration=0.5) ## listen for 1 second to calibrate the energy threshold for ambient noise levels
        audio = r.listen(source)
    
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')


    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand()

    return command

def Ayato(command):
    errors = [
        "I don\'t know what you mean!",
        "Excuse me?",
        "Can you repeat it please?",
    ]
    
    if 'hello' in command:
    #mactching commmand..
        talk('Howdy! Ayato here.. How can i help you?')

    elif 'open google and search' in command:
        reg_ex = re.search('open google and search (.*)',command)
        url = 'https://www.google.com/'
        if reg_ex:
            subgoogle = reg_ex.group(1)
            webbrowser.open("https://google.com/search?q=%s" % subgoogle)
        else:    
            webbrowser.open(url)
        print('Done!')
    elif 'email' in command:
        talk("Tell the subject")
        time.sleep(3)
        subject = myCommand()
        talk('Quote your message:')
        time.sleep(3)
        message = myCommand()
        content = 'Subject: {}\n\n{}'.format(subject, message)
        
        #init gmail SMTP
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        #identify to server
        mail.ehlo()

        #encrypt session
        mail.starttls()
        #login
        mail.login('14125114np@gmail.com', 'glucose@141')
        g = input("Enter reciever email : ") 
        #send message
        mail.sendmail('14125114np@gmail.com', g, content)

        #end mail connection
        mail.close()

        talk('Email sent.')

    elif 'wikipedia' in command:
        reg_ex = re.search('search in wikipedia (.+)', command)
        if reg_ex: 
            query = command.split()
            response = requests.get("https://en.wikipedia.org/wiki/" + query[3])

            if response is not None:
                html = bs4.BeautifulSoup(response.text, 'html.parser')
                
                paragraphs = html.select("p")
                for para in paragraphs:
                    print (para.text)


                intro = '\n'.join([ para.text for para in paragraphs[0:5]])
                print (intro)
                language = 'en'
                myobj = gTTS(text=intro, lang=language, slow=False)   
                date_string = dt.datetime.now().strftime("%d%m%Y%H%M%S")
                filename = "speech"+date_string+".mp3"
                myobj.save(filename)
                mx.init()
                mx.music.load(filename)
                mx.music.play()

    elif 'youtube' in command:
        talk('Ok!')
        reg_ex = re.search('youtube (.+)', command)
        if reg_ex:
            domain = command.split("youtube",1)[1] 
            query_string = urllib.parse.urlencode({"search_query" : domain})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string) 
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode()) # finds all links in search result
            webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
            pass                

    elif 'stop' in command:
        mx.music.stop()
    
    elif 'open pandemic records' in command:
        records = Coronavirus()

    elif 'exit' in command:
        talk("Ayato signing out for now!")
        sys.exit() 
    else:
        error = random.choice(errors)
        talk(error)
#FIrst code executed:
while True:
    if count == 0:
        mx.init()    
        mx.music.load("audio.mp3")
        mx.music.play()
        count+=1
    else:
        Ayato(myCommand())
    



import math
import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import webbrowser # open browser
import ssl
import certifi
import time
import os # to remove created audio files
from PIL import Image
import subprocess
import pyautogui #screenshot
import pyttsx3
import bs4 as bs
import urllib.request
import requests
import pyttsx3
from datetime import date
from tkinter import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
import subprocess
import datetime
from tkinter import colorchooser
from pynput.keyboard import Key, Controller
import mathfunctions

window = Tk()

global bot_response
global user_response
global bot_confirmation
global voice_data 
global receiver_num
global receiver_message
voice_data = None
global isClicked
isClicked = False
global volume 
volume = 100
global bgcolor 
bgcolor = "#0f212c"
global wcount
wcount = 0 

global voice
voice = None
bot_response = StringVar()
user_response = StringVar()
bot_confirmation = StringVar()
receiver_num = StringVar()
receiver_message = StringVar()

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome("C:\\chromedriver_win32\\chromedriver.exe",chrome_options=chrome_options)


class person:
    name = ''
    def setName(self, name):
        self.name = name

class brobot:
    name = ''
    def setName(self, name):
        self.name = name

def swap(frame):
    frame.tkraise()

def tohomescreen():
    swap(homeScreen)
def tosettingscreen():
    swap(settingScreen)


def engine_speak(text):
    text = str(text)
    threading.Thread(target=engine.say(text)).start()
    threading.Thread(target=engine.runAndWait()).start()


def record_audio(ask=""):
    with sr.Microphone() as source: # microphone as source
        if ask:
            threading.Thread(target=engine_speak(ask)).start()
        audio = sr.Recognizer().listen(source, timeout=None, phrase_time_limit= 7)
        threading.Thread(target=bot_confirmation.set("Listening...")).start()
        threading.Thread(target=window.update()).start()
        voice_data = ''
        try:
            voice_data = sr.Recognizer().recognize_google(audio)
            threading.Thread(target=user_response.set(voice_data)).start() 
            threading.Thread(target=window.update()).start()
        except sr.UnknownValueError: # error: recognizer does not understand
            print("I did not get that!")
        except sr.RequestError:
            engine_speak('Sorry, the service is down') # error: recognizer is not connected
        print(">>", voice_data.lower()) # print what user said
        
        
        return voice_data.lower()

def selenium(url,id):
    driver.get(url)
    data = driver.find_element_by_id(id).text
    return data



def engine_speak(audio_string):
    global voice
    audio_string = str(audio_string)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    if voice == 'Female':
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)
    engine.setProperty('volume', volume)
    bot_confirmation.set("Speaking...")
    window.update()
    engine.say(audio_string)
    engine.runAndWait()
    print(brobot_obj.name + ":", audio_string)
    bot_confirmation.set("Listening...")
    window.update()

def respond(voice_data):
    # 1: greeting
    if 'hello' in voice_data:
        greetings = ["hey, how can I help you", "hey, what's up?", "I'm listening", "how can I help you?", "hello"]
        greet = random.randint(0,len(greetings)-1)
        bot_response.set(greetings[greet])
        window.update()
        threading.Thread(target=engine_speak(greetings[greet])).start()

    # 2: name
    if 'what is your name' in voice_data:
            bot_response.set(f"My name is {brobot_obj.name}. what's your name?")
            window.update()
            threading.Thread(target=engine_speak(f"My name is {brobot_obj.name}. what's your name?")).start() #incase you haven't provided your name.

    if 'my name is' in voice_data:
        person_name = voice_data.split("is")[-1].strip()
        bot_response.set("okay, i will remember that " + person_name)
        window.update()
        threading.Thread(target=engine_speak("okay, i will remember that " + person_name)).start()
        person_obj.setName(person_name) # remember name in person object
    
    if 'what is my name' in voice_data:
        bot_response.set("Your name must be " + person_obj.name)
        window.update()
        threading.Thread(target=engine_speak("Your name must be " + person_obj.name)).start()
    
    if 'change your name to' in voice_data:
        asis_name = voice_data.split("to")[-1].strip()
        bot_response.set("okay, i will remember that my name is " + asis_name)
        window.update()
        threading.Thread(target=engine_speak("okay, i will remember that my name is " + asis_name)).start()
        brobot_obj.setName(asis_name) # remember name in asis object

    # 3: greeting
    if voice_data in ["how are you","how are you doing"]:
        bot_response.set("I'm very well, thanks for asking " + person_obj.name)
        window.update()
        threading.Thread(target=engine_speak("I'm very well, thanks for asking " + person_obj.name)).start()

    # 4: time
    if 'time' in voice_data:
        current_time = datetime.datetime.now()
        time = current_time.strftime("%H") + " hours and " + current_time.strftime("%M") + " minutes"
        bot_response.set(time)
        window.update()
        threading.Thread(target=engine_speak(time)).start()

    # 5: search google
    if 'search for' in voice_data and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        bot_response.set("Here is what I found for" + search_term + " on google")
        window.update()
        threading.Thread(target=engine_speak("Here is what I found for" + search_term + " on google")).start()
    

    # 6: search youtube
    if 'youtube' in voice_data:
        search_term = voice_data.split("for")[-1]
        search_term = search_term.replace("on youtube","").replace("search","")
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        bot_response.set("Here is what I found for " + search_term + " on youtube")
        window.update()
        threading.Thread(target=engine_speak("Here is what I found for " + search_term + " on youtube")).start()
  
    
     #9 weather
    if 'weather' in voice_data:
        search_term = voice_data.split("for")[-1]
        url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
        webbrowser.get().open(url)
        bot_response.set("Here is what I found for on google")
        window.update()
        threading.Thread(target=engine_speak("Here is what I found for on google")).start()
     

     #11 toss a coin
    if voice_data in ["toss a coin","flip a coin","coin"]:
        moves=["head", "tails"]   
        cmove=random.choice(moves)
        threading.Thread(target=engine_speak("Tossing...")).start()
        
        threading.Thread(target=engine_speak("Its " + cmove)).start()
        bot_response.set("Its " + cmove)
        window.update()

    #exit
    if voice_data in ["exit", "quit"]:
        bot_response.set("bye")
        window.update()
        threading.Thread(target=engine_speak("bye")).start()
        threading.Thread(target=exit()).start()

   # Current location as per Google maps
    if 'what is my exact location' in voice_data:
        url = "https://www.google.com/maps/search/Where+am+I+?/"
        webbrowser.get().open(url)
        bot_response.set("You must be somewhere near here, as per Google maps")
        window.update()
        threading.Thread(target=engine_speak("You must be somewhere near here, as per Google maps")).start()

    #date
    if voice_data in ["what is today's date", "what is the date today", "date"]:
        bot_response.set(today.strftime("%B %d, %Y"))
        window.update()
        threading.Thread(target=engine_speak(today.strftime("%B %d, %Y"))).start()

    #great compliment
    if voice_data in ["great","interesting","wow","awesome","nice"]:
        bot_response.set("I know right")
        window.update()
        threading.Thread(target=engine_speak("I know right")).start()


    #thanks
    if voice_data in ["thanks","thank","thank you"]:
        bot_response.set("You're welcome!")
        window.update()
        threading.Thread(target=engine_speak("You're welcome!")).start()
     
    #open brobot settings
    if voice_data in ["open settings", "open setting"]:
        bot_response.set("Opening settings...")
        window.update()
        threading.Thread(target=engine_speak("Opening settings...")).start()
        threading.Thread(target=swap(settingScreen)).start()

    #return to brobot homescreen
    if voice_data in ["go back", "go back to home screen", "return to home screen"]:
        bot_response.set("Returning to home screen.")
        window.update()
        threading.Thread(target=engine_speak("Returning to home screen .")).start()
        threading.Thread(target=swap(homeScreen)).start()
              
    if voice_data in ["open notepad","write this down","note","take a note"]:
        date = datetime.datetime.now()
        file_name = str(date).replace(":","-")+ "-note.txt"
        bot_response.set("What do you want me to note down?")
        window.update()
        threading.Thread(target=engine_speak("What do you want me to note down?")).start()
        text = record_audio("")
        with open (file_name,"w") as f:
            f.write(text)
        threading.Thread(target=subprocess.Popen(["notepad.exe",file_name])).start()
    
    if voice_data in ["open zoom","class time"]:
        bot_response.set("Opening zoom...")
        window.update()
        threading.Thread(target=engine_speak("Opening zoom")).start()
        zoom = r"C:\Users\Jash\AppData\Roaming\Zoom\bin\zoom.exe"
        threading.Thread(target=subprocess.Popen(zoom)).start()

    if voice_data in ["calculate","open calculator","math"]:
        bot_response.set("Opening calculator...")
        window.update()
        threading.Thread(target=engine_speak("Opening calculator")).start()
        calculator = "C:\Windows\System32\calc.exe"
        threading.Thread(target=subprocess.Popen(calculator)).start()

    if 'roll a die' in voice_data:
        number = random.randrange(1,6)
        threading.Thread(target=engine_speak("Rolling...")).start()
        bot_response.set("Its "+str(number))
        threading.Thread(target=engine_speak("Its "+str(number))).start()
        window.update()

    #tells you my sub count
    if voice_data in ["sub count","what is my sub count","how many subscribers do i have","how many subs do i have"]:
        bot_response.set("Let me check")
        threading.Thread(target=engine_speak("Let me check")).start()
        url = "https://www.youtube.com/c/c0mplicated"
        driver.get(url)
        subcount = selenium(url,"subscriber-count")
        bot_response.set("You have "+subcount)
        threading.Thread(target=engine_speak("You have "+str(subcount))).start()
        window.update()
        driver.close()

    #send message using whatsapp, must be logged in
    if "whatsapp" in voice_data:
        bot_response.set("Okay, loading things up")
        threading.Thread(target=engine_speak("Okay, loading things up")).start()
        whatsapppopup()

    if "what is" in voice_data and "factorial" not in voice_data and "root" not in voice_data:
        try:
            result = mathfunctions.basic(voice_data)
            bot_response.set(result)
            threading.Thread(target=engine_speak(result)).start()
        except Exception:
            bot_response.set("Can you say that again?")
            threading.Thread(target=engine_speak("Can you say that again?")).start()

    if "what is" in voice_data and "factorial" in voice_data:
        try:
            voice_data=voice_data.replace("what is","")
            voice_data=voice_data.replace("factorial","")
            voice_data=voice_data.replace("the","")
            voice_data=voice_data.replace("of","")
            voice_data=voice_data.replace(" ","")
            print(voice_data)
            result = mathfunctions.factorial(voice_data)
            bot_response.set(result)
            threading.Thread(target=engine_speak(result)).start()
        except Exception:
            bot_response.set("Can you say that again?")
            threading.Thread(target=engine_speak("Can you say that again?")).start()

    if "what is" in voice_data and "root" in voice_data:
        try:
            result = mathfunctions.roots(voice_data)
            bot_response.set(result)
            threading.Thread(target=engine_speak(result)).start()
        except Exception:
            bot_response.set("Can you say that again?")
            threading.Thread(target=engine_speak("Can you say that again?")).start()
		
        
 



def whatsapppopup():
    global wcount
    number = 0
    swap(popupScreen)
    threading.Thread(target=engine_speak("Kindly enter the details")).start()
    bot_response.set("Kindly enter the details")
    

def pause():
    time.sleep(0.1)

def submit():
    receiver_num = number_entry.get()
    receiver_message = message_entry.get()
    print(receiver_num)
    print(receiver_message)
    threading.Thread(target=engine_speak("Sending the message")).start()
    bot_response.set("Sending the message") 
    url = 'https://web.whatsapp.com/send?phone='+receiver_num+'&text='+receiver_message
    webbrowser.get().open(url)
    swap(homeScreen)
    time.sleep(10)
    k = Controller()
    k.press(Key.enter)
    threading.Thread(target=engine_speak("Message sent")).start()
    bot_response.set("Message sent")

    
def saved():
    global bgcolor
    global voice
    global volume
    voice = voicevar.get()
    volume = (volume_slider.get()/100)
    theme = var.get()
    print(theme)
    if theme == 1:
        bgcolor = "#0f212c"
    if theme == 2:
        bgcolor = "white"
    homeScreen.config(bg=bgcolor)
    settingScreen.config(bg=bgcolor)
    threading.Thread(target=settingScreen.update()).start()
    threading.Thread(target=homeScreen.update()).start()
    print(volume)
    #print(voice)
    window.update()


today = date.today()
person_obj = person()
brobot_obj = brobot()
brobot_obj.name = 'Brobot'
person_obj.name = ""
engine = pyttsx3.init()


#******************POPUPSCREEN**************************
popupScreen = Frame(window,width = 400, height = 500, bg = bgcolor)
number_entry = Entry(popupScreen, textvariable = receiver_num)
number_entry.place(x=180,y=100)
message_entry = Entry(popupScreen, textvariable = receiver_message)
message_entry.place(x=200,y=200)
submit_btn = Button(popupScreen,text = "Submit", command = lambda: submit())
submit_btn.place(x=300,y=450)
back = Button(popupScreen, text = "back", command = lambda: tohomescreen())
back.config(font=("Courier", 8))
back.place(x=50, y =450)
#************************************************************


#**********************SETTING SCREEN****************************************
settingScreen = Frame(window,width = 400, height = 500, bg = bgcolor)
back = Button(settingScreen, text = "back", command = lambda: tohomescreen())
back.config(font=("Courier", 8))
back.place(x=50, y =450)
canvas3 = Canvas(settingScreen,width=500,height=50,bg = '#0f212c').place(x=-10,y=-20)
setting_txt = Label(settingScreen,text = "Settings", bg = '#0f212c')
setting_txt.config(font=("",15),fg = 'white')
setting_txt.pack(side = "top")
save = Button(settingScreen,text='save',command =lambda: saved())
save.config(font=("Courier",8))
save.place(x=300,y=450)
bot_voices = ['Male','Female']
voicevar = StringVar(window)
voicevar.set('Male')
voices_menu = OptionMenu(settingScreen,voicevar,*bot_voices)
voice_txt= Label(settingScreen, text="Bot Voice",bg = '#0f212c')
voice_txt.config(fg='white')
voice_txt.place(x = 100, y = 100)
voices_menu.place(x=180, y = 100)
volume_slider = Scale(settingScreen, from_=0 ,to = 100,orient = HORIZONTAL)
volume_slider.set("100")
volume_txt = Label(settingScreen,text = "Bot Volume", bg ='#0f212c')
volume_txt.config(fg='white')
volume_txt.place(x=50,y=200)
volume_slider.place(x=200,y=200)
var = IntVar()
darktheme_btn = Radiobutton(settingScreen,text="Dark",variable= var,value = 1).place(x=150,y=300)
lighttheme_btn = Radiobutton(settingScreen,text="Light",variable= var,value = 2).place(x=250,y=300)
var.set(1)
theme_txt=Label(settingScreen,text="Theme", bg ='#0f212c')
theme_txt.config(fg="white")
theme_txt.place(x=50,y=300)
#***************************************************************************


homeScreen = Frame(window,width = 400, height = 500, bg = bgcolor)
window.title("Brobot")

user_label = Label(homeScreen, textvariable = user_response, bg = '#41a2dc') 
user_label.config(font=("", 10))
user_response.set('')
user_label.place(x = 380 , y= 100 , anchor = 'e')

bot_label = Label(homeScreen, textvariable = bot_response, bg = '#0073cb')
bot_label.config(font=("", 10))
bot_response.set("")
bot_label.place(x=20, y=150 , anchor = 'w')

canvas = Frame(homeScreen, bg ='#b3b4b1', width = 400 ,height = 200, bd = 0) #grey canvas
canvas.place(y=380)

bot_label_confirmation = Label(homeScreen , textvariable = bot_confirmation , bg = '#162937')
bot_label_confirmation.config(font=("", 15) , fg = 'white' ,bd = 15)
bot_confirmation.set("Listening...")
bot_label_confirmation.place(x=125, y= 410)

settings = Button(homeScreen, text = "settings", command = lambda: tosettingscreen())
settings.config(font=("", 8))
settings.place(x=310, y =425)

assitant_voice_text = Text(settingScreen)

for frame in (homeScreen,settingScreen,popupScreen):
    frame.grid(row=0,column=0, sticky = 'news')



threading.Thread(target=homeScreen.tkraise()).start()


def voice():
        global voice_data
        while(True):
            voice_data = record_audio("")
            threading.Thread(target=respond(voice_data)).start()

threading.Thread(target=voice()).start()

threading.Thread(target=mainloop()).start()  


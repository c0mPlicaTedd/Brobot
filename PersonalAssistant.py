import math
import tkinter
import ttk
from pyaudio import paUInt8
import speech_recognition as sr # recognise speech
import random # get time details
import webbrowser # open browser
import time
from PIL import Image
import subprocess
import pyttsx3
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
import pyautogui
window = Tk()

global bot_response
global user_response
global bot_confirmation
global voice_data 
global receiver_number
global receiver_message
voice_data = None
global isClicked
isClicked = False
global volume 
volume = 100
global uiBackgroundColour 
uiBackgroundColour = "#0f212c"
global voice
voice = None
bot_response = StringVar()
user_response = StringVar()
bot_confirmation = StringVar()
receiver_number = StringVar()
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

def recordAudio(ask=""):
    with sr.Microphone() as source: 
        if ask:
            threading.Thread(target=engineSpeak(ask)).start()
        audio = sr.Recognizer().listen(source, timeout=None, phrase_time_limit= 7)
        threading.Thread(target=bot_confirmation.set("Listening...")).start()
        threading.Thread(target=window.update()).start()
        voice_data = ''
        try:
            voice_data = sr.Recognizer().recognize_google(audio)
            threading.Thread(target=user_response.set(voice_data)).start() 
            threading.Thread(target=window.update()).start()
        except sr.UnknownValueError: 
            print("I did not get that!")
        except sr.RequestError:
            setBotsReaction('Sorry, the service is down') 
        print(">>", voice_data.lower()) 
        
        
        return voice_data.lower()

def findThroughSelenium(url,id): 
    driver.get(url)
    data = driver.find_element_by_id(id).text
    return data

def setBotsReaction(message):
    bot_response.set(message)
    threading.Thread(target=engineSpeak(message)).start()


def engineSpeak(audio_string): 
    global voice
    audio_string = str(audio_string)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    if voice == 'Female':
        engine.setProperty('voice', voices[1].id) #Some bug here, its not working properly
    engine.setProperty('rate', 150)
    engine.setProperty('volume', volume)
    bot_confirmation.set("Speaking...")
    window.update()
    engine.say(audio_string)
    engine.runAndWait()
    bot_confirmation.set("Listening...")
    window.update()

def respond(voice_data): 
    
    if 'hello' in voice_data: 
        greetingResponses = ["hey", "hey, what's up?", "I'm listening", "how can I help you?", "hello"]
        setBotsReaction(random.choice(greetingResponses))
    
    if 'what is your name' in voice_data: setBotsReaction(f"My name is {brobot_obj.name}. what's your name?")

    if 'my name is' in voice_data: 
        person_name = voice_data.split("is")[-1].strip()
        person_obj.setName(person_name)
        setBotsReaction(f"okay, i will remember that {person_name}.")
    
    if 'what is my name' in voice_data: setBotsReaction(f"Your name must be {person_obj.name}.")
    
    if 'change your name to' in voice_data: 
        asis_name = voice_data.split("to")[-1].strip()
        brobot_obj.setName(asis_name)
        setBotsReaction(f"okay, i will remember that my name is {asis_name}.")

    if checkIfContains(voice_data,['how are you',"how are you doing"]): setBotsReaction(f"I'm very well, thanks for asking {person_obj.name}.")
    
    if 'time' in voice_data: 
        current_time = datetime.datetime.now()
        setBotsReaction(f"{current_time.strftime('%H')} hours and {current_time.strftime('%M')} minutes.")

    if 'search for' in voice_data and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        googleUrl = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(googleUrl)
        setBotsReaction(f"Here is what I found for {search_term} on google.")
    
    if 'youtube' in voice_data: 
        search_term = voice_data.split("for")[-1]
        search_term = search_term.replace("on youtube","").replace("search","")
        youtubeUrl = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(youtubeUrl)
        setBotsReaction(f"Here is what I found for {search_term} on youtube.")
  
    if 'weather' in voice_data: 
        search_term = voice_data.split("for")[-1]
        weatherUrl = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
        webbrowser.get().open(weatherUrl)
        setBotsReaction("Here is what I found for on google.")
    
    if checkIfContains(voice_data,["toss a coin","flip a coin","coin"]):
        coinFlipOutcome=random.choice(["head","tails"])
        threading.Thread(target=engineSpeak("Tossing...")).start()
        setBotsReaction(f"Its {coinFlipOutcome}.")
    
    if checkIfContains(voice_data,["exit", "quit"]):
        setBotsReaction("bye!")
        threading.Thread(target=exit()).start()

    if 'what is my exact location' in voice_data: 
        locationUrl = "https://www.google.com/maps/search/Where+am+I+?/"
        webbrowser.get().open(locationUrl)
        setBotsReaction("You must be somewhere near here, as per Google maps.")
    
    if checkIfContains(voice_data,["what is today's date", "what is the date today", "date"]): setBotsReaction(today.strftime("%B %d, %Y"))

    if checkIfContains(voice_data,["great","interesting","wow","awesome","nice"]): setBotsReaction("I know right!")
    
    if checkIfContains(voice_data,["thanks","thank","thank you"]): setBotsReaction("You're welcome!")
     
    if checkIfContains(voice_data,["open settings", "open setting"]): 
        setBotsReaction("Opening settings...")
        threading.Thread(target=swap(settingScreen)).start()

    
    if checkIfContains(voice_data,["go back", "go back to home screen", "return to home screen"]) : #return to brobot homescreen
        setBotsReaction("Returning to home screen.")
        threading.Thread(target=swap(homeScreen)).start()
              
    if checkIfContains(voice_data,["open notepad","write this down","note","take a note"]): #opens notepad and notes whatever u say
        date = datetime.datetime.now()
        file_name = str(date).replace(":","-")+ "-note.txt"
        setBotsReaction("What do you want me to note down?")
        text = recordAudio("")
        with open (file_name,"w") as f:
            f.write(text)
        threading.Thread(target=subprocess.Popen(["notepad.exe",file_name])).start()
    
    if checkIfContains(voice_data,["open zoom","class time"]): #opens zoom
        setBotsReaction("Opening zoom...")
        zoom = r"C:\Users\Jash\AppData\Roaming\Zoom\bin\zoom.exe"
        threading.Thread(target=subprocess.Popen(zoom)).start()

    if checkIfContains(voice_data,["calculate","open calculator","math"]): #opens calculator
        setBotsReaction("Opening calculator...")
        calculator = "C:\Windows\System32\calc.exe"
        threading.Thread(target=subprocess.Popen(calculator)).start()

    if 'roll a die' in voice_data: #rolls a die
        number = random.randrange(1,6)
        threading.Thread(target=engineSpeak("Rolling...")).start()
        setBotsReaction(f"Its {str(number)}!")

    if checkIfContains(voice_data,["sub count","what is my sub count","how many subscribers do i have","how many subs do i have"]):
        setBotsReaction("Let me check")
        subscriberCountUrl = "https://www.youtube.com/c/c0mplicated"
        driver.get(subscriberCountUrl)
        setBotsReaction(f"You have {findThroughSelenium(subscriberCountUrl,'subscriber-count')}.")
        driver.close()

    if "whatsapp" in voice_data: #send message using whatsapp, must be logged in
        setBotsReaction("Okay, loading things up.")
        whatsappPopUp()

    if "what is" in voice_data and "factorial" not in voice_data and "root" not in voice_data and checkIfContains(voice_data,['+','-','/','plus','minus','multiply','x','into','times','multiplied by','divided by','to the power of','raise to','raised to']):
        #try:
            result = mathfunctions.basic(voice_data)
            print(result)
            setBotsReaction(result)
        #except Exception: setBotsReaction("Can you say that again?")

    if "what is" in voice_data and "factorial" in voice_data:
        try:
            voice_data=voice_data.replace("what is","")
            voice_data=voice_data.replace("factorial","")
            voice_data=voice_data.replace("the","")
            voice_data=voice_data.replace("of","")
            voice_data=voice_data.replace(" ","")
            result = mathfunctions.factorial(voice_data)
            setBotsReaction(result)
        except Exception: setBotsReaction("Can you say that again?")

    if "what is" in voice_data and "root" in voice_data:
        try:
            result = mathfunctions.roots(voice_data)
            setBotsReaction(result)
        except Exception: setBotsReaction("Can you say that again?")

    if "rock paper scissors" in voice_data:
        rockpaperscissorsPossibilities = ["rock","paper","scissors"]
        setBotsReaction("Okay, together in 3")
        setBotsReaction("3")
        setBotsReaction("2")
        setBotsReaction("1")
        rockpaperscissorOutcome = random.choice(rockpaperscissorsPossibilities)
        user_response = recordAudio("")
        print(user_response)
        setBotsReaction(rockpaperscissorOutcome)
        pause(1)
        if user_response=="rock":
            if rockpaperscissorOutcome=="rock": setBotsReaction("Its a tie!")
            if rockpaperscissorOutcome=="paper": setBotsReaction("I win!")
            if rockpaperscissorOutcome=="scissors": setBotsReaction("Oh, i lose.")

        elif user_response=="paper":
            if rockpaperscissorOutcome=="paper": setBotsReaction("Its a tie!")
            if rockpaperscissorOutcome=="scissors": setBotsReaction("I win!")
            if rockpaperscissorOutcome=="rock": setBotsReaction("Oh, i lose.")

        elif user_response=="scissors":
            if rockpaperscissorOutcome=="scissors": setBotsReaction("Its a tie!")
            if rockpaperscissorOutcome=="rock": setBotsReaction("I win!")
            if rockpaperscissorOutcome=="paper": setBotsReaction("Oh, i lose.")
        else: setBotsReaction("You spoke late cheater")

def pause(n):
    time.sleep(n)


def whatsappPopUp():
    swap(popupScreen)
    setBotsReaction("Kindly enter the details.")
    

def submit():
    receiver_number = number_entry.get()
    receiver_message = message_entry.get()
    print(receiver_number)
    print(receiver_message)
    setBotsReaction("Sending the message") 
    url = f'https://web.whatsapp.com/send?phone={receiver_number}&text={receiver_message}'
    webbrowser.get().open(url)
    swap(homeScreen)
    time.sleep(14)
    pyautogui.click(1327,641,button="left")
    time.sleep(1)
    k = Controller()
    k.press(Key.enter)
    setBotsReaction("Message sent")
    number_entry.delete("0","end")
    message_entry.delete("0","end")
    window.update()

    
def ifSettingsSaved(): 
    global uiBackgroundColour
    global voice
    global volume
    voice = voicevar.get()
    volume = (volume_slider.get()/100)
    theme = var.get()
    if theme == 1: uiBackgroundColour = "#0f212c"
    if theme == 2: uiBackgroundColour = "#ffffff"
    threading.Thread(target=settingScreen.update()).start()
    threading.Thread(target=homeScreen.update()).start()
    setBotsReaction("Saved.")

def checkIfContains(text, searchList):
	for word in searchList:
		if word in text:
			return True
	return False

if __name__ == '__main__':
    today = date.today()
    person_obj = person()
    brobot_obj = brobot()
    brobot_obj.name = 'Brobot'
    person_obj.name = ""
    engine = pyttsx3.init()


    #******************WHATSAPPPOPUPSCREEN**************************
    whatsappcolor = '#25D366'
    popupScreen = Frame(window,width = 400, height = 500, bg = uiBackgroundColour)
    number_entry = Entry(popupScreen, textvariable = receiver_number)
    number_entry.place(x=200,y=100)
    message_entry = Entry(popupScreen, textvariable = receiver_message)
    message_entry.place(x=200,y=200)
    popup_txt = Label(popupScreen,text = "Whatsapp Details", bg = '#0f212c')
    popup_txt.config(font=("",15),fg = 'white')
    popup_txt.pack(side = "top")
    number_entry_txt= Label(popupScreen, text="Enter the number",bg = '#0f212c')
    number_entry_txt.config(fg='white')
    number_entry_txt.place(x = 50, y = 100)
    message_txt = Label(popupScreen,text = "Etner the message", bg = '#0f212c')
    message_txt.config(fg='white')
    message_txt.place(x=50,y=200)
    submit_btn = Button(popupScreen,text = "Submit", command = lambda: submit())
    submit_btn.place(x=300,y=450)
    back = Button(popupScreen, text = "back", command = lambda: tohomescreen())
    back.config(font=("Courier", 8))
    back.place(x=50, y =450)
    #************************************************************


    #**********************SETTING SCREEN****************************************
    settingScreen = Frame(window,width = 400, height = 500, bg = uiBackgroundColour)
    back = Button(settingScreen, text = "back", command = lambda: tohomescreen())
    back.config(font=("Courier", 8))
    back.place(x=50, y =450)
    #line = Label(settingScreen,width=400,height=1,bd=0,bg='white')
    #line.place(x=0,y=30)
    setting_txt = Label(settingScreen,text = "Settings", bg = '#0f212c')
    setting_txt.config(font=("",15),fg = 'white')
    setting_txt.pack(side = "top")
    save = Button(settingScreen,text='save',command =lambda: ifSettingsSaved())
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
    volume_slider = Scale(settingScreen, from_=0 ,to = 100,orient = 'horizontal')
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
    assitant_voice_text = Text(settingScreen)
    #***************************************************************************

    #****************************HOME SCREEN***********************************
    homeScreen = Frame(window,width = 400, height = 500, bg = uiBackgroundColour)
    window.title("Brobot")
    user_label = Label(homeScreen, textvariable = user_response, bg = '#41a2dc') 
    user_label.config(font=("", 10))
    user_response.set('')
    user_label.place(x = 380 , y= 100 , anchor = 'e')
    bot_label = Label(homeScreen, textvariable = bot_response, bg = '#0073cb')
    bot_label.config(font=("", 10))
    bot_response.set("")
    bot_label.place(x=20, y=150 , anchor = 'w')
    canvas = Label(homeScreen, bg ='#b3b4b1', width = 400 ,height = 200, bd = 0) #grey canvas
    canvas.place(y=380)
    bot_label_confirmation = Label(homeScreen , textvariable = bot_confirmation , bg = '#162937')
    bot_label_confirmation.config(font=("", 15) , fg = 'white' ,bd = 15)
    bot_confirmation.set("Listening...")
    bot_label_confirmation.place(x=125, y= 410)
    settings = Button(homeScreen, text = "settings", command = lambda: tosettingscreen())
    settings.config(font=("", 8))
    settings.place(x=310, y =425)
    #****************************************************************************


    for frame in (homeScreen,settingScreen,popupScreen):
        frame.grid(row=0,column=0, sticky = 'news')

    threading.Thread(target=homeScreen.tkraise()).start()


    def voice():
            global voice_data
            while True:
                voice_data = recordAudio("")
                threading.Thread(target=respond(voice_data)).start()
                #window.mainloop() pls check if this works here

    threading.Thread(target=voice()).start()

    threading.Thread(target=window.mainloop()).start()  


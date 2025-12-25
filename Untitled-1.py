import speech_recognition as sr  # type: ignore
import pyttsx3  # type: ignore
import datetime
import time
import os
import subprocess
import pyautogui  # type: ignore
import webbrowser
import wikipedia # type: ignore
import pyjokes # type: ignore
import customtkinter as ctk # type: ignore
import threading
import requests  # type: ignore

typing_active = False

# =========================
# Voice Engine
# =========================
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female
engine.setProperty('rate', 180)

def Speak(audio):
    print(f"EREBUS: {audio}")
    engine.say(audio)
    engine.runAndWait()
    time.sleep(0.2)
    add_message(f"EREBUS: {audio}")

# =========================
# Core Functions
# =========================
def Listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"You: {query}")
        add_message(f"You: {query}")
    except Exception as e:
        print("Sorry, I could not recognize. Error:", e)
        return ""
    return query.lower()

def Wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        greeting = "Good morning Shubh."
    elif 12 <= hour < 18:
        greeting = "Good afternoon Shubh."
    else:
        greeting = "Good evening Shubh."
    Speak(f"{greeting} I am EREBUS, your AI assistant. How can I help you?")

def TellTime():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    Speak(f"The time is {strTime}")

def TellDate():
    today = datetime.datetime.now().strftime("%A, %d %B %Y")
    Speak(f"Today is {today}")

def OpenNotepad():
    try:
        subprocess.Popen("notepad.exe")
        Speak("Notepad is now open")
    except:
        Speak("Sorry, I could not open Notepad")

def CloseNotepad():
    try:
        os.system("taskkill /f /im notepad.exe")
        Speak("I have closed Notepad for you")
    except:
        Speak("Sorry, I could not close Notepad")
def TypeInNotepadVoice():
    global typing_active
    typing_active = True
    Speak("I am ready to type. Say 'stop typing' when you want me to stop.")
    time.sleep(1)
    while typing_active:
        content = Listen()
        if "stop typing" in content:
            typing_active = False
            Speak("Okay, I stopped typing.")
            break
        elif content:
            pyautogui.typewrite(content + "\n", interval=0.05)

def TypeInNotepadText(text):
    Speak("Typing in Notepad for you")
    time.sleep(1)
    pyautogui.typewrite(text + "\n", interval=0.05)
    
def OpenChrome():
    try:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        os.startfile(chrome_path)
        Speak("Opening Google Chrome")
    except:
        Speak("Sorry, I could not open Chrome")

def OpenWebsiteInChrome(site):
    try:
        url = f"https://www.{site}.com"
        os.system(f'start chrome "{url}"')
        Speak(f"Opening {site} in Chrome")
    except:
        Speak(f"Sorry, I could not open {site}")

def OpenCalculator():
    try:
        os.system("calc")
        Speak("Opening Calculator")
    except:
        Speak("Sorry, I could not open Calculator")
        
def GoogleSearch(query):
    try:
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        Speak(f"Here are the search results for {query}")
    except:
        Speak("Sorry, I could not perform the search")

def WikiSearch(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        Speak(result)
    except:
        Speak("Sorry, I could not find anything on Wikipedia")

def TellJoke():
    joke = pyjokes.get_joke()
    Speak(joke)

# =========================
# Memory
# =========================
def Remember(text):
    with open("data.txt", "w") as f:
        f.write(text)
    Speak(f"I will remember that {text}")

def Recall():
    try:
        with open("data.txt", "r") as f:
            memory = f.read()
        if memory:
            Speak(f"You told me to remember that {memory}")
        else:
            Speak("I don't have anything remembered right now")
    except FileNotFoundError:
        Speak("I don't have anything remembered yet")

# =========================
# Command Handler
# =========================
def handle_query(query):
    global typing_active

    if "quit" in query or "exit" in query:
        Speak("Goodbye Shubh, take care!")
        root.quit()

    elif "hello" in query:
        Speak("Hello Shubh, I am ready for your command")

    elif "time" in query:
        TellTime()

    elif "date" in query:
        TellDate()

    elif "remember that" in query:
        Speak("What should I remember?")
        memory_text = Listen()
        if memory_text:
            Remember(memory_text)

    elif "what do you remember" in query or "recall" in query:
        Recall()

    elif "open notepad" in query:
        OpenNotepad()
        time.sleep(1)
        Speak("Do you want me to type continuously by voice or just a single line?")
        response = Listen()
        if "voice" in response:
            TypeInNotepadVoice()
        else:
            Speak("What should I write in Notepad?")
            content = Listen()
            if content:
                TypeInNotepadText(content)

    elif "close notepad" in query:
        CloseNotepad()

    elif "stop typing" in query:
        typing_active = False
        Speak("Okay, I stopped typing in Notepad")

    elif "open chrome" in query:
        OpenChrome()

    elif "open youtube" in query:
        OpenWebsiteInChrome("youtube")

    elif "open google" in query:
        OpenWebsiteInChrome("google")

    elif "open facebook" in query:
        OpenWebsiteInChrome("facebook")

    elif "open calculator" in query:
        OpenCalculator()

    elif "search for" in query:
        search_term = query.replace("search for", "").strip()
        GoogleSearch(search_term)

    elif "wikipedia" in query:
        topic = query.replace("wikipedia", "").strip()
        WikiSearch(topic)

    elif "joke" in query:
        TellJoke()

# =========================
# UI with CustomTkinter
# =========================
def run_sympto():
    query = Listen()
    if query:
        handle_query(query)

def start_sympto():
    threading.Thread(target=run_sympto).start()

def add_message(msg):
    chat_display.configure(state="normal")
    chat_display.insert("end", msg + "\n")
    chat_display.configure(state="disabled")
    chat_display.see("end")
#_________________________
#APP UI
#_________________________

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("🤖 EREBUS AI Assistant")
root.geometry("1000x800")

chat_display = ctk.CTkTextbox(root, width=580, height=380, state="disabled")
chat_display.pack(padx=10, pady=10)

btn_frame = ctk.CTkFrame(root)
btn_frame.pack(pady=10)

btn_speak = ctk.CTkButton(btn_frame, text="🎤 Speak", command=start_sympto)
btn_speak.grid(row=0, column=0, padx=10)

btn_exit = ctk.CTkButton(btn_frame, text="❌ Exit", command=root.quit)
btn_exit.grid(row=0, column=1, padx=10)

# Start with a greeting
threading.Thread(target=Wish).start()

root.mainloop()


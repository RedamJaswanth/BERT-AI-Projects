import speech_recognition as sr
import pyttsx3 as pt
import pywhatkit as pk
import webbrowser
import subprocess
import os

# Voice recognition
listening = sr.Recognizer()

# Text to speech
engine = pt.init()


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def hear():
    cmd = ""

    try:
        with sr.Microphone() as mic:
            print("Listening...")
            speak("Listening")

            listening.adjust_for_ambient_noise(mic, duration=0.5)

            voice = listening.listen(mic)

            cmd = listening.recognize_google(voice)
            cmd = cmd.lower()

            print("You said:", cmd)

            # Wake word
            if "Jaanu" in cmd:
                cmd = cmd.replace("Jaanu", "").strip()

    except Exception as e:
        print("Error:", e)

    return cmd


def open_application(cmd):

    if "notepad" in cmd:
        speak("Opening Notepad")
        subprocess.Popen("notepad.exe")

    elif "calculator" in cmd:
        speak("Opening Calculator")
        subprocess.Popen("calc.exe")

    elif "paint" in cmd:
        speak("Opening Paint")
        subprocess.Popen("mspaint.exe")

    else:
        speak("Application not found")


def run():

    speak("Hello, I am Jaanu. How can I help you?")

    while True:

        cmd = hear()

        # Open YouTube
        if "open youtube" in cmd:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        # Open Google
        elif "open google" in cmd:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        # Play song on YouTube
        elif "play" in cmd:
            song = cmd.replace("play", "").strip()

            if song:
                speak("Playing " + song)
                pk.playonyt(song)

            else:
                speak("Please tell me the song name")

        # Open applications
        elif "open" in cmd:
            open_application(cmd)

        # Exit assistant
        elif "exit" in cmd or "stop" in cmd or "bye" in cmd:
            speak("Goodbye. Have a nice day!")
            break

        # Unknown command
        elif cmd:
            speak("Sorry, I did not understand that command")


run()
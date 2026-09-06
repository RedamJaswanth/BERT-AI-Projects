import speech_recognition as sr
import pyttsx3 as pt
import pywhatkit as pk

listening = sr.Recognizer()
engine = pt.init()   # ✅ fixed


def speak(text):
    engine.say(text)
    engine.runAndWait()

def hear():
    cmd = ""   # ✅ initialize variable
    try:
        with sr.Microphone() as mic:
            print("Listening...")
            voice = listening.listen(mic)
            cmd = listening.recognize_google(voice)
            cmd = cmd.lower()

            if "kodi" in cmd:
                cmd = cmd.replace("kodi", "")
                print(cmd)

    except Exception as e:
        print("Error:", e)

    return cmd

def run():
    cmd = hear()

    if "play" in cmd:
        song = cmd.replace("play", "")
        speak("Playing " + song)
        pk.playonyt(song)   # ✅ fixed
run()

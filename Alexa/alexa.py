import speech_recognition as sr
import pyttsx3
import pywhatkit as pk
import webbrowser
import subprocess
from datetime import datetime
import wikipedia


# =====================================
# VOICE RECOGNITION SETUP
# =====================================

listener = sr.Recognizer()


# =====================================
# TEXT TO SPEECH SETUP
# =====================================

engine = pyttsx3.init()
engine.setProperty("rate", 170)


def speak(text):
    """Speak and print assistant response."""

    print("Jaanu:", text)

    engine.say(text)
    engine.runAndWait()


# =====================================
# LISTEN TO USER
# =====================================

def hear():

    command = ""

    try:

        with sr.Microphone() as source:

            print("\nListening...")

            # Adjust microphone for background noise
            listener.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            # Listen to user voice
            voice = listener.listen(
                source,
                timeout=5,
                phrase_time_limit=7
            )

            # Convert voice to text
            command = listener.recognize_google(
                voice
            ).lower()

            print("You said:", command)

            # ---------------------------------
            # REMOVE WAKE WORD VARIATIONS
            # ---------------------------------

            wake_words = [
                "hey jaanu",
                "hey janu",
                "hello jaanu",
                "hello janu",
                "jaanu",
                "janu",
                "jano"
            ]

            for word in wake_words:

                if word in command:
                    command = command.replace(
                        word,
                        ""
                    ).strip()

            # Remove unwanted extra words
            command = command.strip()

            print("Command:", command)

    except sr.WaitTimeoutError:

        print("No voice detected.")


    except sr.UnknownValueError:

        print("Could not understand the voice.")


    except sr.RequestError:

        speak(
            "Speech recognition service is unavailable. "
            "Please check your internet connection."
        )


    except Exception as error:

        print("Error:", error)


    return command


# =====================================
# OPEN WINDOWS APPLICATIONS
# =====================================

def open_application(command):

    applications = {

        "notepad": "notepad.exe",

        "calculator": "calc.exe",

        "paint": "mspaint.exe",

        "command prompt": "cmd.exe",

        "cmd": "cmd.exe",

        "file explorer": "explorer.exe",

        "explorer": "explorer.exe"
    }

    for name, program in applications.items():

        if name in command:

            speak(
                f"Opening {name}"
            )

            try:

                subprocess.Popen(
                    program
                )

            except Exception as error:

                print(
                    "Application Error:",
                    error
                )

                speak(
                    "Sorry, I could not open that application."
                )

            return

    speak(
        "Sorry, I could not find that application."
    )


# =====================================
# GOOGLE SEARCH
# =====================================

def google_search(command):

    query = command

    query = query.replace(
        "search google",
        ""
    )

    query = query.replace(
        "search",
        ""
    )

    query = query.replace(
        "google",
        ""
    )

    query = query.strip()

    if query:

        speak(
            f"Searching Google for {query}"
        )

        webbrowser.open(
            "https://www.google.com/search?q="
            + query.replace(" ", "+")
        )

    else:

        speak(
            "Please tell me what you want to search."
        )


# =====================================
# YOUTUBE SEARCH
# =====================================

def youtube_search(command):

    query = command

    query = query.replace(
        "search youtube",
        ""
    )

    query = query.replace(
        "search on youtube",
        ""
    )

    query = query.strip()

    if query:

        speak(
            f"Searching YouTube for {query}"
        )

        webbrowser.open(
            "https://www.youtube.com/results?search_query="
            + query.replace(" ", "+")
        )

    else:

        speak(
            "Please tell me what you want to search on YouTube."
        )


# =====================================
# WIKIPEDIA SEARCH
# =====================================

def wikipedia_search(command):

    query = command

    query = query.replace(
        "who is",
        ""
    )

    query = query.replace(
        "what is",
        ""
    )

    query = query.strip()

    try:

        speak(
            "Searching for information."
        )

        information = wikipedia.summary(
            query,
            sentences=2
        )

        speak(
            information
        )

    except wikipedia.DisambiguationError:

        speak(
            "There are multiple results for that. "
            "Please be more specific."
        )

    except wikipedia.PageError:

        speak(
            "Sorry, I could not find information about that."
        )

    except Exception as error:

        print(
            "Wikipedia Error:",
            error
        )

        speak(
            "Sorry, something went wrong while searching."
        )


# =====================================
# MAIN VOICE ASSISTANT
# =====================================

def run():

    speak(
        "Hello. I am Jaanu, your AI voice assistant. "
        "How can I help you?"
    )

    while True:

        command = hear()

        # If no command was detected
        if not command:

            continue


        # =================================
        # OPEN YOUTUBE
        # =================================

        if "open youtube" in command:

            speak(
                "Opening YouTube"
            )

            webbrowser.open(
                "https://www.youtube.com"
            )


        # =================================
        # OPEN GOOGLE
        # =================================

        elif "open google" in command:

            speak(
                "Opening Google"
            )

            webbrowser.open(
                "https://www.google.com"
            )


        # =================================
        # SEARCH YOUTUBE
        # =================================

        elif (
            "search youtube" in command
            or "search on youtube" in command
        ):

            youtube_search(
                command
            )


        # =================================
        # PLAY SONG
        # =================================

        elif command.startswith("play"):

            song = command.replace(
                "play",
                ""
            ).strip()

            if song:

                speak(
                    f"Playing {song}"
                )

                pk.playonyt(
                    song
                )

            else:

                speak(
                    "Please tell me the song name."
                )


        # =================================
        # GOOGLE SEARCH
        # =================================

        elif (
            command.startswith("search")
            or command.startswith("google")
        ):

            google_search(
                command
            )


        # =================================
        # CURRENT TIME
        # =================================

        elif (
            "what is the time" in command
            or "tell me the time" in command
            or command == "time"
        ):

            current_time = datetime.now().strftime(
                "%I:%M %p"
            )

            speak(
                f"The current time is {current_time}"
            )


        # =================================
        # CURRENT DATE
        # =================================

        elif (
            "date" in command
            or "today" in command
            or "day" in command
        ):

            today = datetime.now().strftime(
                "%A, %d %B %Y"
            )

            speak(
                f"Today is {today}"
            )


        # =================================
        # WIKIPEDIA INFORMATION
        # =================================

        elif (
            command.startswith("who is")
            or command.startswith("what is")
        ):

            wikipedia_search(
                command
            )


        # =================================
        # OPEN WINDOWS APPLICATION
        # =================================

        elif command.startswith("open"):

            open_application(
                command
            )


        # =================================
        # EXIT
        # =================================

        elif (
            "exit" in command
            or "stop" in command
            or "bye" in command
            or "goodbye" in command
        ):

            speak(
                "Goodbye. Have a nice day!"
            )

            break


        # =================================
        # UNKNOWN COMMAND
        # =================================

        else:

            speak(
                "Sorry, I did not understand that command."
            )


# =====================================
# START PROGRAM
# =====================================

if __name__ == "__main__":

    run()
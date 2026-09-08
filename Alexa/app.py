import streamlit as st
from streamlit_mic_recorder import speech_to_text
from urllib.parse import quote
import webbrowser
import pywhatkit as pk

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Jaanu AI Voice Assistant",
    page_icon="🤖",
    layout="wide"
)


if "last_command" not in st.session_state:
    st.session_state.last_command = ""

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

if "last_action" not in st.session_state:
    st.session_state.last_action = ""

if "last_data" not in st.session_state:
    st.session_state.last_data = ""


def process_command(command):

    command = command.lower().strip()

    # Remove wake words
    wake_words = [
        "hey jaanu",
        "hi jaanu",
        "hello jaanu",
        "jaanu",
        "hey janu",
        "hi janu",
        "hello janu",
        "janu"
    ]

    for word in wake_words:
        command = command.replace(word, "").strip()


    # ==========================================
    # OPEN YOUTUBE
    # ==========================================

    if "open youtube" in command:

        return (
            "Opening YouTube for you!",
            "website",
            "https://www.youtube.com"
        )


    # ==========================================
    # OPEN GOOGLE
    # ==========================================

    elif "open google" in command:

        return (
            "Opening Google for you!",
            "website",
            "https://www.google.com"
        )


    # ==========================================
    # SEARCH GOOGLE
    # ==========================================

    elif command.startswith("search"):

        query = command.replace("search", "", 1).strip()

        if query:

            search_url = (
                "https://www.google.com/search?q="
                + quote(query)
            )

            return (
                f"Searching Google for {query}",
                "website",
                search_url
            )

        return (
            "Please tell me what you want to search.",
            "",
            ""
        )


    # ==========================================
    # PLAY SONG
    # ==========================================

    elif command.startswith("play"):

        song = command.replace("play", "", 1).strip()

        if song:

            return (
                f"Playing {song} on YouTube.",
                "song",
                song
            )

        return (
            "Please tell me the song name.",
            "",
            ""
        )


    # ==========================================
    # UNKNOWN COMMAND
    # ==========================================

    else:

        return (
            "Sorry, I did not understand that command.",
            "",
            ""
        )


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 50% 20%,
                #132238 0%,
                #07111f 45%,
                #02060d 100%
            );
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1000px;
    }

    .jaanu-title {
        text-align: center;
        font-size: 64px;
        font-weight: bold;
        letter-spacing: 8px;
        color: #00d9ff;

        text-shadow:
            0 0 10px #00d9ff,
            0 0 25px #00d9ff,
            0 0 45px #0066ff;
    }

    .jaanu-subtitle {
        text-align: center;
        font-size: 16px;
        letter-spacing: 4px;
        color: #9ccaff;
        margin-bottom: 30px;
    }

    .ai-circle {
        width: 200px;
        height: 200px;

        margin: 25px auto;

        border-radius: 50%;

        display: flex;
        align-items: center;
        justify-content: center;

        font-size: 80px;

        border: 3px solid #00d9ff;

        box-shadow:
            0 0 20px #00d9ff,
            0 0 50px #0066ff,
            inset 0 0 30px #00d9ff;

        animation: pulse 2s infinite;
    }

    @keyframes pulse {

        0% {
            transform: scale(1);
        }

        50% {
            transform: scale(1.08);
        }

        100% {
            transform: scale(1);
        }

    }

    .wave {
        text-align: center;
        font-size: 25px;
        letter-spacing: 8px;
        color: #00d9ff;
    }

    .status {
        text-align: center;
        color: #00ff88;
        font-size: 16px;
        letter-spacing: 2px;
        margin-top: 15px;
    }

    .user-box {

        padding: 18px;
        margin-top: 15px;

        border-radius: 12px;

        background: #102b45;

        border-left: 5px solid #00d9ff;

        font-size: 18px;
    }

    .ai-box {

        padding: 18px;
        margin-top: 15px;

        border-radius: 12px;

        background: #123d35;

        border-left: 5px solid #00ff88;

        font-size: 18px;
    }

    .conversation-title {

        margin-top: 50px;

        text-align: center;

        color: #00d9ff;

        font-size: 28px;

        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="jaanu-title">JAANU</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="jaanu-subtitle">YOUR PERSONAL AI VOICE ASSISTANT</div>',
    unsafe_allow_html=True
)


# ==================================================
# AI VISUAL
# ==================================================

st.markdown(
    '<div class="ai-circle">🤖</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="wave">○ ○ ○ ○ ○ ○ ○</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="status">● STATUS: READY TO LISTEN</div>',
    unsafe_allow_html=True
)


# ==================================================
# MICROPHONE
# ==================================================

st.write("")
st.write("")

st.markdown("## 🎤 Speak to Jaanu")

text = speech_to_text(
    language="en",
    start_prompt="🎤 CLICK TO SPEAK",
    stop_prompt="⏹️ STOP RECORDING",
    just_once=True,
    use_container_width=True,
    key="jaanu_voice"
)


# ==================================================
# PROCESS VOICE INPUT
# ==================================================

if text:

    if text != st.session_state.last_command:

        # Process command
        response, action, data = process_command(text)

        # Save conversation
        st.session_state.last_command = text
        st.session_state.last_response = response
        st.session_state.last_action = action
        st.session_state.last_data = data

# ==================================================
# DISPLAY CONVERSATION
# ==================================================

# ==========================================
# EXECUTE COMMAND
# ==========================================

if st.session_state.last_action == "website":

    website_url = st.session_state.last_data

    if website_url:
        webbrowser.open_new_tab(website_url)

    # Clear action
    st.session_state.last_action = ""
    st.session_state.last_data = ""


elif st.session_state.last_action == "song":

    song_name = st.session_state.last_data

    if song_name:
        pk.playonyt(song_name)

    # Clear action
    st.session_state.last_action = ""
    st.session_state.last_data = ""
# ==================================================
# CONVERSATION TITLE
# ==================================================

st.markdown(
    '<div class="conversation-title">💬 CONVERSATION</div>',
    unsafe_allow_html=True
)


# ==================================================
# DEFAULT CONVERSATION
# ==================================================

if not st.session_state.last_command:

    st.markdown(
        """
        <div class="user-box">
            👤 <b>You:</b> Ready to give a command...
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="ai-box">
            🤖 <b>Jaanu:</b> Hello! How can I help you today?
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="
        text-align:center;
        color:#6fa8dc;
        letter-spacing:2px;
        padding-bottom:30px;
    ">
        JAANU AI VOICE ASSISTANT • VERSION 1.0
    </div>
    """,
    unsafe_allow_html=True
)
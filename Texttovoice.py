from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
import pyttsx3  # Import the text-to-speech library
import re  # Import regex for removing special characters
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

def initialize_tts_engine(voice_index=0, rate=150):
    voices = tts_engine.getProperty('voices')
    if voices and 0 <= voice_index < len(voices):
        tts_engine.setProperty('voice', voices[voice_index].id)  # Set to the specified voice
    else:
        logger.warning("Invalid voice index, using default voice")
    tts_engine.setProperty('rate', rate)  # Adjust the rate as needed

# Initialize with default settings
initialize_tts_engine()

# Initialize the agent
agent = Agent(
    model = Groq(id="llama-3.3-70b-versatile"),
    version = "latest",
    tools = [],
    markdown=True,
    show_tool_calls=True,
    instructions=[
        "Generate a simple short story",
        "Keep the story engaging and concise"
    ],
    debug_mode=False
)

def generate_story(user_input):
    logger.info("Generating story using the agent")
    response = agent.run(user_input).content
    if response:
        clean_response = re.sub(r'[^\w\s]', '', response)
        logger.info("Generated story: %s", clean_response)
        return clean_response
    else:
        logger.error("The agent did not provide a response")
        return None

def speak_text(text):
    logger.info("Converting text to speech: %s", text)
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except RuntimeError as e:
        logger.error("Error in speak_text: %s", e)
        # If the loop is already running, stop it and try again
        tts_engine.stop()
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        logger.error("Unexpected error in speak_text: %s", e)
    finally:
        tts_engine.stop()

if __name__ == '__main__':
    try:
        logger.info("Starting the text-to-speech server")
        response = generate_story("Write a short story about a magical adventure")
        speak_text(response)
    except Exception as e:
        logger.error("Error in main: %s", e)
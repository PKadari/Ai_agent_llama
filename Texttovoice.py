from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
import logging
import pyttsx3  # Import the text-to-speech library

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the text-to-speech engine
try:
    tts_engine = pyttsx3.init()
    logger.info("Text-to-speech engine initialized successfully.")
except Exception as e:
    logger.exception("Failed to initialize text-to-speech engine: %s", e)
    print("Failed to initialize text-to-speech engine. Please check the logs for more details.")
    tts_engine = None

# Check and set the voice
if tts_engine:
    voices = tts_engine.getProperty('voices')
    if voices:
        tts_engine.setProperty('voice', voices[0].id)  # Set to the first available voice
        logger.info("Voice set to: %s", voices[0].id)
    else:
        logger.warning("No voices found for text-to-speech engine.")

    # Set speech rate (optional)
    tts_engine.setProperty('rate', 150)  # Adjust the rate as needed
    logger.info("Speech rate set to: %d", 150)
else:
    logger.error("Text-to-speech engine is not available.")

# Test the text-to-speech engine with a simple phrase
if tts_engine:
    try:
        test_phrase = "This is a test of the text-to-speech engine."
        logger.info("Testing text-to-speech engine with phrase: %s", test_phrase)
        tts_engine.say(test_phrase)
        tts_engine.runAndWait()
        logger.info("Text-to-speech test completed.")
    except Exception as e:
        logger.exception("An error occurred during the text-to-speech test: %s", e)
else:
    logger.error("Text-to-speech engine is not available for testing.")

try:
    agent = Agent(
        model = Groq(id="llama-3.3-70b-versatile"),
        # use latest data to get the best results
        version = "latest",
        tools = [YFinanceTools(stock_price=True, stock_fundamentals=True, analyst_recommendations=True)],
        markdown=True,
        show_tool_calls=True,
        instructions=[
            "Use table to display the data",
            "Provide a summary of the stock performance",
            "Highlight key financial metrics",
            "Include analyst recommendations"
        ],
        debug_mode=False
    )

    # Ensure the agent is properly initialized before calling print_response
    if agent:
        response = agent.print_response("analyze NVDA")
        logger.info("Agent response: %s", response)
        print(response)
        
        # Convert the response text to speech
        if tts_engine:
            logger.info("Starting text-to-speech conversion.")
            tts_engine.say(response)
            tts_engine.runAndWait()
            logger.info("Text-to-speech conversion completed.")
            
            # Additional debugging: Save the speech to a file
            tts_engine.save_to_file(response, 'output.mp3')
            tts_engine.runAndWait()
            logger.info("Text-to-speech saved to output.mp3.")
        else:
            logger.error("Text-to-speech engine is not available for conversion.")
    else:
        logger.error("Failed to initialize the agent.")
        print("Failed to initialize the agent.")
except Exception as e:
    logger.exception("An error occurred while initializing the agent or processing the request: %s", e)
    print("An error occurred. Please check the logs for more details.")

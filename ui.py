import pyttsx3
from Texttovoice import generate_story, speak_text

def list_voices(engine):
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"Voice {index}: {voice.name}")

def select_voice(engine, voice_index):
    voices = engine.getProperty('voices')
    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    else:
        print("Invalid voice index")

def text_to_speech(engine, text):
    engine.say(text)
    engine.runAndWait()
    # iwant the ability to pause the speech and resume it and forword and backward the speech
    # engine.stop()


def main():
    engine = pyttsx3.init()
    
    print("Available voices:")
    list_voices(engine)
    
    voice_index = int(input("Select a voice by index: "))
    select_voice(engine, voice_index)
    
    storyname = input("Enter the story you want to convert to speech: ")
    story = generate_story(storyname)
    engine.save_to_file(story, '%s.mp3' % storyname)
    text_to_speech(engine, story)

if __name__ == "__main__":
    main()
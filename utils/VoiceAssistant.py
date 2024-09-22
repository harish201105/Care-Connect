import time

import pyttsx3
import threading


class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Set the speech rate to 150 words per minute
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Use the second voice in the list

    def say(self, sentence: str, new_thread=False):
        def run_speech():
            self.engine.say(sentence)
            self.engine.runAndWait()

        if new_thread:
            threading.Thread(target=run_speech).start()
        else:
            run_speech()


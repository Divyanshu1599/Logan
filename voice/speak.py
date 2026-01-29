import pyttsx3
import threading

# Initialize engine ONCE at module level
engine = pyttsx3.init()

def speak(text):
    def _run():
        engine.say(text)
        engine.runAndWait()

    t = threading.Thread(target=_run, daemon=True)
    t.start()

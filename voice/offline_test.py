import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone(device_index=0) as source:
    print("Speak clearly...")
    r.adjust_for_ambient_noise(source, duration=2)
    audio = r.listen(source)

try:
    print("You said:", r.recognize_sphinx(audio))
except Exception as e:
    print("Error:", e)

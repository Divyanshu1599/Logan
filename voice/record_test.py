import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone(device_index=0) as source:
    print("Speak now for 5 seconds...")
    audio = r.record(source, duration=5)

with open("test.wav", "wb") as f:
    f.write(audio.get_wav_data())

print("Saved test.wav")

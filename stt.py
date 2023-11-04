import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Listen to the microphone
with sr.Microphone() as source:
    print("Say something:")
    audio = recognizer.listen(source)

try:
    # Recognize the speech
    text = recognizer.recognize_google(audio)
    print("You said: " + text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition; {0}".format(e))

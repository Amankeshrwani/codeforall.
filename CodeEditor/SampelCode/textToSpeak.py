import pyttsx3
speak = pyttsx3.init()
def speaker(str):
    speak.say(str)
    speak.runAndWait()
speaker("hello world")
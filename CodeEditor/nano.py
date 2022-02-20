import pyttsx3
def speaker(str):
	print(str)
	speak = pyttsx3.init()
	speak.say(str)
	
	speak.runAndWait()
for i in range(15):
	speaker('hello aman')

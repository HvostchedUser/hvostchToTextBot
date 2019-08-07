import sys
import speech_recognition as sr
argpos=1
recognizer=sr.Recognizer()
while argpos<len(sys.argv):
    with sr.AudioFile(sys.argv[argpos]) as source:
        audio=recognizer.record(source)
    text=recognizer.recognize_google(audio,language='ru-RU')
    print(text)
    argpos=argpos+1

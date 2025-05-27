
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for your command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            speak("Network error.")
    return ""

def control_device(command):
    if "turn on the light" in command:
        speak("Turning on the light.")
    elif "turn off the light" in command:
        speak("Turning off the light.")
    elif "turn on the fan" in command:
        speak("Turning on the fan.")
    elif "turn off the fan" in command:
        speak("Turning off the fan.")
    else:
        speak("Command not recognized.")

def main():
    speak("Welcome to your smart home assistant.")
    while True:
        command = listen()
        if command:
            if "exit" in command or "stop" in command:
                speak("Shutting down. Goodbye!")
                break
            control_device(command)

if __name__ == "__main__":
    main()

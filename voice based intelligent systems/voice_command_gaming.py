
import speech_recognition as sr
import pyttsx3
import keyboard
import time

CONFIG = {
    "activation_word": "computer",
    "commands": {
        "jump": {"keywords": ["jump", "leap"], "key": "space"},
        "fire": {"keywords": ["fire", "shoot", "attack"], "key": "ctrl"},
        "reload": {"keywords": ["reload", "recharge"], "key": "r"},
        "crouch": {"keywords": ["crouch", "duck"], "key": "c"},
        "run": {"keywords": ["run", "sprint"], "key": "shift"}
    }
}

class SpeechEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
        except Exception as e:
            print("Microphone error:", e)
            exit(1)
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 160)

    def listen(self, prompt="Listening..."):
        print(prompt)
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone is listening...")
            try:
                audio = self.recognizer.listen(source, timeout=10)
                print("Audio captured...")
                voice_input = self.recognizer.recognize_google(audio)
                print(f"You said: {voice_input}")
                return voice_input.lower()
            except sr.UnknownValueError:
                print("Could not understand audio.")
                return None
            except sr.RequestError as e:
                print(f"Recognition error: {e}")
                return None
            except sr.WaitTimeoutError:
                print("Listening timed out.")
                return None

    def speak(self, text):
        print(f"[Assistant]: {text}")
        self.tts.say(text)
        self.tts.runAndWait()

class CommandHandler:
    def __init__(self, config):
        self.commands = config["commands"]
        self.activation_word = config["activation_word"]

    def match_command(self, voice_text):
        for cmd, details in self.commands.items():
            for keyword in details["keywords"]:
                if keyword in voice_text:
                    return cmd, details["key"]
        return None, None

class KeyMapper:
    def press_key(self, key):
        print(f"Executing key press: {key}")
        keyboard.press_and_release(key)

def main():
    print("Starting Voice Gaming Assistant...")
    engine = SpeechEngine()
    handler = CommandHandler(CONFIG)
    mapper = KeyMapper()

    engine.speak("Voice Gaming Assistant ready. Say the activation word to begin.")

    while True:
        activation_input = engine.listen("Say activation word (e.g., 'computer')...")
        if activation_input and handler.activation_word in activation_input:
            engine.speak("Listening for commands.")
            break

    while True:
        command_input = engine.listen("Say a game command... (Say 'exit' to stop)")
        if command_input:
            if 'exit' in command_input or 'quit' in command_input:
                engine.speak("Exiting. Goodbye.")
                break
            command, key = handler.match_command(command_input)
            if command and key:
                engine.speak(f"{command} command recognized.")
                mapper.press_key(key)
            else:
                engine.speak("No valid command detected.")
        else:
            engine.speak("I didn't hear a command.")
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")

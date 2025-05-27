
import speech_recognition as sr
import pandas as pd

def load_support_data(file_path='customer_support_data.csv'):
    try:
        data = pd.read_csv(file_path)
        support_data = []
        for _, row in data.iterrows():
            keywords = [kw.strip().lower() for kw in row['keywords'].split(';') if kw.strip()]
            support_data.append({
                'intent': row['intent'],
                'keywords': keywords,
                'response': row['response']
            })
        print(f"Successfully loaded data from {file_path}")
        return support_data
    except FileNotFoundError:
        print(f"Error: Dataset file not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

def recognize_speech():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=5)
            print("Say something!")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("🧠 Transcribing...")
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text.lower()
    except sr.UnknownValueError:
        print("❌ Could not understand audio. Please try again.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred during speech recognition: {e}")
    return ""

def get_response(user_input, support_data):
    if not user_input:
        return "🤖 Sorry, I didn't hear anything or could not understand. Could you please speak?"
    for item in support_data:
        for keyword in item.get('keywords', []):
            if keyword in user_input:
                print(f"(Matched keyword: '{keyword}' for intent '{item['intent']}')")
                return item['response']
    return "🤖 Sorry, I didn't catch that. Could you rephrase or ask about a different topic?"

def virtual_support_system(data_file='customer_support_data.csv'):
    print("Starting Virtual Support System...")
    support_data = load_support_data(data_file)
    if not support_data:
        print("Cannot proceed without support data.")
        return
    print("\nReady to listen. Say 'goodbye' to exit.")
    while True:
        user_input = recognize_speech()
        if user_input:
            if 'goodbye' in user_input:
                print("🤖 Virtual Assistant: Goodbye!")
                break
            response = get_response(user_input, support_data)
            print("🤖 Virtual Assistant:", response)
        else:
            print("🤖 Virtual Assistant: Could you please repeat that?")
        print("-" * 20)

if __name__ == "__main__":
    virtual_support_system()

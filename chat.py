import random
import json
import pyttsx3
import speech_recognition as sr
import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('data.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

bot_name = "Brian"

data = [line.strip().split('\t') for line in intents]

def get(msg):
    available_responses = []
    for input_msg, response in data:
        if msg == input_msg:
            available_responses.append(response)

    if available_responses:
        text_to_speak = random.choice(available_responses)
        return text_to_speak
    else:
        return "I do not understand..."

def speak_message(message):
    engine.say(message)
    engine.runAndWait()

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # Listen for user's spoken input
        with sr.Microphone() as source:
            print("You: (Speak something...)")
            audio = recognizer.listen(source)

        try:
            # Recognize user's speech using Google Web Speech API
            user_input = recognizer.recognize_google(audio)
            print("You:", user_input)
        except sr.UnknownValueError:
            print("Sorry, I could not understand your input.")

        # Bot generates response
        bot_response = get(user_input)
        print("Bot:", bot_response)

        # Speak the bot's response
        speak_message(bot_response)
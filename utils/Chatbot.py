import json
import pickle
import random
import numpy as np
import tensorflow as tf
from fastapi import HTTPException

# Load the chatbot model and related files
try:
    # Load the trained chatbot model
    model = tf.keras.models.load_model('chatbotmodel/chatbot.h5')

    # Load the list of classes (tags) from a pickle file
    with open('chatbotmodel/classes.pkl', 'rb') as f:
        classes = pickle.load(f)

    # Load the list of words from a pickle file
    with open('chatbotmodel/words.pkl', 'rb') as f:
        words = pickle.load(f)

    # Load the intents from a JSON file
    with open('chatbotmodel/intents.json', 'r') as f:
        intents = json.load(f)
except Exception as e:
    # Raise an HTTPException if there's an error loading the files
    raise HTTPException(status_code=500, detail="Internal Server Error")


def preprocess_input(text):
    # Convert the input text to lowercase
    text = text.lower()

    # Tokenize the input text
    tokens = text.split()

    # Create a bag of words representation
    bag = np.zeros(len(words), dtype=int)
    for word in tokens:
        if word in words:
            bag[words.index(word)] = 1
    return np.array([bag])


async def chatbot_response(user_input):
    # Preprocess the user input to create a bag of words
    processed_input = preprocess_input(user_input)

    # Predict the class of the input using the loaded model
    prediction = model.predict(processed_input)
    predicted_class = np.argmax(prediction)
    response_class = classes[predicted_class]

    # Find the corresponding intent and return a random response
    for intent in intents['intents']:
        if intent['tag'] == response_class:
            return random.choice(intent['responses'])

    # Return a default message if the input doesn't match any intent
    return ("Kata-kata tersebut diluar kemampuan kami. Silakan tanyakan sesuatu yang berhubungan dengan nutrisi atau "
            "aplikasi ini.")

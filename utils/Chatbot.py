import json
import pickle
import random
import numpy as np
import tensorflow as tf
from fastapi import HTTPException

# Load the chatbot model and related files
try:
    model = tf.keras.models.load_model('chatbotmodel/chatbot.h5')
    with open('chatbotmodel/classes.pkl', 'rb') as f:
        classes = pickle.load(f)
    with open('chatbotmodel/words.pkl', 'rb') as f:
        words = pickle.load(f)
    with open('chatbotmodel/intents.json', 'r') as f:
        intents = json.load(f)
except Exception as e:
    raise HTTPException(status_code=500, detail="Internal Server Error")


def preprocess_input(text):
    tokens = text.split()
    bag = np.zeros(len(words), dtype=int)
    for word in tokens:
        if word in words:
            bag[words.index(word)] = 1
    return np.array([bag])


async def chatbot_response(user_input):
    processed_input = preprocess_input(user_input)
    prediction = model.predict(processed_input)
    predicted_class = np.argmax(prediction)
    response_class = classes[predicted_class]

    for intent in intents['intents']:
        if intent['tag'] == response_class:
            return random.choice(intent['responses'])
    return "Kata-kata tersebut diluar kemampuan kami. Silakan tanyakan sesuatu yang berhubungan dengan nutrisi atau aplikasi ini."

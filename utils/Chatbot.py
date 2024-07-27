import json
import pickle
import numpy as np
import tensorflow as tf
from fastapi import HTTPException
from transformers import TFBertModel, BertTokenizer

# Initialize BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained("cahya/bert-base-indonesian-522M")
bert_model = TFBertModel.from_pretrained("cahya/bert-base-indonesian-522M")

# Load the chatbot model and related files
try:
    # Load the trained chatbot model
    model = tf.keras.models.load_model('chatbotmodel/chatbot.h5')

    # Load the list of classes (tags) from a pickle file
    with open('chatbotmodel/classes.pkl', 'rb') as f:
        classes = pickle.load(f)

    # Load the intents from a JSON file
    with open('chatbotmodel/intents.json', 'r') as f:
        intents = json.load(f)
except Exception as e:
    # Raise an HTTPException if there's an error loading the files
    raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# Function to get BERT embeddings for a list of texts.
def get_bert_embeddings(texts):
    # Tokenize the input texts and convert them to TensorFlow tensors
    inputs = tokenizer(texts, return_tensors='tf', padding=True, truncation=True, max_length=512)

    # Pass the tokenized inputs through the BERT model to get the model outputs
    outputs = bert_model(**inputs)

    # Extract the last hidden state from the model outputs
    last_hidden_state = outputs.last_hidden_state

    # Calculate the mean of the last hidden state across the token dimension
    mean_embeddings = tf.reduce_mean(last_hidden_state, axis=1)

    # Convert the TensorFlow tensor to a NumPy array and return it
    return mean_embeddings.numpy()


# Asynchronous function to get a response from the chatbot for a given user input
async def chatbot_response(user_input):
    # Get BERT embeddings for the input sentence
    embeddings = get_bert_embeddings([user_input])

    # Reshape embeddings to match model input shape (batch_size, time_steps, features)
    # This step is necessary because the model expects a 3D input tensor
    embeddings = np.expand_dims(embeddings, axis=1)  # Shape (1, 1, 768)

    # Make a prediction using the trained model
    prediction = model.predict(embeddings, verbose=0)

    # Get the index of the highest predicted class
    predicted_class = np.argmax(prediction)

    # Get the corresponding class label from the classes list
    response_class = classes[predicted_class]

    # Find the corresponding intent and return a random response from the intent's responses list
    for intent in intents['intents']:
        if intent['tag'] == response_class:
            return np.random.choice(intent['responses'])

    # Return a default message if the input doesn't match any intent
    return ("Kata-kata tersebut diluar kemampuan kami. Silakan tanyakan sesuatu yang berhubungan dengan nutrisi atau "
            "aplikasi ini.")

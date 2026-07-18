import json
import random
import pickle
import numpy as np

from tensorflow.keras.models import load_model

model = load_model("model/chatbot_model.keras")

# Load the trained vectorizer
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

encoder = pickle.load(open("model/label_encoder.pkl", "rb"))

with open("data/intents.json", "r") as file:
    intents = json.load(file)

responses = {}

for item in intents:
    responses.setdefault(item["category"], [])
    responses[item["category"]].append(item["output"])


def get_response(message):

    X = vectorizer.transform([message]).toarray()

    prediction = model.predict(X, verbose=0)

    index = np.argmax(prediction)

    confidence = prediction[0][index]

    if confidence < 0.50:
        return (
            "Sorry, I couldn't understand your question. "
            "Please contact the student support office."
        )

    tag = encoder.inverse_transform([index])[0]

    if tag in responses:
        return random.choice(responses[tag])

    return "Sorry, I don't know the answer."

import json
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

from tensorflow.keras.utils import to_categorical

from model import build_model

# Load dataset
with open("data/intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)

texts = []
labels = []

# Extract training data
for item in intents:
    texts.append(item["input"])
    labels.append(item["category"])

# Create and fit vectorizer
vectorizer = CountVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(texts).toarray()

# Encode labels
encoder = LabelEncoder()
y = encoder.fit_transform(labels)
y = to_categorical(y)

# Build model
model = build_model(
    input_size=X.shape[1],
    output_size=y.shape[1]
)

# Train model
model.fit(
    X,
    y,
    epochs=200,
    batch_size=8,
    verbose=1
)

# Save model and preprocessing objects
model.save("data/chatbot_model.keras")

with open("data/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("data/label_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("Training completed successfully!")

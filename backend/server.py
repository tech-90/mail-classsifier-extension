from flask import Flask, request, jsonify
import pickle
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
import re
import string

import os
import pickle

# Get the absolute path of the backend directory
base_dir = os.path.abspath(os.path.dirname(__file__))

# Define the paths to the model and vectorizer
vectorizer_path = os.path.join(base_dir, "vectorizer.pkl")
model_path = os.path.join(base_dir, "model.pkl")

# Check if files exist before loading
if not os.path.exists(vectorizer_path):
    raise FileNotFoundError(f"Vectorizer file not found: {vectorizer_path}")

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

# Load vectorizer and model
with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)

with open(model_path, "rb") as f:
    model = pickle.load(f)

print("Vectorizer and Model loaded successfully.")

# Initialize Flask app
app = Flask(__name__)

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    tokens = word_tokenize(text)
    return " ".join(tokens)

# API Route for classification
@app.route("/classify", methods=["POST"])
def classify_email():
    data = request.get_json()
    email_text = data.get("email", "")
    
    processed_text = preprocess_text(email_text)
    vectorized_text = vectorizer.transform([processed_text])
    prediction = model.predict(vectorized_text)[0]
    
    result = "spam" if prediction == 1 else "ham"
    return jsonify({"classification": result})

if __name__ == "__main__":
    app.run(debug=True)

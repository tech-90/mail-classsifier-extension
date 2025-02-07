from flask import Flask, request, jsonify
import pickle
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
import re
import string
import os


import nltk

# Ensure the tokenizer resource is available
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")  # Download missing tokenizer data


# Initialize Flask app
app = Flask(__name__)

# Get the absolute path of the backend directory
base_dir = os.path.abspath(os.path.dirname(__file__))

# Define the paths to the model and vectorizer
vectorizer_path = os.path.join(base_dir, "vectorizer.pkl")
model_path = os.path.join(base_dir, "model.pkl")

# Load vectorizer and model
try:
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    print("✅ Vectorizer and Model loaded successfully.")
except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    exit(1)

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    tokens = word_tokenize(text)
    return " ".join(tokens)

# Root Route to Check Server Status
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🚀 Server is running!"}), 200

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

# Use PORT from environment variables
PORT = int(os.environ.get("PORT", 10000))  # Default 10000 if not set

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)  # Bind to 0.0.0.0

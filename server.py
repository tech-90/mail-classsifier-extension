from flask import Flask, request, jsonify
import pickle
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
import re
import string

import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory

vectorizer_path = os.path.join(base_dir, "vectorizer.pkl")

vectorizer = pickle.load(open(vectorizer_path, "rb"))
# Load vectorizer and model
# vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

model_path = os.path.join(base_dir, "model.pkl")
model = pickle.load(open(model_path, "rb"))
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

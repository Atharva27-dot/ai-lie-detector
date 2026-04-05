from flask import Flask, render_template, request, jsonify
from model import predict
def detect_contradiction(text):
    text = text.lower()
    if "always" in text and "sometimes" in text:
        return True
    return False

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

import random

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data["text"]

    # 🚨 CONTRADICTION CHECK
    if detect_contradiction(text):
        return jsonify({
            "result": "⚠️ Contradictory Statement",
            "score": 50,
            "explanation": "Statement contains conflicting words."
        })

    # ML Prediction
    result, confidence = predict(text)

    # 🧠 SENTENCE LENGTH CHECK
    if len(text.split()) < 4:
        confidence += 10

    # 🎲 RANDOM FACTOR
    confidence += random.randint(-5, 5)

    # Limit score
    confidence = max(0, min(100, confidence))

    # Label
    if result == "truth":
        label = "✅ Likely Truth"
        explanation = "Statement contains confident wording."
    else:
        label = "⚠️ Possible Lie"
        explanation = "Statement contains uncertainty patterns."

    return jsonify({
        "result": label,
        "score": round(confidence, 2),
        "explanation": explanation
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
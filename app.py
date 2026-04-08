from flask import Flask, render_template, request, jsonify
from model import predict
import random
from rapidfuzz import fuzz

app = Flask(__name__)

# 🌐 FACT CHECK FUNCTION
def fact_check(text):
    text = text.lower()

    known_facts = [
        "sun rises in the east",
        "earth revolves around the sun",
        "water boils at 100 degrees",
        "humans need oxygen to survive",
        "gravity pulls objects toward earth"
    ]

    for fact in known_facts:
        if fuzz.ratio(text, fact) > 60:
            return True

    return False


# ⚠️ CONTRADICTION DETECTION
def detect_contradiction(text):
    text = text.lower()
    return "always" in text and "sometimes" in text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data["text"]

    # 🌐 FACT CHECK (highest priority)
    if fact_check(text):
        return jsonify({
            "result": "🌐 Verified Fact",
            "score": 95,
            "explanation": "This matches real-world knowledge."
        })

    # ⚠️ CONTRADICTION CHECK
    if detect_contradiction(text):
        return jsonify({
            "result": "⚠️ Contradictory Statement",
            "score": 50,
            "explanation": "Conflicting words detected."
        })

    # 🤖 ML PREDICTION
    result, confidence = predict(text)

    text_lower = text.lower()

    # 🧠 RULE-BASED CORRECTION (STRONG WORDS)
    strong_words = ["always", "definitely", "never", "absolutely"]
    if any(word in text_lower for word in strong_words):
        confidence -= 15   # reduce lie probability

    # ⚠️ UNCERTAINTY DETECTION
    uncertain_words = ["maybe", "probably", "guess", "think", "not sure"]
    if any(word in text_lower for word in uncertain_words):
        confidence += 20   # increase lie probability

    # 🎲 RANDOM SMALL VARIATION
    confidence += random.randint(-5, 5)

    # 🎯 CLAMP VALUE (0–100)
    confidence = max(0, min(100, confidence))

    # 🎯 FINAL DECISION
    if confidence < 40:
        label = "✅ Likely Truth"
        explanation = "Statement appears confident and clear."

    elif confidence > 60:
        label = "⚠️ Possible Lie"
        explanation = "Statement contains uncertainty patterns."

    else:
        label = "🤔 Uncertain"
        explanation = "Mixed signals detected."

    return jsonify({
        "result": label,
        "score": round(confidence, 2),
        "explanation": explanation
    })


if __name__ == "__main__":
    app.run(debug=True)
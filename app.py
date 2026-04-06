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
        "gravity pulls objects towards earth"
    ]

    for fact in known_facts:
        if fuzz.ratio(text, fact) > 60:
            return True

    return False

# 🧠 CONTRADICTION CHECK
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

    # 🌐 FACT CHECK
    if fact_check(text):
        return jsonify({
            "result": "🌐 Verified Fact",
            "score": 95,
            "explanation": "This matches real-world knowledge."
        })

    # ⚠️ CONTRADICTION
    if detect_contradiction(text):
        return jsonify({
            "result": "⚠️ Contradictory Statement",
            "score": 50,
            "explanation": "Conflicting words detected."
        })

    # 🤖 ML
    result, confidence = predict(text)

    # 🎲 Adjust confidence
    if len(text.split()) < 4:
        confidence += 10

    confidence += random.randint(-5, 5)
    confidence = max(0, min(100, confidence))

    # 🎯 FINAL DECISION (FIXED)
    if confidence < 40:
        label = "✅ Likely Truth"
        explanation = "Statement appears confident and clear."

    elif confidence > 60:
        label = "⚠️ Possible Lie"
        explanation = "Statement contains uncertainty patterns."

    else:
        label = "🤔 Uncertain"
        explanation = "Mixed signals detected."

    # ✅ RETURN MUST BE LAST
    return jsonify({
        "result": label,
        "score": round(confidence, 2),
        "explanation": explanation
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
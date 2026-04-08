from flask import Flask, render_template, request, jsonify
from model import predict
import random
from rapidfuzz import fuzz

app = Flask(__name__)

#  FACT CHECK
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


#  CONTRADICTION
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

    # all logic here...

    if "Truth" in label:
        display_score = truth_score
    else:
        display_score = lie_score

    return jsonify({
        "result": label,
        "score": round(display_score, 2),
        "explanation": explanation
    })

    # CONTRADICTION
    if detect_contradiction(text):
        return jsonify({
            "result": " Contradictory Statement",
            "score": 50,
            "explanation": "Conflicting words detected."
        })

    #  ML PREDICTION
    truth_score, lie_score = predict(text)
    text_lower = text.lower()

    #  RULES
    strong_words = ["always", "definitely", "never", "absolutely"]
    uncertain_words = ["maybe", "probably", "guess", "think", "not sure"]

    if any(w in text_lower for w in strong_words):
        lie_score -= 15

    if any(w in text_lower for w in uncertain_words):
        lie_score += 20

    #  SMALL RANDOM ADJUSTMENT
    lie_score += random.randint(-5, 5)

    # CLAMP
    lie_score = max(0, min(100, lie_score))
    truth_score = 100 - lie_score

    # 🎯 FINAL DECISION
    if lie_score < 40:
        label = " Likely Truth"
    elif lie_score > 60:
        label = " Possible Lie"
    else:
        label = " Uncertain"

    #  EXPLANATION
    explanation = f"Truth: {round(truth_score,2)}% | Lie: {round(lie_score,2)}%"

    # highlight detected words
    found = [w for w in uncertain_words if w in text_lower]
    if found:
        explanation += f" | Detected: {', '.join(found)}"

  #  Choose correct score to display
if "Truth" in label:
    display_score = truth_score
else:
    display_score = lie_score

return jsonify({
    "result": label,
    "score": round(display_score, 2),
    "explanation": explanation
})


if __name__ == "__main__":
    app.run(debug=True)

import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

vectorizer = None
model = None

def load_model():
    global vectorizer, model

    if model is not None:
        return

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data = pd.read_csv(os.path.join(BASE_DIR, "dataset.csv"))

    X = data["text"]
    y = data["label"]

    vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words='english')
    X_vec = vectorizer.fit_transform(X)

    model = MultinomialNB()
    model.fit(X_vec, y)


def predict(text):
    load_model()

    text_vec = vectorizer.transform([text])
    probs = model.predict_proba(text_vec)[0]

    truth_prob = probs[0] * 100
    lie_prob = probs[1] * 100

    return truth_prob, lie_prob

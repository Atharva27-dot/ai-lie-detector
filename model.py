import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

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

    vectorizer = TfidfVectorizer(ngram_range=(1,3), stop_words='english')
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_vec, y)

def predict(text):
    load_model()   # ✅ load only when needed

    text_vec = vectorizer.transform([text])
    result = model.predict(text_vec)[0]
    confidence = model.predict_proba(text_vec).max() * 100

    return result, confidence
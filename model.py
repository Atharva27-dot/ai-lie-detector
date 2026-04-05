import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data = pd.read_csv(os.path.join(BASE_DIR, "dataset.csv"))



X = data["text"]
y = data["label"]

# Better vectorizer (captures word patterns)
vectorizer = TfidfVectorizer(ngram_range=(1,2))
X_vec = vectorizer.fit_transform(X)

# Better model
model = MultinomialNB()
model.fit(X_vec, y)

def predict(text):
    text_vec = vectorizer.transform([text])
    result = model.predict(text_vec)[0]
    confidence = model.predict_proba(text_vec).max() * 100
    return result, round(confidence, 2)
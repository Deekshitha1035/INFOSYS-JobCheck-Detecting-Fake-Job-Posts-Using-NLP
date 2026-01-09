import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample training data (replace later if you have dataset)
data = {
    "text": [
        "TCS hiring data analyst",
        "Wipro software engineer job",
        "Pay money to get job",
        "Earn money from home scam",
        "Google job opening",
        "Fake job asking registration fee"
    ],
    "label": ["Real", "Real", "Fake", "Fake", "Real", "Fake"]
}

df = pd.DataFrame(data)

# Vectorization
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(df["text"])
y = df["label"]

# Model
model = LogisticRegression()
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model & vectorizer saved successfully!")

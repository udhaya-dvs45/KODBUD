import streamlit as st
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

nltk.download('stopwords')

# -----------------------------
# Train Model (cached)
# -----------------------------
@st.cache_resource
def train_model():
    df = pd.read_csv("reviews_dataset.csv")

    stop_words = set(stopwords.words('english'))

    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z]', ' ', text)
        words = text.split()
        words = [w for w in words if w not in stop_words]
        return " ".join(words)

    df["cleaned_review"] = df["review"].apply(clean_text)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000
    )

    X = vectorizer.fit_transform(df["cleaned_review"])
    y = df["sentiment"]

    model = MultinomialNB()
    model.fit(X, y)

    return model, vectorizer, clean_text

model, vectorizer, clean_text = train_model()

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("⭐ Sentiment Analysis App")
st.write("Predict sentiment: Positive / Neutral / Negative")

review = st.text_area("Enter your review:")

rating = st.radio(
    "Rate the product:",
    [1, 2, 3, 4, 5],
    format_func=lambda x: "⭐" * x
)

if st.button("Analyze Sentiment"):

    if review.strip() == "":
        st.warning("Please enter a review first.")
    else:
        cleaned = clean_text(review)
        vector = vectorizer.transform([cleaned])
        prediction = model.predict(vector)[0]
        probabilities = model.predict_proba(vector)[0]
        confidence = max(probabilities) * 100

        # Show results in app
        st.success(f"Predicted Sentiment: {prediction}")
        st.info(f"Confidence: {confidence:.2f}%")
        st.write(f"Your Rating: {'⭐'*rating}")

        # -----------------------------
        # SAVE TO CONSOLE ONLY
        # -----------------------------
        print("\n----- New Prediction -----")
        print("Review:", review)
        print("Predicted Sentiment:", prediction)
        print("Confidence:", f"{confidence:.2f}%")
        print("Star Rating:", rating)
        print("---------------------------")

import re
from app.model_loader import text_model, text_model_error, text_vectorizer

def preprocess_text(text):
    # Lowercase
    text = text.lower()

    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def analyze_text(text):
    if text_model is None:
        return {"error": f"Text model unavailable: {text_model_error}"}

    clean_text = preprocess_text(text)
    if not clean_text:
        return {"error": "Text is empty after preprocessing"}

    # If a separate vectorizer exists (ml_module artifacts), transform before predict.
    if text_vectorizer is not None:
        features = text_vectorizer.transform([clean_text])
        pred = text_model.predict(features)[0]
    else:
        pred = text_model.predict([clean_text])[0]

    return {
        "prediction": "Fake" if pred == 1 else "Real"
    }
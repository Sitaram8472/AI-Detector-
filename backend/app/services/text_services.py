import re
from app.model_loader import (
    text_model,
    text_model_error,
    text_vectorizer,
    source_model,
    source_model_error,
)

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

    features = None
    if text_vectorizer is not None:
        features = text_vectorizer.transform([clean_text])

    if features is not None:
        pred = text_model.predict(features)[0]
        ai_probability = None
        if hasattr(text_model, "predict_proba"):
            ai_probability = round(max(text_model.predict_proba(features)[0]) * 100, 2)
    else:
        pred = text_model.predict([clean_text])[0]
        ai_probability = None

    response = {
        "prediction": "Fake" if pred == 1 else "Real",
    }

    if ai_probability is not None:
        response["confidence"] = f"{ai_probability}%"

    if pred == 1:
        if source_model is None:
            response["likely_source"] = f"Unavailable: {source_model_error}"
        elif features is not None:
            source_pred = source_model.predict(features)[0]
            source_prob = round(source_model.predict_proba(features)[0].max() * 100, 2)
            response["likely_source"] = f"{source_pred} ({source_prob}%)"
        else:
            response["likely_source"] = "N/A"
    else:
        response["likely_source"] = "N/A"

    return response
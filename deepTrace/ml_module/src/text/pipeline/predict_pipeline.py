# import joblib
# from src.text.preprocessing.clean_text import clean_text
# from src.text.feature_engineering.tfidf import load_tfidf

# # Load models
# ai_model = joblib.load("models/text/ai_model.pkl")
# source_model = joblib.load("models/text/source_model.pkl")
# vectorizer = load_tfidf()

# def predict(text):
#     cleaned = clean_text(text)
#     X = vectorizer.transform([cleaned])

#     # AI vs Human classifier
#     ai_pred = ai_model.predict(X)[0]

#     # Confidence (margin from decision_function)
#     ai_score = ai_model.decision_function(X)[0]
#     ai_confidence = abs(ai_score)

#     # Source attribution
#     source_pred = source_model.predict(X)[0]
#     source_prob = source_model.predict_proba(X)[0].max() * 100

#     result = {}
#     if ai_pred == 1:  # AI (per Kaggle dataset convention)
#         result["Type"] = "AI Generated"
#         result["Confidence"] = f"{ai_confidence:.2f} (margin)"
#         result["Likely Source"] = f"{source_pred} ({source_prob:.2f}%)"
#     else:  # Human
#         result["Type"] = "Human"
#         result["Confidence"] = f"{ai_confidence:.2f} (margin)"
#         result["Likely Source"] = f"{source_pred} ({source_prob:.2f}%)"

#     return result
import joblib
from src.text.preprocessing.clean_text import clean_text
from src.text.feature_engineering.tfidf import load_tfidf

# Load models
ai_model = joblib.load("models/text/ai_model.pkl")
source_model = joblib.load("models/text/source_model.pkl")
vectorizer = load_tfidf()

def predict(text):
    cleaned = clean_text(text)

    if not cleaned.strip():
        return {"Error": "Text is empty or invalid after cleaning"}

    X = vectorizer.transform([cleaned])

    # ✅ Use predict_proba for clean confidence percentage
    ai_pred = ai_model.predict(X)[0]
    ai_proba = ai_model.predict_proba(X)[0]
    ai_confidence = round(max(ai_proba) * 100, 2)

    result = {}

    if ai_pred == 1:  # AI Generated
        source_pred = source_model.predict(X)[0]
        source_prob = round(source_model.predict_proba(X)[0].max() * 100, 2)

        result["Type"] = "AI Generated"
        result["Confidence"] = f"{ai_confidence}%"
        result["Likely Source"] = f"{source_pred} ({source_prob}%)"

    else:  # Human
        result["Type"] = "Human Written"
        result["Confidence"] = f"{ai_confidence}%"
        # ✅ Don't show source if human — it's not meaningful
        result["Likely Source"] = "N/A"

    return result
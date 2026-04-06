# import pandas as pd
# import joblib
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from src.text.preprocessing.clean_text import clean_text

# # Load dataset
# df = pd.read_csv("dataset/text/raw/source_raw.csv")
# df['clean_text'] = df['text'].apply(clean_text)

# # Load the SAME vectorizer
# vectorizer = joblib.load("models/text/tfidf_vectorizer.pkl")

# # Train source classifier
# X = vectorizer.transform(df['clean_text'])
# y = df['label']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# model = MultinomialNB()
# model.fit(X_train, y_train)

# print("Source Classifier Accuracy:", accuracy_score(y_test, model.predict(X_test)))
# joblib.dump(model, "models/text/source_model.pkl")
# print("Source model trained & saved!")


import os
import pandas as pd
import joblib
from sklearn.naive_bayes import ComplementNB   # ✅ better than MultinomialNB for text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from src.text.preprocessing.clean_text import clean_text

# ✅ Ensure output directory exists
os.makedirs("models/text", exist_ok=True)

# Load dataset
df = pd.read_csv("dataset/text/raw/source_raw.csv")
df['clean_text'] = df['text'].apply(clean_text)

# ✅ Drop empty rows after cleaning
df = df[df['clean_text'].str.strip() != ""]

# Load the SAME unified vectorizer
vectorizer = joblib.load("models/text/tfidf_vectorizer.pkl")

# Train source classifier
X = vectorizer.transform(df['clean_text'])
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y   # ✅ stratify for balanced split
)

model = ComplementNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Source Classifier Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

joblib.dump(model, "models/text/source_model.pkl")
print("Source model trained & saved!")
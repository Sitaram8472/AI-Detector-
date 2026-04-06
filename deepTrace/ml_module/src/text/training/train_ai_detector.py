# import pandas as pd
# import joblib
# from sklearn.svm import LinearSVC
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, classification_report
# from sklearn.feature_extraction.text import TfidfVectorizer
# from src.text.preprocessing.clean_text import clean_text

# # Load datasets
# df_ai = pd.read_csv("dataset/text/raw/ai_human_raw.csv")
# df_source = pd.read_csv("dataset/text/raw/source_raw.csv")

# # Clean text
# df_ai['clean_text'] = df_ai['text'].apply(clean_text)
# df_source['clean_text'] = df_source['text'].apply(clean_text)

# # Build unified TF-IDF on combined corpus
# combined_texts = pd.concat([df_ai['clean_text'], df_source['clean_text']])
# vectorizer = TfidfVectorizer(max_features=5000)
# vectorizer.fit(combined_texts)

# # Save vectorizer once
# joblib.dump(vectorizer, "models/text/tfidf_vectorizer.pkl")
# print("Unified TF-IDF vectorizer saved!")

# # Balance AI dataset (0 = Human, 1 = AI in Kaggle dataset)
# df_ai = df_ai.sample(frac=1, random_state=42)
# min_count = df_ai['label'].value_counts().min()
# df0 = df_ai[df_ai['label'] == 0].head(min_count)  # Human
# df1 = df_ai[df_ai['label'] == 1].head(min_count)  # AI
# df_ai = pd.concat([df0, df1]).sample(frac=1, random_state=42)

# # Train AI detector
# X_ai = vectorizer.transform(df_ai['clean_text'])
# y_ai = df_ai['label']
# X_train, X_test, y_train, y_test = train_test_split(X_ai, y_ai, test_size=0.2, random_state=42)

# ai_model = LinearSVC()
# ai_model.fit(X_train, y_train)

# y_pred = ai_model.predict(X_test)
# print("AI Detector Accuracy:", accuracy_score(y_test, y_pred))
# print(classification_report(y_test, y_pred, target_names=["Human","AI"]))

# joblib.dump(ai_model, "models/text/ai_model.pkl")
# print("AI model trained & saved!")


import os
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from src.text.preprocessing.clean_text import clean_text

# ✅ Ensure output directory exists
os.makedirs("models/text", exist_ok=True)

# Load datasets
df_ai = pd.read_csv("dataset/text/raw/ai_human_raw.csv")
df_source = pd.read_csv("dataset/text/raw/source_raw.csv")

# Clean text
df_ai['clean_text'] = df_ai['text'].apply(clean_text)
df_source['clean_text'] = df_source['text'].apply(clean_text)

# ✅ Drop rows where clean_text is empty after cleaning
df_ai = df_ai[df_ai['clean_text'].str.strip() != ""]
df_source = df_source[df_source['clean_text'].str.strip() != ""]

# Build unified TF-IDF on combined corpus
combined_texts = pd.concat([df_ai['clean_text'], df_source['clean_text']])
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),      # ✅ unigrams + bigrams for better context
    sublinear_tf=True         # ✅ apply log normalization to term frequency
)
vectorizer.fit(combined_texts)

# Save vectorizer once
joblib.dump(vectorizer, "models/text/tfidf_vectorizer.pkl")
print("Unified TF-IDF vectorizer saved!")

# Balance AI dataset (0 = Human, 1 = AI)
df_ai = df_ai.sample(frac=1, random_state=42)
min_count = df_ai['label'].value_counts().min()
df0 = df_ai[df_ai['label'] == 0].head(min_count)  # Human
df1 = df_ai[df_ai['label'] == 1].head(min_count)  # AI
df_ai = pd.concat([df0, df1]).sample(frac=1, random_state=42)

# Train AI detector
X_ai = vectorizer.transform(df_ai['clean_text'])
y_ai = df_ai['label']
X_train, X_test, y_train, y_test = train_test_split(
    X_ai, y_ai, test_size=0.2, random_state=42, stratify=y_ai  # ✅ stratify for balanced split
)

# ✅ Logistic Regression instead of LinearSVC (as defined in project)
ai_model = LogisticRegression(
    max_iter=1000,            # ✅ enough iterations to converge
    C=1.0,                    # regularization strength
    solver='lbfgs',
    random_state=42
)
ai_model.fit(X_train, y_train)

y_pred = ai_model.predict(X_test)
print("AI Detector Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=["Human", "AI"]))

joblib.dump(ai_model, "models/text/ai_model.pkl")
print("AI model trained & saved!")
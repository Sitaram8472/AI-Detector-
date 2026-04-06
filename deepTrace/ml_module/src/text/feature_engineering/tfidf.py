# from sklearn.feature_extraction.text import TfidfVectorizer
# import joblib

# def create_and_save_tfidf(texts):
#     vectorizer = TfidfVectorizer(max_features=5000)
#     X = vectorizer.fit_transform(texts)

#     joblib.dump(vectorizer, "models/text/tfidf_vectorizer.pkl")
#     return X

# def load_tfidf():
#     return joblib.load("models/text/tfidf_vectorizer.pkl")


import joblib

def load_tfidf():
    return joblib.load("models/text/tfidf_vectorizer.pkl")
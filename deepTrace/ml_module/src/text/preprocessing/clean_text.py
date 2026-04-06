# import re
# from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# def clean_text(text):
#     if not isinstance(text, str):
#         return ""
    
#     # Lowercase
#     text = text.lower()
    
#     # Remove URLs
#     text = re.sub(r'http\S+|www\S+', '', text)
    
#     # Remove HTML tags
#     text = re.sub(r'<.*?>', '', text)
    
#     # Keep letters, numbers, and spaces (remove special chars)
#     text = re.sub(r'[^a-z0-9\s]', '', text)
    
#     # Tokenization
#     words = text.split()
    
#     # Remove stopwords
#     words = [word for word in words if word not in ENGLISH_STOP_WORDS]
    
#     return " ".join(words)

import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def clean_text(text):
    if not isinstance(text, str):
        return ""

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Keep letters, numbers, spaces only
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # Tokenize
    words = text.split()

    # Remove stopwords
    words = [word for word in words if word not in ENGLISH_STOP_WORDS]

    # ✅ Remove very short tokens (length <= 1) that add no meaning
    words = [word for word in words if len(word) > 1]

    # ✅ Collapse extra whitespace
    return " ".join(words).strip()
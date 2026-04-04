import re
from app.services.web_search_service import search_google

# 🔹 Clean text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text


# 🔹 Web plagiarism check (IMPROVED)
def check_web_plagiarism(text):
    sentences = re.split(r"[.!?\n]+", text)

    matches = []

    for sentence in sentences[:5]:   # 🔥 limit API usage
        sentence = re.sub(r"\s+", " ", sentence).strip()

        if len(sentence) < 40:
            continue

        # Keep search queries small and stable.
        sentence = sentence[:220]

        result = search_google(sentence)

        if result:
            matches.append(result.get("link"))

    if len(matches) > 0:
        return "YES", matches[0]

    return "NO", None


# 🔹 Simple AI detection
def detect_ai_text(text):
    words = text.split()
    if len(words) == 0:
        return 0.0

    avg_len = sum(len(w) for w in words) / len(words)

    return 0.7 if avg_len > 5 else 0.3


# 🔹 FINAL FUNCTION
def analyze_file(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    clean_text = preprocess_text(text)

    web_status, web_source = check_web_plagiarism(text)
    ai_score = detect_ai_text(clean_text)

    return {
        "plagiarism": web_status,
        "source": web_source,
        "ai_generated_percentage": round(ai_score * 100, 2),
        "human_written_percentage": round((1 - ai_score) * 100, 2)
    }
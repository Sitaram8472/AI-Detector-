import re
from difflib import SequenceMatcher

from app.services.web_search_service import search_google


MIN_SENTENCE_LEN = 18
MAX_CHUNKS_TO_CHECK = 20
MATCH_THRESHOLD = 0.42
SHORT_TEXT_THRESHOLD = 0.35


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text):
    parts = re.split(r"[.!?\n]+", text)
    return [re.sub(r"\s+", " ", part).strip() for part in parts if part.strip()]


def similarity(a, b):
    a = preprocess_text(a)
    b = preprocess_text(b)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def build_chunks(text):
    sentences = split_sentences(text)
    if not sentences:
        return []

    chunks = []

    # Single sentences
    for sentence in sentences:
        if len(sentence) >= MIN_SENTENCE_LEN:
            chunks.append(sentence)

    # Consecutive sentence windows to catch copied paragraphs
    for window in (2, 3):
        for i in range(len(sentences) - window + 1):
            chunk = " ".join(sentences[i : i + window]).strip()
            if len(chunk) >= MIN_SENTENCE_LEN:
                chunks.append(chunk)

    # If text is very short, keep the whole text too
    whole = " ".join(sentences).strip()
    if whole and len(whole) >= MIN_SENTENCE_LEN:
        chunks.append(whole)

    # De-duplicate while preserving order
    seen = set()
    unique_chunks = []
    for chunk in chunks:
        normalized = preprocess_text(chunk)
        if normalized not in seen:
            seen.add(normalized)
            unique_chunks.append(chunk)

    return unique_chunks[:MAX_CHUNKS_TO_CHECK]


def check_web_plagiarism(text):
    chunks = build_chunks(text)
    matches = []

    for chunk in chunks:
        results = search_google(chunk, num_results=8)
        if not results:
            continue

        best_match = None
        best_score = 0.0

        for result in results:
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            link = result.get("link", "")

            title_score = similarity(chunk, title)
            snippet_score = similarity(chunk, snippet)
            score = max(title_score, snippet_score)

            # Extra signal for near-exact copied text
            chunk_norm = preprocess_text(chunk)
            title_norm = preprocess_text(title)
            snippet_norm = preprocess_text(snippet)

            if chunk_norm and (
                chunk_norm in title_norm
                or chunk_norm in snippet_norm
                or title_norm in chunk_norm
                or snippet_norm in chunk_norm
            ):
                score = max(score, 0.9)

            if score > best_score:
                best_score = score
                best_match = {
                    "link": link,
                    "title": title,
                    "snippet": snippet,
                    "sentence": chunk,
                    "score": round(score, 2),
                }

        threshold = SHORT_TEXT_THRESHOLD if len(chunk.split()) < 12 else MATCH_THRESHOLD

        if best_match and best_score >= threshold:
            matches.append(best_match)

    if matches:
        best = max(matches, key=lambda item: item["score"])
        return "YES", best["link"], best

    return "NO", None, None


def detect_ai_text(text):
    words = text.split()

    if not words:
        return 0.0

    avg_len = sum(len(word) for word in words) / len(words)
    return 0.7 if avg_len > 5 else 0.3


def analyze_file(path):
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    clean_text = preprocess_text(text)
    web_status, web_source, evidence = check_web_plagiarism(text)
    ai_score = detect_ai_text(clean_text)

    plagiarism_detected = web_status == "YES"
    ai_generated_percentage = round(ai_score * 100, 2)
    human_written_percentage = round((1 - ai_score) * 100, 2)

    plagiarism_confidence = 90 if plagiarism_detected else 30
    if evidence and "score" in evidence:
        plagiarism_confidence = max(plagiarism_confidence, int(evidence["score"] * 100))

    return {
        "plagiarism": web_status,
        "plagiarism_detected": plagiarism_detected,
        "plagiarism_label": "Detected" if plagiarism_detected else "Not detected",
        "source": web_source,
        "matched_title": evidence["title"] if evidence else None,
        "matched_snippet": evidence["snippet"] if evidence else None,
        "matched_sentence": evidence["sentence"] if evidence else None,
        "match_score": evidence["score"] if evidence else None,
        "plagiarism_explanation": (
            f"A close web match was found: {evidence['title']}"
            if plagiarism_detected and evidence
            else "No strong web match was found for the uploaded text."
        ),
        "ai_generated_percentage": ai_generated_percentage,
        "human_written_percentage": human_written_percentage,
        "ai_generated_label": "Likely AI-generated" if ai_generated_percentage >= 50 else "Likely human-written",
        "ai_explanation": (
            "The text pattern looks more similar to AI-generated writing."
            if ai_generated_percentage >= 50
            else "The text pattern looks more similar to human writing."
        ),
        "confidence": {
            "plagiarism": plagiarism_confidence,
            "ai_generated": ai_generated_percentage,
        },
    }
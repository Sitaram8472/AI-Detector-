import os

from serpapi import GoogleSearch

API_KEY = os.getenv("SERPAPI_API_KEY")

def search_google(query):
    if not API_KEY:
        return None

    params = {
        "q": query,
        "api_key": API_KEY,
        "num": 1
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception:
        # Network/DNS/API errors should not crash plagiarism endpoint.
        return None

    if "organic_results" in results:
        return results["organic_results"][0]

    return None
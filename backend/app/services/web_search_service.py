import os
import logging

from serpapi import GoogleSearch

logger = logging.getLogger(__name__)
API_KEY = os.getenv("SERPAPI_KEY")


def search_google(query, num_results=5):
    if not API_KEY:
        logger.warning("SERPAPI_KEY not set")
        return []

    if not query or not query.strip():
        return []

    params = {
        "q": query.strip()[:220],
        "api_key": API_KEY,
        "num": num_results,
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception as e:
        logger.exception("SerpAPI request failed: %s", e)
        return []

    return results.get("organic_results", []) or []
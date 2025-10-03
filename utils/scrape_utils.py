"""
This module provides utilities for scraping web content and caching responses.
"""
import cloudscraper
from utils import cache_manager


def fetch_url(url, session=None):
    """Fetch the content of a URL and cache the response."""
    if not session:
        # Create a new session if none is provided
        session = cloudscraper.create_scraper()

    # Perform the GET request with no timeout specified
    r = session.get(url, timeout=None)

    # Check if the response status is not OK (e.g., 404, 500)
    if not r.ok:
        return None

    # Extract the response text
    response = r.text

    # Cache the response for future use
    cache_manager.cache_response(url, response)

    return response

"""
This module provides functionality to scrape and parse entries from MarioCube indexes.
It includes methods to fetch HTML responses, extract relevant data using regex, and format
the data into structured entries.
"""
import re
import html
import sys
from utils import cache_manager
from utils.scrape_utils import fetch_url
from utils.parse_utils import size_bytes_to_str, size_str_to_bytes, join_urls

HOST_NAME = 'MarioCube'


def extract_entries(response, source, platform, base_url):
    """Extract entries from the HTML response using regex."""
    entries = []
    # Regex pattern to extract link, title, and size (bytes) from table rows
    pattern = (
        r"<tr><td>-</td><td><a href=\"(.*?)\">(.*?)</a></td><td>(.*?)</td><td></td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td></tr>"
    )
    matches = re.findall(pattern, response, re.DOTALL)

    for link, title, size_bytes_str in matches:
        # Apply the filter from the source configuration
        match = re.match(source['filter'], title)
        if not match:
            continue

        filename = title  # Original filename
        title = match.group(1)  # Extract the filtered title

        # Create an entry and add it to the list
        entries.append(create_entry(
            link, filename, title, size_bytes_str, source, platform, base_url))

    return entries


def create_entry(link, filename, title, size_bytes_str, source, platform, base_url):
    """Create a dictionary representing a single entry."""
    name = html.unescape(title)
    size = int(size_bytes_str)
    size_str = size_bytes_to_str(size)
    url = join_urls(base_url, link)

    return {
        'title': name,
        'platform': platform,
        'regions': source['regions'],
        'links': [
            {
                'name': name,
                'type': source['type'],
                'format': source['format'],
                'url': url,
                'filename': filename,
                'host': HOST_NAME,
                'size': size,
                'size_str': size_str,
                'source_url': base_url
            }
        ]
    }


def fetch_response(url, use_cached):
    """Fetch the response from a URL, optionally using a cached version."""
    if use_cached:
        # Attempt to retrieve the response from the cache
        response = cache_manager.get_cached_response(url)
        if response:
            return response

    # Fetch the URL directly if no cached response is available
    return fetch_url(url)


def scrape(source, platform, use_cached=False):
    """Scrape entries from MarioCube based on the source configuration."""
    entries = []

    for url in source['urls']:
        # Fetch the response for each URL
        response = fetch_response(url, use_cached)
        if not response:
            print(f"Failed to get response from {url}")
            sys.exit(1)

        # Extract entries from the response
        parsed_entries = extract_entries(response, source, platform, url)
        if not parsed_entries:
            print(f"Failed to parse entries from {url}")
            sys.exit(1)

        entries.extend(parsed_entries)

    return entries

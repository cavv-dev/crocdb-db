"""
This module provides utility functions for caching HTTP responses to a local directory.
It includes functionality to sanitize URLs into valid filenames, save responses to cache,
and retrieve cached responses.
"""
import os
import re

# Directory name where cached responses will be stored
CACHE_DIRNAME = 'cache'

# Ensure the cache directory exists
if not os.path.exists(CACHE_DIRNAME):
    os.mkdir(CACHE_DIRNAME)


def get_cached_response_filename(url):
    """Generate a safe filename for caching a response based on the given URL."""
    # Replace invalid filename characters with underscores
    return re.sub(r"[\\/:\*\?\"<>|]", '_', url)


def cache_response(url, response):
    """Cache the response content for a given URL by saving the response to a file in the cache directory using a sanitized filename."""
    # Generate a sanitized filename for the URL
    filename = get_cached_response_filename(url)

    # Write the response to the cache file
    with open(f'{CACHE_DIRNAME}/{filename}', 'w', encoding='utf-8') as f:
        f.write(response)


def get_cached_response(url):
    """Retrieve the cached response for a given URL by reading the cached response from the file if it exists."""
    # Generate a sanitized filename for the URL
    filename = get_cached_response_filename(url)

    # Check if the cache file exists
    if not os.path.exists(f'{CACHE_DIRNAME}/{filename}'):
        return None

    # Read and return the cached response
    with open(f'{CACHE_DIRNAME}/{filename}', encoding='utf-8') as f:
        return f.read()

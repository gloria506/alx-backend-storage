#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps


r = redis.Redis()


def url_access_count(method):
    """Decorator for caching and tracking URL access."""
    @wraps(method)
    def wrapper(url):
        """Wrapper function to cache and track access."""
        key = "cached:" + url
        cached_value = r.get(key)

        if cached_value:
            return cached_value.decode()  # More flexible decoding

        key_count = "count:" + url
        try:
            html_content = method(url)  # Fetch the HTML content
        except requests.RequestException as e:
            return f"Error fetching page: {e}"

        r.incr(key_count)  # Increment access count
        r.set(key, html_content, ex=10)  # Cache the content for 10 seconds
        return html_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL."""
    response = requests.get(url, timeout=10)  # Adding a timeout
    response.raise_for_status()  # Raise an error for bad responses (4XX/5XX)
    return response.text


if __name__ == "__main__":
    print(get_page('http://slowwly.robertomurray.co.uk'))  # Example usage


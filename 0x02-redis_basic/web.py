#!/usr/bin/env python3
"""
Web Cache and Tracker
"""

import requests
import redis
import time

class WebCache:
    """
    Class to fetch, cache, and track web pages.
    """

    def __init__(self):
        """
        Initializes the WebCache instance.
        """
        self._redis = redis.Redis()

    def cached_page(self, url: str) -> str:
        """
        Fetches the content of a web page, caches it, and tracks its access count.

        Args:
            url (str): The URL of the web page to fetch.

        Returns:
            str: The content of the web page.
        """
        cached_content = self._redis.get(url)
        if cached_content:
            return cached_content.decode('utf-8')

        response = requests.get(url)
        content = response.text

        self._redis.setex(url, 10, content)
        self._redis.incr(f"count:{url}")

        return content

    def get_page(self, url: str) -> str:
        """
        Fetches the content of a web page, using caching and tracking.

        Args:
            url (str): The URL of the web page to fetch.

        Returns:
            str: The content of the web page.
        """
        return self.cached_page(url)

if __name__ == "__main__":
    web_cache = WebCache()
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
    content = web_cache.get_page(url)
    print(content)

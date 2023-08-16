#!/usr/bin/env python3
""" Web cache example using Redis"""
import redis
import requests
import time

class WebCache:
    """ Web cache class"""
    def __init__(self):
        """ Init method"""
        self._redis = redis.Redis()

    def get_page(self, url: str) -> str:
        """ Get page method"""
        # Check if the cached content exists
        cached_content = self._redis.get(url)
        if cached_content:
            return cached_content.decode('utf-8')

        # Fetch the page content
        response = requests.get(url)
        content = response.text

        # Store the content with an expiration time of 10 seconds
        self._redis.setex(url, 10, content)

        # Track the access count
        access_count_key = f"count:{url}"
        self._redis.incr(access_count_key)

        return content

if __name__ == "__main__":
    web_cache = WebCache()

    urls = ["http://slowwly.robertomurray.co.uk/\
            delay/5000/url/https://www.example.com"]  # Example slow URL
    for url in urls:
        content = web_cache.get_page(url)
        print(content)

        access_count_key = f"count:{url}"
        access_count = web_cache._redis.get(access_count_key).decode('utf-8')
        print(f"Access count for {url}: {access_count}")


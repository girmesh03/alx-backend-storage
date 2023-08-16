#!/usr/bin/env python3
"""
Web Cache and Tracker
"""

import requests
import redis
import time
from typing import Callable

def get_page(url: str) -> str:
    response = requests.get(url)
    content = response.text
    return content

class WebCacheTracker:
    def __init__(self):
        self.redis_client = redis.Redis()

    def track_access_count(self, url: str):
        access_key = f"count:{url}"
        self.redis_client.incr(access_key)

    def cache_result(self, url: str, content: str):
        cache_key = f"cache:{url}"
        self.redis_client.setex(cache_key, 10, content)

    def get_cached_page(self, url: str) -> str:
        cache_key = f"cache:{url}"
        cached_content = self.redis_client.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')
        return None

def cached_web_request(fn: Callable):
    cache_tracker = WebCacheTracker()

    def wrapper(url: str):
        cached_content = cache_tracker.get_cached_page(url)
        if cached_content:
            return cached_content

        content = fn(url)
        cache_tracker.cache_result(url, content)
        return content

    return wrapper

@cached_web_request
def get_page(url: str) -> str:
    response = requests.get(url)
    content = response.text
    cache_tracker = WebCacheTracker()
    cache_tracker.track_access_count(url)
    return content

if __name__ == "__main__":
    slow_url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.google.com"

    for _ in range(5):
        page_content = get_page(slow_url)
        print(page_content)
        time.sleep(2)

#!/usr/bin/env python3
"""
Web Cache and Tracker
"""

import requests
import redis
import time

redis_client = redis.Redis()


def get_page(url: str) -> str:
    """Get a web page"""
    # Create a key for tracking URL access count
    count_key = f"count:{url}"

    # Get the current count or initialize it if it doesn't exist
    access_count = redis_client.get(count_key)
    if access_count is None:
        access_count = 1
    else:
        access_count = int(access_count) + 1

    # Store the updated count in Redis
    redis_client.set(count_key, access_count)

    # Check if the page content is cached
    cached_content = redis_client.get(url)
    if cached_content is not None:
        return cached_content.decode('utf-8')

    # If not cached, fetch the page content using requests
    response = requests.get(url)
    page_content = response.text

    # Cache the page content with an expiration time of 10 seconds
    redis_client.setex(url, 10, page_content)

    return page_content


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"

    for _ in range(3):
        content = get_page(url)
        # print(content)
        time.sleep(10)

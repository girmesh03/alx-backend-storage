#!/usr/bin/env python3
"""
Main file
"""

import functools
from typing import Callable
import redis
import uuid

class Cache:
    """
    Cache class for storing and retrieving data with Redis.
    """

    def __init__(self):
        """
        Initializes the Cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: bytes) -> str:
        """
        Store data in Redis.

        Args:
            data (bytes): The data to store.

        Returns:
            str: The generated key for the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str) -> bytes:
        """
        Retrieve data from Redis.

        Args:
            key (str): The key associated with the data.

        Returns:
            bytes: The retrieved data.
        """
        return self._redis.get(key)

def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to decorate.

    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper

if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"first",
        b"second",
        b"third"
    }

    cache.store = count_calls(cache.store)  # Applying the decorator here

    for data in TEST_CASES:
        cache.store(data)
        print(cache.get(cache.store.__qualname__))

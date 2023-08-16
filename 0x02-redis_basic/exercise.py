#!/usr/bin/env python3
"""
Cache Class
"""

import redis
import uuid
from typing import Callable, Union

class Cache:
    """
    Cache class for storing and retrieving data with Redis.
    """

    def __init__(self):
        """
        Initializes the Cache instance.
        """
        self._redis = redis.Redis()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis.

        Args:
            data (Union[str, bytes, int, float]):
            The data to store.

        Returns:
            str: The generated key for the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> \
        Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally convert
        using the provided function.

        Args:
            key (str): The key associated with the data.
            fn (Callable, optional): A callable function
            for data conversion.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data.
        """
        data = self._redis.get(key)
        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve a UTF-8 string data from Redis.

        Args:
            key (str): The key associated with the data.

        Returns:
            Union[str, None]: The retrieved string data.
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve an integer data from Redis.

        Args:
            key (str): The key associated with the data.

        Returns:
            Union[int, None]: The retrieved integer data.
        """
        return self.get(key, fn=int)

if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value

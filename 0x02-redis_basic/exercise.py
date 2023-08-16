#!/usr/bin/env python3
""" Module for implementing a Cache class with redis"""


import redis
from typing import Union, Callable, Optional
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper for decorator functionality """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to record the call history"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''' Wrapper for decorator functionality '''
        input = str(args)
        self._redis.rpush(method.__qualname__ + ':inputs', input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ':outputs', output)
        return output

    return wrapper


def replay(fn: Callable):
    """Replay the call history"""
    radis = redis.Redis()
    function_name = fn.__qualname__
    number_of_calls = radis.get(function_name)
    try:
        number_of_calls = number_of_calls.decode('utf-8')
    except Exception:
        number_of_calls = 0
    print(f'{function_name} was called {number_of_calls} times:')

    ins = radis.lrange(function_name + ':inputs', 0, -1)
    outs = radis.lrange(function_name + ':outputs', 0, -1)

    for i, o in zip(ins, outs):
        try:
            i = i.decode('utf-8')
        except Exception:
            i = ''
        try:
            o = o.decode('utf-8')
        except Exception:
            o = ''

        print(f'{function_name}(*{i}) -> {o}')


class Cache:
    """ Cache class for storing and retrieving data with Redis """
    def __init__(self):
        """ Initialize the Cache instance """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store data in Redis """
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ Retrieve data from Redis and optionally
        convert using the provided function """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """ Retrieve a UTF-8 string data from Redis """
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value

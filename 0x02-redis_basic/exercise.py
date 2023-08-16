#!/usr/bin/env python3
'''
Project on Redis basics
'''


import redis
from typing import Union, Callable, Optional
from uuid import uuid4, UUID
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''
    Decorator for counting how many times a function has been called
    '''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''' Wrapper for decorator functionality '''
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    '''
    Decorator to store the history of inputs and outputs for
    a particular function
    '''
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
    ''' Display the history calls of a particular function'''
    r = redis.Redis()
    f_name = fn.__qualname__
    n_calls = r.get(f_name)
    try:
        n_calls = n_calls.decode('utf-8')
    except Exception:
        n_calls = 0
    print(f'{f_name} was called {n_calls} times:')

    ins = r.lrange(f_name + ':inputs', 0, -1)
    outs = r.lrange(f_name + ':outputs', 0, -1)

    for i, o in zip(ins, outs):
        try:
            i = i.decode('utf-8')
        except Exception:
            i = ''
        try:
            o = o.decode('utf-8')
        except Exception:
            o = ''

        print(f'{f_name}(*{i}) -> {o}')


class Cache:
    ''' Class for implementing a Cache with redis '''

    def __init__(self):
        ''' Constructor '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        store the input data in Redis using a random key
        and return the key
        '''
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        ''' Reading from Redis and recovering original type '''
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        '''Paramaterizes a value from redis to str '''
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value

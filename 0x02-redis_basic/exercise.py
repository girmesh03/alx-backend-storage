#!/usr/bin/env python3
'''
Redis Cache Implementation Project
'''

import redis
from typing import Union, Callable, Optional
from uuid import uuid4, UUID
from functools import wraps

def track_calls(method: Callable) -> Callable:
    '''
    Decorator to count the number of times a function is called
    '''
    call_count_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''' Wrapper function for tracking calls '''
        self._redis.incr(call_count_key)
        return method(self, *args, **kwargs)

    return wrapper

def track_history(method: Callable) -> Callable:
    '''
    Decorator to store the history of inputs and outputs of a function
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        ''' Wrapper function for tracking history '''
        input_args = str(args)
        self._redis.rpush(method.__qualname__ + ':inputs', input_args)
        output_result = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ':outputs', output_result)
        return output_result

    return wrapper

def show_call_history(fn: Callable):
    ''' Display the call history of a specific function '''
    redis_conn = redis.Redis()
    func_name = fn.__qualname__
    num_calls = redis_conn.get(func_name)
    try:
        num_calls = num_calls.decode('utf-8')
    except Exception:
        num_calls = 0
    print(f'{func_name} has been called {num_calls} times:')

    inputs = redis_conn.lrange(func_name + ':inputs', 0, -1)
    outputs = redis_conn.lrange(func_name + ':outputs', 0, -1)

    for in_args, out_result in zip(inputs, outputs):
        try:
            in_args = in_args.decode('utf-8')
        except Exception:
            in_args = ''
        try:
            out_result = out_result.decode('utf-8')
        except Exception:
            out_result = ''

        print(f'{func_name}(*{in_args}) -> {out_result}')

class RedisCache:
    ''' Class for implementing a Redis Cache '''

    def __init__(self):
        ''' Constructor '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @track_history
    @track_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Store the input data in Redis using a random key
        and return the key
        '''
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def retrieve(self, key: str,
                 converter: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        ''' Retrieve data from Redis and apply conversion if provided '''
        value = self._redis.get(key)
        if converter:
            value = converter(value)
        return value

    def retrieve_string(self, key: str) -> str:
        ''' Retrieve and convert value from Redis to a string '''
        value = self._redis.get(key)
        return value.decode('utf-8')

    def retrieve_int(self, key: str) -> int:
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value

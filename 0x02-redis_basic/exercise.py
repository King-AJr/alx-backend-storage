#!/usr/bin/env python3
"""
creating a simple redis cache
"""
import redis
import uuid
from typing import Union, Callable
import functools


def count_calls(fn: Callable) -> Callable:
    """returns a Callable"""
    qual_name = fn.__qualname__

    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        """wrapper to carry out increment"""
        self._redis.incr(qual_name)
        return fn(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    a class for a simple
    redis cache
    """

    def __init__(self):
        """
        Initialize a Redis client and flush the Redis database.

        This constructor method creates an instance of a Redis
        client using the `redis.Redis()` constructor and also
        defines a `flush` attribute, which is a reference to the
        `flushdb` method of the Redis client instance. This allows
        you to easily flush the Redis database when needed.

        Parameters:
            None

        Returns:
            None
        """
        self._redis = redis.Redis()
        self.flush = self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Receives a string data and stores it in the Redis cache.

        Args:
            self: An instance of the class containing this method.
            data (str): The string data to be stored in the Redis cache.

        Returns:
            str: The unique key used to store the data in the Redis cache.
        """
        key = str(uuid.uuid4())  # Generate a unique key
        self._redis.set(key, data)  # Store the data in the Redis cache
        return key  # Return the unique key used for storage

    def get(self, key: str, fn: Callable = None) -> Union[str, int, None]:
        """
        Retrieve data from Redis using the specified 'key'.

        Args:
            key (str): The key to retrieve data from Redis.
            fn (Callable, optional): A callable function used to convert
            the data. Defaults to None.

        Returns:
            Any: The retrieved data, optionally converted by 'fn'. Returns
            None if the key does not exist.
        """
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            data = fn(data)

        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve data from Redis as a string.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            str: The retrieved data as a string, or None if the
            key does not exist.
        """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """
        Retrieve data from Redis as an integer.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            int: The retrieved data as an integer, or None if the
            key does not exist.
        """
        return self.get(key, int)

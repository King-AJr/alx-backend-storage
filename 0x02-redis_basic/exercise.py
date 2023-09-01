#!/usr/bin/env python3
"""
creating a simple redis cache
"""
import redis
import uuid
from typing import Union


class Cache():
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

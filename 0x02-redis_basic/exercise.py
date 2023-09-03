#!/usr/bin/env python3
"""
creating a simple redis cache
"""
import redis
import uuid
from typing import Union, Callable
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: A decorated version of the method.
    """
    # Get the qualified name of the method for use as a key
    qual_name = method.__qualname__

    # Define a wrapper function to carry out the increment and call the original method
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to carry out the call counting and delegate to the original method.

        Args:
            self: The instance of the class the method belongs to.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            Any: The result of calling the original method.
        """
        # Increment the count associated with the method's qualified name
        self._redis.incr(qual_name)

        # Call the original method with its arguments and keyword arguments
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    # Create keys for storing input and output data in Redis
    # The keys are based on the qualified name of the decorated method
    inputs = "{}:inputs".format(method.__qualname__)
    outputs = "{}:outputs".format(method.__qualname__)

    # Define the wrapper function that will replace the original method
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Push the method's input arguments as a string into the Redis list
        self._redis.rpush(inputs, str(*args))

        # Call the original method and capture its result
        result = method(self, *args, **kwargs)

        # Push the result of the method into the Redis list for outputs
        self._redis.rpush(outputs, result)

        # Return the result obtained from calling the original method
        return result

    # Return the wrapper function, effectively replacing the original method
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
    @call_history
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

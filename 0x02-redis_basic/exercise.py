#!/usr/bin/env python3
"""
creating a simple redis cache
"""
import redis
import uuid
from typing import Any


class Cache():
    """
    a class for a simple
    redis cache
    """
    def __init__(self):
        """
        instantiate a redis client as
        a redis variable and flush the
        instance using flushdb.
        """
        self._redis = redis.Redis()
        self.flush = self._redis.flushdb()

    def store(self, data: Any) -> str:
        """
        recieves a data and stores
        it in the redis cache
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

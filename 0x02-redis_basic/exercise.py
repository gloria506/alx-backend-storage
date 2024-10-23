#!/usr/bin/env python3
"""
This module defines a Cache class that interacts with Redis to store and retrieve data
while tracking method calls and input/output history.
"""

import redis
import uuid
from typing import Callable, Optional, Any

class Cache:
    """
    This class provides a simple interface to store and retrieve values from a Redis database.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache class, creating a Redis client instance and flushing the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Any) -> str:
        """
        Store a value in Redis with a random key.

        Args:
            data (str, bytes, int, float): The data to be stored.

        Returns:
            str: The generated key for the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Retrieve a value from Redis using the given key and optionally convert it using fn.

        Args:
            key (str): The key to look up in Redis.
            fn (Optional[Callable]): A function to convert the retrieved value.

        Returns:
            Any: The retrieved value, converted using fn if provided.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieve a string value from Redis.

        Args:
            key (str): The key to look up in Redis.

        Returns:
            str: The retrieved value converted to string.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer value from Redis.

        Args:
            key (str): The key to look up in Redis.

        Returns:
            int: The retrieved value converted to integer.
        """
        return self.get(key, lambda d: int(d))

    def count_calls(method: Callable) -> Callable:
        """
        Decorator to count the number of times a method is called.

        Args:
            method (Callable): The method to be decorated.

        Returns:
            Callable: The decorated method that increments the call count in Redis.
        """
        def wrapper(self, *args, **kwargs) -> Any:
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)

        return wrapper

    @count_calls
    def store(self, data: Any) -> str:
        """
        Store a value in Redis with a random key, decorated to count calls.

        Args:
            data (str, bytes, int, float): The data to be stored.

        Returns:
            str: The generated key for the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


#!/usr/bin/env python3
"""
Implements an expiring web cache and tracker
"""
from typing import Callable
from functools import wraps
import redis
import requests
redis_client = redis.Redis()


def url_count(method: Callable) -> Callable:
    """counts how many times an url is accessed"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        url = args[0]
        redis_client.incr(f"count:{url}")
        cached = redis_client.get(f'{url}')
        if cached:
            return cached.decode('utf-8')
        redis_client.setex(f'{url}, 10, {method(url)}')
        return method(*args, **kwargs)
    return wrapper


@url_count
def get_page(url: str) -> str:
    """get a page and cache value"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')

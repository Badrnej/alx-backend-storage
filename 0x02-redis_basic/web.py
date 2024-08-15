#!/usr/bin/python3
import redis
import requests
from functools import wraps

# Create a Redis client
r = redis.Redis()

def cache_page(func):
    @wraps(func)
    def wrapper(url):
        cache_key = f"count:{url}"
        content_key = f"content:{url}"

        # Increment the access count
        r.incr(cache_key)

        # Check if the content is already cached
        cached_content = r.get(content_key)
        if cached_content:
            return cached_content.decode('utf-8')

        # Fetch the content from the URL
        content = func(url)

        # Cache the content with an expiration time of 10 seconds
        r.setex(content_key, 10, content)

        return content
    return wrapper

@cache_page
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Example usage
    url = "http://slowwly.robertomurray.co.uk/delay/3000/url/http://www.example.com"
    print(get_page(url))


#!/usr/bin/env python3
import redis
import requests
import functools

redis_client = redis.Redis()


def url_access_count(method):
    """
    decorator function for caching and counting URL accesses
    """
    @functools.wraps(method)
    def wrapper(url):
        # Create keys for caching and counting
        cache_key = "cached:" + url
        count_key = "count:" + url

        # Try to retrieve cached content from Redis
        cached_content = redis_client.get(cache_key)

        if cached_content:
            # Return cached content as a UTF-8 decoded string
            return cached_content.decode("utf-8")

        # If not cached, fetch new content
        html_content = method(url)

        # Update the count in Redis
        redis_client.incr(count_key)

        # Set the cached content with an expiration of 10 seconds
        redis_client.setex(cache_key, 10, html_content)

        return html_content

    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL"""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    # Example usage of the decorated get_page function
    content = get_page('http://slowwly.robertomurray.co.uk')
    print(content)

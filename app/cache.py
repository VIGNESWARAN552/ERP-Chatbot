import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

def cache_query(key, value):
    cache.set(key, value, ex=3600)  # Cache for 1 hour

def get_cached_query(key):
    return cache.get(key)

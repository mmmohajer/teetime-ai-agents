import os

REDIS_USER_PASS = os.environ.get('REDIS_USER_PASS', 'RedisUserPass')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://:{REDIS_USER_PASS}@redis-cache:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
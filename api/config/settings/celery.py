from celery.schedules import crontab
import os

DEBUG = bool(int(os.environ.get("DEBUG", 1)))

REDIS_USER_PASS = os.environ.get('REDIS_USER_PASS', 'RedisUserPass')

CELERY_BROKER_URL = f"redis://:{REDIS_USER_PASS}@redis:6379/1"

CELERY_TIMEZONE = os.environ.get('API_TIME_ZONE', 'America/Toronto')

CELERY_BEAT_SCHEDULE = {}
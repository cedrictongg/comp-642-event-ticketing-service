import json

from app.config import settings
from app.database import redis_client


CACHE_KEY_PREFIX = "event:summary"


def get_event_cache_key(event_id):
    return f"{CACHE_KEY_PREFIX}:{event_id}"


def get_cached_event(event_id):
    cached_value = redis_client.get(
        get_event_cache_key(event_id)
    )

    if cached_value is None:
        return None

    return json.loads(cached_value)


def cache_event(event_id, event_data):
    redis_client.set(
        get_event_cache_key(event_id),
        # need to convert unsupported values to strings
        json.dumps(event_data, default=str),
        ex=settings.event_cache_ttl_seconds
    )


def invalidate_event_cache(event_id):
    redis_client.delete(
        get_event_cache_key(event_id)
    )


def get_event_cache_ttl(event_id):
    return redis_client.ttl(
        get_event_cache_key(event_id)
    )
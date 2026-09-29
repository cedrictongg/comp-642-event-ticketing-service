from app.database import redis_client
from app.services.cache_service import (
    cache_event,
    get_cached_event,
    get_event_cache_key,
    get_event_cache_ttl,
    invalidate_event_cache
)
from app.services.trending_service import (
    TRENDING_EVENTS_KEY,
    get_top_trending_events,
    increment_event_view
)


def test_event_cache_key():
    assert get_event_cache_key(1) == "event:summary:1"


def test_cache_event_and_retrieve():
    event_id = 9001

    event_data = {
        "eventId": event_id,
        "title": "Redis Cache Test Event",
        "eventType": "TEST"
    }

    try:
        cache_event(event_id, event_data)

        cached_event = get_cached_event(event_id)
        ttl_seconds = get_event_cache_ttl(event_id)

        assert cached_event == event_data
        assert 0 < ttl_seconds <= 120

    finally:
        invalidate_event_cache(event_id)


def test_invalidate_event_cache():
    event_id = 9002

    try:
        cache_event(
            event_id,
            {
                "eventId": event_id,
                "title": "Cache Invalidation Test",
                "eventType": "TEST"
            }
        )

        assert get_cached_event(event_id) is not None

        invalidate_event_cache(event_id)

        assert get_cached_event(event_id) is None

    finally:
        invalidate_event_cache(event_id)


def test_trending_events_ranked_by_score():
    redis_client.delete(TRENDING_EVENTS_KEY)

    try:
        increment_event_view(9001)
        increment_event_view(9001)
        increment_event_view(9002)

        trending_events = get_top_trending_events()

        assert trending_events[0] == {
            "eventId": 9001,
            "score": 2
        }

        assert trending_events[1] == {
            "eventId": 9002,
            "score": 1
        }

    finally:
        redis_client.delete(TRENDING_EVENTS_KEY)
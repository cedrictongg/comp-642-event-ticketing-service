from app.database import redis_client


TRENDING_EVENTS_KEY = "trending:events"


def increment_event_view(event_id):
    # https://redis.io/docs/latest/commands/zincrby/
    # Increments the score of member in the sorted set stored at key by increment.
    # If member does not exist in the sorted set, it is added with increment as its
    # score (as if its previous score was 0.0). If key does not exist, a new sorted
    # set with the specified member as its sole member is created.
    return redis_client.zincrby(
        TRENDING_EVENTS_KEY,
        1,
        str(event_id)
    )


def get_top_trending_events():
    # https://redis.io/docs/latest/commands/zrevrange/
    ranked_events = redis_client.zrevrange(
        TRENDING_EVENTS_KEY,
        0,
        9,
        withscores=True
    )

    return [
        {
            "eventId": int(event_id),
            "score": int(score)
        }
        for event_id, score in ranked_events
    ]
from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.database import mongo_database, mysql_engine
from app.services.cache_service import cache_event, get_cached_event
from app.services.trending_service import increment_event_view


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("")
def list_events():
    with mysql_engine.connect() as connection:
        events = connection.execute(
            text("""
                SELECT
                    E.EVENT_ID,
                    E.EVENT_TITLE,
                    E.EVENT_DATETIME,
                    V.VENUE_NAME
                FROM EVENTS AS E
                LEFT JOIN VENUES AS V
                    ON E.VENUE_ID = V.VENUE_ID
                ORDER BY E.EVENT_DATETIME
            """)
        ).mappings().all()

    return [
        {
            "eventId": event["EVENT_ID"],
            "title": event["EVENT_TITLE"],
            "datetime": str(event["EVENT_DATETIME"]),
            "venue": event["VENUE_NAME"]
        }
        for event in events
    ]


@router.get("/{event_id}")
def get_event(event_id):
    cached_event = get_cached_event(event_id)

    if cached_event is not None:
        increment_event_view(event_id)

        return {
            "source": "redis",
            "event": cached_event
        }

    with mysql_engine.connect() as connection:
        event = connection.execute(
            text("""
                SELECT
                    E.EVENT_ID,
                    E.EVENT_TITLE,
                    E.EVENT_DATETIME,
                    E.VENUE_ID,
                    V.VENUE_NAME,
                    V.VENUE_CAPACITY
                FROM EVENTS AS E
                LEFT JOIN VENUES AS V
                    ON E.VENUE_ID = V.VENUE_ID
                WHERE E.EVENT_ID = :event_id
            """),
            {"event_id": event_id}
        ).mappings().first()

        ticket_types = connection.execute(
            text("""
                SELECT
                    TTA.TICKET_TYPE
                FROM TICKET_TYPE_ASSIGNMENTS AS TTA
                WHERE TTA.EVENT_ID = :event_id
                ORDER BY TTA.TICKET_TYPE
            """),
            {"event_id": event_id}
        ).mappings().all()

        tickets_sold = connection.execute(
            text("""
                SELECT
                    COUNT(*) AS TICKETS_SOLD
                FROM ORDER_ITEMS
                WHERE EVENT_ID = :event_id
            """),
            {"event_id": event_id}
        ).mappings().first()

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    content = mongo_database.event_content.find_one(
        # cast to int because string was not working
        {"eventId": int(event_id)},
        {"_id": 0}
    )

    ticket_count = tickets_sold["TICKETS_SOLD"]

    event_data = {
        "eventId": event["EVENT_ID"],
        "title": event["EVENT_TITLE"],
        "datetime": str(event["EVENT_DATETIME"]),
        "venue": {
            "venueId": event["VENUE_ID"],
            "name": event["VENUE_NAME"],
            "capacity": event["VENUE_CAPACITY"]
        },
        "ticketTypes": [
            ticket["TICKET_TYPE"]
            for ticket in ticket_types
        ],
        "ticketsSold": ticket_count,
        "inventoryRemaining": event["VENUE_CAPACITY"] - ticket_count,
        "content": content
    }

    cache_event(event_id, event_data)
    increment_event_view(event_id)

    return {
        "source": "database",
        "event": event_data
    }

###j
@router.get("/{event_id}/sales")
def get_sales(event_id):
    event_id = event_id
    return None
from datetime import datetime

from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import text

from app.database import mysql_engine, redis_client
from app.services.cache_service import invalidate_event_cache


router = APIRouter(prefix = "/admin", tags = ["Admin"])


def validate_event(data):
    try:
        title = data["title"].strip()
        venue_id = data["venueId"]
        event_datetime = datetime.strptime(
            data["datetime"], "%Y-%m-%d %H:%M:%S"
        )

        if not 1 <= len(title) <= 100:
            raise ValueError()

        if type(venue_id) is not int or venue_id < 1:
            raise ValueError()

    except (KeyError, TypeError, ValueError, AttributeError):
        raise HTTPException(
            400,
            "Provide title (Up to 100 characters), a positive integer venueId, "
            "and datetime in YYYY-MM-DD HH:MM:SS format"
        )

    return {
        "title": title,
        "datetime": event_datetime,
        "venue_id": venue_id
    }


def check_venue(connection, venue_id):
    venue = connection.execute(
        text("SELECT VENUE_ID FROM VENUES WHERE VENUE_ID = :venue_id"),
        {"venue_id": venue_id}
    ).first()

    if venue is None:
        raise HTTPException(404, "Venue not found")


@router.post("/events", status_code = 201)
def create_event(data = Body(...)):
    values = validate_event(data)

    with mysql_engine.begin() as connection:
        check_venue(connection, values["venue_id"])

        result = connection.execute(
            text("""
                INSERT INTO EVENTS (
                    EVENT_TITLE, EVENT_DATETIME, VENUE_ID
                )
                VALUES (:title, :datetime, :venue_id)
            """),
            values
        )

        event_id = result.lastrowid

    return {"eventId": event_id, "message": "Event created"}


@router.put("/events/{event_id}")
def update_event(event_id, data = Body(...)):
    values = validate_event(data)
    values["event_id"] = event_id

    with mysql_engine.begin() as connection:
        event = connection.execute(
            text("SELECT EVENT_ID FROM EVENTS WHERE EVENT_ID = :event_id"),
            {"event_id": event_id}
        ).first()

        if event is None:
            raise HTTPException(404, "Event not found")

        check_venue(connection, values["venue_id"])

        connection.execute(
            text("""
                UPDATE EVENTS
                SET EVENT_TITLE = :title,
                    EVENT_DATETIME = :datetime,
                    VENUE_ID = :venue_id
                WHERE EVENT_ID = :event_id
            """),
            values
        )

    invalidate_event_cache(event_id)

    return {"eventId": int(event_id), "message": "Event updated"}


@router.get("/events/{event_id}/activity")
def get_event_activity(event_id):
    with mysql_engine.connect() as connection:
        event = connection.execute(
            text("""
                SELECT
                    E.EVENT_ID,
                    E.EVENT_TITLE,
                    COUNT(OI.ITEM_ID) AS TICKETS_SOLD,
                    COALESCE(SUM(OI.TICKET_PRICE), 0) AS ORDER_VALUE
                FROM EVENTS AS E
                LEFT JOIN ORDER_ITEMS AS OI
                    ON E.EVENT_ID = OI.EVENT_ID
                WHERE E.EVENT_ID = :event_id
                GROUP BY E.EVENT_ID, E.EVENT_TITLE
            """),
            {"event_id": event_id}
        ).mappings().first()

    if event is None:
        raise HTTPException(404, "Event not found")

    views = redis_client.zscore("trending:events", str(event["EVENT_ID"]))

    return {
        "eventId": event["EVENT_ID"],
        "title": event["EVENT_TITLE"],
        "ticketsSold": event["TICKETS_SOLD"],
        "orderValue": str(event["ORDER_VALUE"]),
        "views": int(views or 0)
    }


@router.get("/events/{event_id}/sales")
def get_event_sales(event_id):
    with mysql_engine.connect() as connection:
        sales = connection.execute(
            text("""
                SELECT E.EVENT_ID, E.EVENT_TITLE, E.TOTAL_SALES, E.TICKETS_SOLD, V.VENUE_NAME,
                    V.VENUE_CAPACITY, E.TICKETS_SOLD/V.VENUE_CAPACITY AS SELL_THROUGH
                FROM EVENTS E
                JOIN VENUES V
                ON E.VENUE_ID = V.VENUE_ID
                WHERE EVENT_ID = :event_id
            """),
            {"event_id": event_id}
        ).mappings().first()

        if sales is None:
            raise HTTPException(404, "No event found")
        
        return {
            "eventId": sales["EVENT_ID"],
            "title": sales["EVENT_TITLE"],
            "ticketsSold": sales["TICKETS_SOLD"],
            "totalSales": sales["TOTAL_SALES"],
            "venue": sales["VENUE_NAME"],
            "venueCapacity": sales["VENUE_CAPACITY"],
            "sellThrough": sales["SELL_THROUGH"]
        }


@router.post("/events/{event_id}/tickets", status_code = 201)
def assign_ticket_type(event_id: int, ticket_type: str = Body(..., embed = True)):
    with mysql_engine.connect() as conn:
        event = conn.execute(
            text("SELECT EVENT_ID FROM EVENTS WHERE EVENT_ID = :id"),
            {"id": event_id}
        ).fetchone()

        if not event:
            raise HTTPException(status_code = 404, detail = "Event not found")

        try:
            conn.execute(
                text("INSERT INTO TICKET_TYPE_ASSIGNMENTS (EVENT_ID, TICKET_TYPE) VALUES (:id, :type)"),
                {"id": event_id, "type": ticket_type}
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise HTTPException(status_code = 400, detail = "Ticket type already assigned or invalid")

        return {"event_id": event_id, "ticket_type": ticket_type}


@router.get("/events/{event_id}/inventory")
def get_event_inventory(event_id: int):
    with mysql_engine.connect() as conn:
        query = text("""
            SELECT 
                E.EVENT_ID,
                E.EVENT_TITLE,
                V.VENUE_CAPACITY AS total_capacity,
                E.TICKETS_SOLD AS tickets_sold,
                (V.VENUE_CAPACITY - E.TICKETS_SOLD) AS remaining_inventory
            FROM EVENTS E
            JOIN VENUES V ON E.VENUE_ID = V.VENUE_ID
            WHERE E.EVENT_ID = :id
        """)
        
        row = conn.execute(query, {"id": event_id}).mappings().fetchone()
        if not row:
            raise HTTPException(status_code = 404, detail = "Event not found")

        return dict(row)
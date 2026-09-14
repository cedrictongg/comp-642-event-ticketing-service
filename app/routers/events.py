from fastapi import APIRouter

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("")
def list_events():
    return {
        "message": "Event listing endpoint placeholder."
    }


@router.get("/{event_id}")
def get_event(event_id: int):
    return {
        "message": "Cross-database event endpoint placeholder.",
        "eventId": event_id
    }
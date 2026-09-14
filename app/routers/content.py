from fastapi import APIRouter

router = APIRouter(
    prefix="/events",
    tags=["Event Content"]
)


@router.get("/{event_id}/content")
def get_event_content(event_id: int):
    return {
        "message": "MongoDB event-content endpoint placeholder.",
        "eventId": event_id
    }


@router.post("/{event_id}/reviews")
def create_event_review(event_id: int):
    return {
        "message": "MongoDB review endpoint placeholder.",
        "eventId": event_id
    }
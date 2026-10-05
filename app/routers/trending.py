from fastapi import APIRouter

from app.services.trending_service import get_top_trending_events

router = APIRouter(
    prefix="/trending",
    tags=["Trending"]
)


@router.get("")
def get_trending():
    return {
        "events": get_top_trending_events()
    }
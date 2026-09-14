from fastapi import APIRouter

router = APIRouter(
    prefix="/trending",
    tags=["Trending"]
)


@router.get("")
def get_trending_events():
    return {
        "message": "Redis trending-events endpoint placeholder."
    }
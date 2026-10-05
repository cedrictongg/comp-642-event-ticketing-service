from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.database import mongo_database

router = APIRouter(
    prefix="/events",
    tags=["Event Content"]
)

class ReviewCreate(BaseModel):
    user_id: int = Field(alias="userId")
    rating: int = Field(ge=1, le=5)
    comment: str

@router.get("/{event_id}/content")
def get_event_content(event_id: int):
    content = mongo_database.event_content.find_one({"eventId": event_id}, {"_id": 0})
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.post("/{event_id}/reviews", status_code=status.HTTP_201_CREATED)
def create_event_review(event_id: int, review: ReviewCreate):
    review_data = review.model_dump(by_alias=True)
    
    result = mongo_database.event_content.update_one(
        {"eventId": event_id},
        {"$push": {"reviews": review_data}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
        
    return {"message": "Review added", "eventId": event_id, "review": review_data}
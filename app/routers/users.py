from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("")
def create_user():
    return {
        "message": "User creation endpoint placeholder."
    }


@router.get("/{user_id}/orders")
def get_user_orders(user_id: int):
    return {
        "message": "User order-history endpoint placeholder.",
        "userId": user_id
    }
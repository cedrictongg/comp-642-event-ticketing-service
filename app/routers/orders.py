from fastapi import APIRouter

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("")
def create_order():
    return {
        "message": "Order transaction endpoint placeholder."
    }
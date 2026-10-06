from fastapi import APIRouter
from sqlalchemy import text
from datetime import datetime

from app.database import mysql_engine
from app.services.cache_service import cache_event, get_cached_event
from app.services.trending_service import increment_event_view

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

###j
@router.get("")
def get_user_ids():
    with mysql_engine.connect() as connection:
        user_ids = connection.execute(
            text("""
                SELECT * FROM USERS
            """)
        ).mappings().all()

    return [
            {
                "userId": user_id["USER_ID"]
            }
            for user_id in user_ids
        ]

###j
@router.post("/{f_name}/{l_name}")
def create_user(f_name: str, l_name: str):
    acct_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with mysql_engine.connect() as connection:
            connection.execute(
                text("""
                    INSERT INTO USERS (USER_FNAME, USER_LNAME, ACCT_CREATED) VALUES
                    (:f_name, :l_name, :acct_created)
                """),
                {"f_name": f_name, "l_name": l_name, "acct_created": acct_created}
            )
            connection.commit()
            inserted = connection.execute(
                text("""
                    SELECT USER_ID FROM USERS 
                    WHERE 
                        USER_FNAME = :f_name AND
                        USER_LNAME = :l_name
                    ORDER BY ACCT_CREATED DESC
                """),
                {"f_name": f_name, "l_name": l_name}
            ).mappings().first()
            return [
                {
                     "userID" : inserted["USER_ID"],
                    "message" : f'User {f_name} {l_name} successfully added'
                }
            ]

###j
@router.get("/{user_id}/orders")
def get_user_orders(user_id: int):    
    with mysql_engine.connect() as connection:
        orders = connection.execute(
            text("""
                    SELECT * FROM ORDERS
                    WHERE USER_ID = :user_id
            """),
            {"user_id" : user_id}
        ).mappings().all()

    return [
        {
            "orderId" : order['ORDER_ID'],
             "balance" :order['BALANCE'],
             "status" : order['STATUS']
        }
        for order in orders
    ]
from fastapi import APIRouter
from sqlalchemy import text
from pydantic import BaseModel, Field

from decimal import Decimal
from datetime import datetime

from app.database import mysql_engine

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

#Default Json for order purchasing
class TicketOrder(BaseModel):
    userId: int
    balance: Decimal = Field(default = 0)
    status: str = Field(default = "UNPAID")
    orderItems: list
    orderCreated: datetime = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#Retrieve an order
@router.get("/{order_id}")
def get_order(order_id: int):
    with mysql_engine.connect() as connection:
        response = connection.execute(
            text("""
                SELECT * FROM ORDERS WHERE ORDER_ID = :order_id
            """),
            {"order_id" : order_id}
        ).mappings().first()
        return { 
            'userId':response['USER_ID'], 
            'balance':response['BALANCE'], 
            'status': response['STATUS']
        }

#Retrieve items associated with an order
@router.get("/{order_id}/items")
def get_order_items(order_id):
    with mysql_engine.connect() as connection:
            response = connection.execute(
                text("""
                    SELECT * FROM ORDER_ITEMS WHERE ORDER_ID = :order_id
                """),
                {"order_id" : order_id}
            ).mappings().all()
            return [{ 
                'orderId' : order_id,
                'eventId': r['EVENT_ID'], 
                'ticketPrice': r['TICKET_PRICE']
            } for r in response
            ]


###j
#Create order/Purchase Tickets
@router.post("")
def create_order(_order: TicketOrder):
    userId = _order.userId
    balance = _order.balance
    status = _order.status
    orderItems = _order.orderItems
    orderCreated = _order.orderCreated

    with mysql_engine.connect() as connection:
        #Create Order
        connection.execute(
            text("""
                INSERT INTO 
                    ORDERS (USER_ID, BALANCE, STATUS, ORDER_CREATED) VALUES
                        (:userId, :balance, :status, :orderCreated)
            """),
            {"userId":userId, "balance" : balance, "status" : status, "orderCreated" : orderCreated}
        )
        connection.commit()
        #Get Order ID
        orderId = connection.execute(
            text("""
                SELECT ORDER_ID FROM ORDERS
                    WHERE 
                        USER_ID = :userId AND
                        ORDER_CREATED = :orderCreated
                    ORDER BY ORDER_CREATED DESC
            """),
            {"userId" : userId, "orderCreated" : orderCreated}
        ).mappings().first()['ORDER_ID']
        for oi in orderItems:
            eventId = oi['eventId']
            ticketPrice = oi['ticketPrice']
            connection.execute(
                text("""
                    INSERT INTO 
                    ORDER_ITEMS (ORDER_ID, EVENT_ID, TICKET_PRICE) VALUES
                    (:orderId, :eventId, :ticketPrice)
                """),
                {'orderId' : orderId, 'eventId' : eventId, 'ticketPrice' : ticketPrice}
            )
        connection.commit()
        order = connection.execute(
            text("""
                SELECT * FROM ORDERS WHERE ORDER_ID = :orderId
            """),
            {'orderId' : orderId}
        ).mappings().first()
        return {
            'userId' : order["USER_ID"],
            'orderId' : order["ORDER_ID"],
            'balance' : order["BALANCE"],
            'status' : order["STATUS"],
            'orderCreated' : order["ORDER_CREATED"]
        }
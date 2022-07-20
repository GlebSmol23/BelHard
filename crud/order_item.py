from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import Order_item, create_session
from schemas import OrderItemSchema, OrderItemInDBSchema


class CRUDOrderItem:

    @staticmethod
    @create_session
    def add(order_item: OrderItemSchema, session: Session = None) -> OrderItemInDBSchema | None:
        order_item = Order_item(**order_item.dict())
        session.add(order_item)
        try:
            session.commit()
        except IntegrityError:
            return None
        else:
            session.refresh(order_item)
            return OrderItemInDBSchema(**order_item.__dict__)

    @staticmethod
    @create_session
    def get(order_item_id: int, session: Session = None) -> OrderItemInDBSchema | None:
        order_item = session.execute(select(Order_item).where(Order_item.id == order_item_id))
        order_item = order_item.first()
        if order_item:
            return OrderItemInDBSchema(**order_item[0].__dict__)

    @staticmethod
    @create_session
    def get_all(category_id: int = None, session: Session = None) -> list[OrderItemInDBSchema] | None:
        if category_id:
            order_items = session.execute(
                select(Order_item).where(Order_item.category_id == category_id)
            )
        else:
            order_items = session.execute(
                select(Order_item)
            )
        return [OrderItemInDBSchema(**order_item[0].__dict__) for order_item in order_items]

    @staticmethod
    @create_session
    def update(order_item: OrderItemInDBSchema, session: Session = None) -> None:
        session.execute(
            update(Order_item).where(Order_item.id == order_item.id).values(
                **order_item.dict()
            )
        )
        session.commit()

    @staticmethod
    @create_session
    def delete(order_item_id: int, session: Session = None) -> None:
        session.execute(
            delete(Order_item).where(Order_item.id == order_item_id)
        )
        session.commit()

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import Product, create_session
from schemas import ProductSchema, ProductInDBSchema


class CRUDProduct:

    @staticmethod
    @create_session
    def add(product: ProductSchema, session: Session = None) -> ProductInDBSchema | None:
        product = Product(
            **product.dict()
        )
        session.add(product)
        try:
            session.commit()
        except IntegrityError:
            return None
        else:
            session.refresh(product)
            return ProductInDBSchema(**product.__dict__)

    @staticmethod
    @create_session
    def get(product_id: int, session: Session = None) -> ProductInDBSchema | None:
        product = session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = product.first()
        if product:
            return ProductInDBSchema(**product[0].__dict__)

    @staticmethod
    @create_session
    def get_all(category_id: int = None, session: Session = None) -> list[ProductInDBSchema] | None:
        if category_id:
            products = session.execute(
                select(Product).where(Product.category_id == category_id)
            )
        else:
            products = session.execute(
                select(Product)
            )
        return [ProductInDBSchema(**product[0].__dict__) for product in products]

    @staticmethod
    @create_session
    def update(product: ProductInDBSchema, session: Session = None) -> None:
        session.execute(
            update(Product).where(Product.id == product.id).values(
                **product.dict()
            )
        )
        session.commit()

    @staticmethod
    @create_session
    def delete(product_id: int, session: Session = None) -> None:
        session.execute(
            delete(Product).where(Product.id == product_id)
        )
        session.commit()


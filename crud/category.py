from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import Category, create_session, Product
from schemas import CategorySchema, CategoryInDBSchema, ProductInDBSchema


class CRUDCategory:

    @staticmethod
    @create_session
    def add(category: CategorySchema, session: Session = None) -> CategoryInDBSchema | None:
        category = Category(
            **category.dict()
        )
        session.add(category)
        try:
            session.commit()
        except IntegrityError:
            return None
        else:
            session.refresh(category)
            return CategoryInDBSchema(**category.__dict__)

    @staticmethod
    @create_session
    def get(category_id: int, session: Session = None) -> CategoryInDBSchema | None:
        category = session.execute(
            select(Category).where(Category.id == category_id)
        )
        category = category.first()
        if category:
            return CategoryInDBSchema(**category[0].__dict__)

    @staticmethod
    @create_session
    def get_all(parent_id: int = None, session: Session = None) -> list[CategoryInDBSchema]:
        if parent_id:
            categories = session.execute(
                select(Category).order_by(Category.id).where(Category.parent_id == parent_id)
            )
        else:
            categories = session.execute(
                select(Category).order_by(Category.id)
            )
        return [CategoryInDBSchema(**category[0].__dict__) for category in categories]

    @staticmethod
    @create_session
    def delete(category_id: int, session: Session = None) -> None:
        session.execute(
            delete(Category).where(Category.id == category_id)
        )
        session.commit()

    @staticmethod
    @create_session
    def update(
            category: CategoryInDBSchema,
            session: Session = None
    ) -> None:
        session.execute(
            update(Category).where(Category.id == category.id).values(
                **category.__dict__
            )
        )
        session.commit()

    @staticmethod
    @create_session
    def get_products(
            category_id: int = None,
            session: Session = None
    ) -> list[tuple[CategoryInDBSchema, ProductInDBSchema]] | None:
        if category_id:
            response = session.execute(
                select(Category, Product)
                .join(Product, Category.id == Product.category_id)
                .where(Category.id == category_id)
            )
            return [
                (
                    CategoryInDBSchema(**res[0].__dict__),
                    ProductInDBSchema(**res[1].__dict__)
                ) for res in response
            ]
        else:
            response = session.execute(
                select(Category, Product)
                .join(Product, Category.id == Product.category_id)
            )
            return [
                (
                    CategoryInDBSchema(**res[0].__dict__),
                    ProductInDBSchema(**res[1].__dict__)
                ) for res in response
            ]
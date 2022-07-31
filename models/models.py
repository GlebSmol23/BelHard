from datetime import datetime
from sqlalchemy import (Column, Text, SmallInteger, ForeignKey, VARCHAR, TIMESTAMP, DECIMAL, Boolean)
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Category(Base):
    __tablename__: str = "categories"

    id = Column(SmallInteger, primary_key=True)
    parent_id = Column(SmallInteger, ForeignKey("categories.id", ondelete="CASCADE"))
    is_published = Column(Boolean, unique=False, default=True)
    name_en = Column(VARCHAR(20), nullable=False)
    name = Column(VARCHAR(20), nullable=False)


class Product(Base):
    __tablename__: str = "products"

    id = Column(SmallInteger, primary_key=True)
    category_id = Column(SmallInteger, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    price = Column(DECIMAL(8, 2), default=0)
    media = Column(VARCHAR(20), nullable=False)
    total = Column(SmallInteger)
    is_published = Column(Boolean, unique=False, default=True)
    name_en = Column(VARCHAR(20), nullable=False)
    name = Column(VARCHAR(24), nullable=False)


class Order(Base):
    __tablename__: str = "orders"

    id = Column(SmallInteger, primary_key=True)
    bot_user_id = Column(SmallInteger, ForeignKey("bot_users.id", ondelete="CASCADE"), nullable=False)
    date_create = Column(TIMESTAMP, default=datetime.now())
    status_id = Column(SmallInteger, ForeignKey("statuses.id", ondelete="CASCADE"), nullable=False)
    invoice_id = Column(SmallInteger, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)


class OrderItem(Base):
    __tablename__: str = "order_items"

    id = Column(SmallInteger, primary_key=True)
    order_id = Column(SmallInteger, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(SmallInteger, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    total = Column(SmallInteger)


class Status(Base):
    __tablename__: str = "statuses"

    id = Column(SmallInteger, primary_key=True)
    name = Column(VARCHAR(20), nullable=False)


class Invoice(Base):
    __tablename__: str = "invoices"

    id = Column(SmallInteger, primary_key=True)
    bot_user_id = Column(SmallInteger, ForeignKey("bot_users.id", ondelete="CASCADE"), nullable=False)
    date_create = Column(TIMESTAMP, default=datetime.now())
    total = Column(SmallInteger)
    status_id = Column(SmallInteger, ForeignKey("statuses.id", ondelete="CASCADE"), nullable=False)


class BotUser(Base):
    __tablename__: str = "bot_users"

    id = Column(SmallInteger, primary_key=True)
    is_blocked = Column(Boolean, unique=False, default=True)
    balance = Column(SmallInteger)
    language_id = Column(SmallInteger, ForeignKey("languages.id", ondelete="CASCADE"), nullable=False)


class Language(Base):
    __tablename__: str = "languages"

    id = Column(SmallInteger, primary_key=True)
    language_code = Column(VARCHAR(20), nullable=False)


class User(Base):
    __tablename__: str = "users"

    id = Column(SmallInteger, primary_key=True)
    username = Column(VARCHAR(24), unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)

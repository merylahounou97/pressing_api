from enum import Enum
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String

from src.catalog.catalog_enums import ArticleSpecificityEnum
from src.database import Base
from src.order.order_enums import OrderStatusEnum
from src.order.order_schemas import TypeOrderEnum
from src.utils.constants import Constants


class OrderModel(Base):
    __tablename__ = Constants.ORDERS
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime)
    delivery_date = Column(DateTime)
    type_order = Column(Enum(TypeOrderEnum), default=TypeOrderEnum.Normal)
    collect = Column(Boolean)
    delivery = Column(Boolean)
    discount_order = Column(Float)
    customer_id = Column(String, ForeignKey(f"{Constants.USERS}.id"))
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)


class OrderDetailsModel(Base):
    __tablename__ = Constants.ORDER_DETAILS
    order_id = Column(String, ForeignKey(f"{Constants.ORDERS}.id"), primary_key=True)
    article_id = Column(
        String, ForeignKey(f"{Constants.ORDER_DETAILS}.id"), primary_key=True
    )
    specificity = Column(
        Enum(ArticleSpecificityEnum), default=ArticleSpecificityEnum.NONE
    )
    divider_coef = Column(Float)
    multiplier_coef = Column(Float)
    discount_article = Column(Float)
    quantity = Column(Integer)

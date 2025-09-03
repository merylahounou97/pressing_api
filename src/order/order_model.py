from sqlalchemy.types import Enum
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from src.catalog.catalog_enums import ArticleSpecificityEnum
from src.database import Base
from src.order.order_enums import OrderStatusEnum, OrderTypeEnum
from src.utils.constants import Constants


class OrderModel(Base):
    __tablename__ = Constants.ORDERS
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime)
    delivery_date = Column(DateTime)
    collect_date = Column(DateTime)
    type_order = Column(Enum(OrderTypeEnum), default=OrderTypeEnum.NORMAL)
    collect = Column(Boolean)
    delivery = Column(Boolean)
    discount_order = Column(Float)
    customer_id = Column(String, ForeignKey(f"{Constants.USERS}.id"), nullable=False)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    
    customer = relationship("UserModel", back_populates="orders")
    order_details = relationship("OrderDetailsModel", back_populates="order", cascade="all, delete-orphan")
        
    @property
    def num_order(self) -> str:
        return f"{self.id} / {self.customer_id or ''} / {self.order_date.strftime('%d-%b-%y')}"




class OrderDetailsModel(Base):
    __tablename__ = Constants.ORDER_DETAILS
    order_id = Column(Integer, ForeignKey(f"{Constants.ORDERS}.id"), primary_key=True)
    article_id = Column(
        String,
        ForeignKey(f"{Constants.ARTICLES}.id", ondelete="CASCADE"),
        primary_key=True,
    )
    specificity = Column(
        Enum(ArticleSpecificityEnum), default=ArticleSpecificityEnum.NONE
    )
    divider_coef = Column(Float)
    multiplier_coef = Column(Float)
    discount_article = Column(Float)
    quantity = Column(Integer)
    
    order = relationship("OrderModel", back_populates="order_details")
    article = relationship("ArticleModel", back_populates="order_details")
    


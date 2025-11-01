from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, computed_field
from src.catalog.catalog_enums import ArticleCategoryEnum, ArticleFreqEnum, ArticleSpecificityEnum, ArticleStatusEnum
from src.order.order_enums import OrderStatusEnum, OrderTypeEnum
from src.users.users_schemas import UserOutput


class OrderDetailSchema(BaseModel):
    """Shema for order detail input. when creating or editing an order."""
    article_id: str
    quantity: int
    specificity: ArticleSpecificityEnum
    divider_coef: float
    multiplier_coef: float
    discount_article: float

class OrderDetailOutputSchema(OrderDetailSchema):
    """Schema for order detail output, including article info."""
    code: str
    name: str
    details: str
    category: ArticleCategoryEnum
    status: ArticleStatusEnum
    freq: ArticleFreqEnum
    description: str
    price: int
    express_price: int


class OrderSchema(BaseModel):
    order_date: datetime
    customer_id: Optional[str] = Field(default=None, description="The customer id")
    collect: bool
    delivery: bool
    type_order: OrderTypeEnum
    delivery_date: datetime


class OrderCreateInputSchema(OrderSchema):
    """Schema pour créer une commande."""
    order_details: List[OrderDetailSchema]


class OrderCreateOutputSchema(OrderSchema):
    """Schema pour la sortie lors de la création d'une commande."""
    id: int
    status: OrderStatusEnum
    order_details: List[OrderDetailOutputSchema]

    @computed_field
    @property
    def num_order(self) -> str:
        return f"{self.id} / {self.customer_id or ''} / {self.order_date.strftime('%d-%b-%y')}"


class OrderEditInputSchema(BaseModel):
    order_date: Optional[datetime] = None
    customer_id: Optional[str] = Field(default=None, description="The customer id")
    collect: Optional[bool] = None
    delivery: Optional[bool] = None
    type_order: Optional[OrderTypeEnum] = None
    delivery_date: Optional[datetime] = None
    articles_to_delete: Optional[List[str]] = None
    order_details: Optional[List[OrderDetailSchema]] = None
    

class FullOrderSchema(OrderCreateOutputSchema):
    customer: Optional[UserOutput] = Field(default=None, description="The customer name")
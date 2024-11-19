from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, computed_field
from src.catalog.catalog_enums import ArticleSpecificityEnum
from src.order.order_enums import OrderStatusEnum, OrderTypeEnum

class OrderDetailSchema(BaseModel):
    article_id: str
    quantity: int
    specificity: ArticleSpecificityEnum
    divider_coef: float
    multiplier_coef: float
    discount_article: float

class OrderSchema(BaseModel):
    order_date: datetime
    customer_id: Optional[str] = Field(
        default=None, description="The customer id"
    )
    collect: bool
    delivery: bool
    type_order: OrderTypeEnum
    delivery_date: datetime

class OrderCreateInputSchema(OrderSchema):
    order_details: List[OrderDetailSchema]

class OrderCreateOutputSchema(OrderCreateInputSchema):
    id: int
    status: OrderStatusEnum

    @computed_field
    @property
    def num_order(self) -> str:
        return f"{self.id}/{self.customer_id or ''}/{self.order_date}"

class OrderEditInputSchema(BaseModel):
    order_date: Optional[datetime] = None
    customer_id: Optional[str] = Field(
        default=None, description="The customer id"
    )
    collect: Optional[bool] = None
    delivery: Optional[bool] = None
    type_order: Optional[OrderTypeEnum] = None
    delivery_date: Optional[datetime] = None
    order_details: Optional[List[OrderDetailSchema]] = None

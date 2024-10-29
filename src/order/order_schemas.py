from datetime import date, datetime, time, timedelta
from typing import Annotated

from pydantic import BaseModel, computed_field, Field

from src.catalog.catalog_enums import ArticleSpecificityEnum
from src.catalog.catalog_schemas import ArticleOutputSchema
from src.order.order_enums import OrderStatusEnum, OrderTypeEnum
import typing_extensions

class OrderDetailSchema(BaseModel):
    article_id: str
    quantity: int
    specificity: ArticleSpecificityEnum
    divider_coef:float
    multiplier_coef:float
    discount_article:float

class OrderCreateInputSchema(BaseModel):
    order_date: datetime
    customer_id: str | None = Field(
        default=None, json_schema_extra={"description": "The customer id"}
    )
    collect: bool
    delivery: bool
    type_order: OrderTypeEnum
    delivery_date: datetime
    order_details: list[OrderDetailSchema]

class OrderCreateOutputSchema(OrderCreateInputSchema):
    id: int
    status: OrderStatusEnum

    @computed_field
    @property
    def num_order(self) -> str:
        return str(self.id) + "/" + self.customer_id + str(self.order_date)

    """ 
    delivery_date: datetime
    payment_due: float
    customer_name: str
    client_status: str
    subscription: str
    distance: float
    Price: float
    Price_discount: float
    delivery_price: float
    total_before_discount: float
    total_after_discount: float
    total_net: float
    type_order: TypeOrderEnum """

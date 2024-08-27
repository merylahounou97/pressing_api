import datetime

from pydantic import BaseModel, computed_field

from src.catalog.catalog_schemas import ArticleOutputSchema
from src.order.order_enums import OrderStatusEnum, TypeOrderEnum


class OrderCreateInputSchema(BaseModel):
    date: datetime
    customer_id: str
    collect: bool
    delivery: bool
    type_order: TypeOrderEnum
    delivery_date: datetime
    order_details: list[ArticleOutputSchema]



class OrderCreateOutputSchema(OrderCreateInputSchema):
    id: str
    status: OrderStatusEnum
    @computed_field
    @property
    def num_order(self):
        return self.id+"/"+self.customer_id+self.date


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
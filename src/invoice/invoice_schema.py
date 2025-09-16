from datetime import datetime
from typing import List
from pydantic import BaseModel

class InvoiceItemSchema(BaseModel):
    article_name: str
    specificity: str
    quantity: int
    unit_price: float
    total_price: float
    discount: float

class InvoiceSchema(BaseModel):
    invoice_date: datetime
    due_date: datetime
    customer_name: str
    customer_reference: str
    order_id: int
    items: List[InvoiceItemSchema]
    total_amount: float
    discounted_amount: float
    net_amount: float

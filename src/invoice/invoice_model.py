from sqlalchemy import Column, Integer, String, Float, DateTime
from src.database import Base

class InvoiceModel(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_date = Column(DateTime)
    due_date = Column(DateTime)
    customer_name = Column(String)
    customer_reference = Column(String)
    order_id = Column(Integer)
    total_amount = Column(Float)
    discounted_amount = Column(Float)
    net_amount = Column(Float)

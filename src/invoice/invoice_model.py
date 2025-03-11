from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from src.database import Base

class InvoiceItemModel(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    article_name = Column(String)
    specificity = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_price = Column(Float)
    discount = Column(Float)

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

    items = relationship("InvoiceItemModel", backref="invoice", cascade="all, delete-orphan")

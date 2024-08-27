

from sqlalchemy import Column, Float, String
from src.database import Base
from src.utils.constants import Constants


class ArticleModel(Base):
    __tablename__ = Constants.ARTICLES
    id = Column(String, primary_key=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    express_price = Column(Float)
    
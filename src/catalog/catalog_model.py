from sqlalchemy import Column, Enum, Float, Integer, String
from src.catalog.catalog_enums import (
    ArticleCategoryEnum,
    ArticleFreqEnum,
    ArticleStatusEnum,
)
from src.database import Base
from src.utils.constants import Constants


class ArticleModel(Base):
    __tablename__ = Constants.ARTICLES
    id = Column(String, primary_key=True)
    code = Column(String, index=True)
    name = Column(String)
    details = Column(String)
    category = Column(Enum(ArticleCategoryEnum), default=ArticleCategoryEnum.NONE)
    status = Column(Enum(ArticleStatusEnum), default=ArticleStatusEnum.NONE)
    freq = Column(Enum(ArticleFreqEnum), default=ArticleFreqEnum.NONE)
    description = Column(String)
    price = Column(Integer)
    express_price = Column(Integer)

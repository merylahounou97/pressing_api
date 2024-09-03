from sqlalchemy.orm import Session
from fastapi import Depends
import uuid
from src.catalog.catalog_schemas import ArticleCreateInputSchema
from src.dependencies.db import get_db
from src.catalog.catalog_model import ArticleModel

class CatalogService:
    db: Session
    def __init__(self,db: Session = Depends(get_db)):
        self.db = db

    def create(self, article_input: ArticleCreateInputSchema):
        """Create an article

        Args:
            input (ArticleCreateInputSchema): Input data for creating an article

        Returns:
            _type_: [ArticleModel]
        """
        article = ArticleModel(**{**article_input.model_dump(), "id": str(uuid.uuid4())})
        self.db.add(article)
        self.db.commit()
        return article
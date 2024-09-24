from sqlalchemy.orm import Session
from fastapi import Depends
import uuid
from src.catalog.catalog_schemas import ArticleCreateInputSchema, ArticleEditInputSchema
from src.dependencies.db import get_db
from src.catalog.catalog_model import ArticleModel

class CatalogService:
    db: Session
    def __init__(self,db: Session = Depends(get_db)):
        self.db = db

    def create_article(self, article_input: ArticleCreateInputSchema):
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
    
    def edit_article(self, article_id: str, article_input: ArticleEditInputSchema):
        """Edit an article

        Args:
            article_id (str): The id of the article to edit
            article_input (ArticleCreateInputSchema): Input data for editing an article

        Returns:
            _type_: [ArticleModel]
        """
        
        article = self.db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
        article_input_data = article_input.model_dump()
        print(article_input_data)
        if article is not None:
            for key, value in article_input_data.items():
                print(key,value)
                if value is not None : setattr(article, key, value)
            self.db.commit()
            self.db.refresh(article)
        return article
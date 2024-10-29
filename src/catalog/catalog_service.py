from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_
from fastapi import Depends
import uuid
from src.catalog.catalog_schemas import ArticleCreateInputSchema, ArticleEditInputSchema
from src.dependencies.db import get_db
from src.catalog.catalog_model import ArticleModel


class CatalogService:
    db: Session

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_article(self, article_input: ArticleCreateInputSchema):
        """Create an article

        Args:
            input (ArticleCreateInputSchema): Input data for creating an article

        Returns:
            _type_: [ArticleModel]
        """
        article = ArticleModel(
            **{**article_input.model_dump(), "id": str(uuid.uuid4())}
        )
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

        article = (
            self.db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
        )
        article_input_data = article_input.model_dump()
        if article is not None:
            for key, value in article_input_data.items():
                if value is not None:
                    setattr(article, key, value)
            self.db.commit()
            self.db.refresh(article)
        return article

    def get_all_articles(self):
        """Retrieve all articles

        Returns:
            List[ArticleModel]: A list of all articles
        """
        return self.db.query(ArticleModel).all()

    def get_article_by_id(self, article_id: str):
        """Retrieve an article by its ID

        Args:
            article_id (str): The ID of the article to retrieve

        Returns:
            ArticleModel: The article if found, else None
        """
        return self.db.query(ArticleModel).filter(ArticleModel.id == article_id).first()

    def delete_article_by_id(self, article_id: str):
        """Delete an article by its ID

        Args:
            article_id (str): The ID of the article to delete

        Returns:
            ArticleModel: The deleted article if found, else None
        """
        article = (
            self.db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
        )

        if article:
            self.db.delete(article)
            self.db.commit()
            return article.id
        return None

    def search_article(self, search_term: str):
        """Search for an article by name or code

        Args:
            search_term (str): The name or code to search

        Returns:
            List[ArticleModel]: A list of articles that match the search term
        """
        return (
            self.db.query(ArticleModel)
            .filter(
                or_(
                    ArticleModel.name.ilike(f"%{search_term}%"),
                    ArticleModel.code.ilike(f"%{search_term}%"),
                )
            )
            .all()
        )

from http.client import HTTPException
from fastapi import APIRouter, Depends
from src.users.users_model import UserRole
from src.users.users_router import get_user_online_dep
from src.utils.constants import Constants
from src.catalog.catalog_schemas import (
    ArticleCreateInputSchema,
    ArticleEditInputSchema,
    ArticleOutputSchema,
)
from src.catalog.catalog_service import CatalogService

router = APIRouter(prefix=f"/{Constants.ARTICLES}", tags=[Constants.ARTICLES])


@router.post(
    "/",
    dependencies=[
        Depends(get_user_online_dep(roles=[UserRole.ADMIN, UserRole.SECRETARY]))
    ],
)
async def create_article(
    article_input: ArticleCreateInputSchema, catalog_service=Depends(CatalogService)
) -> ArticleOutputSchema:
    """Create an article

    The user must be an admin or a secretary to create an article

    """
    return catalog_service.create_article(article_input)


@router.patch(
    "/{article_id}",
    dependencies=[
        Depends(get_user_online_dep(roles=[UserRole.ADMIN, UserRole.SECRETARY]))
    ],
)
async def edit_article(
    article_id: str,
    article_input: ArticleEditInputSchema,
    catalog_service=Depends(CatalogService),
) -> ArticleOutputSchema | None:
    """Edit an article

    The user must be an admin or a secretary to edit an article

    """
    return catalog_service.edit_article(article_id, article_input)


@router.get("/", response_model=list[ArticleOutputSchema])
async def get_all_articles(search: str = None, catalog_service=Depends(CatalogService)):
    """Retrieve all articles
    if search is provided, search for articles by name or code
    Returns: List[ArticleOutputSchema]: A list of all articles
    """
    if search:
        return catalog_service.search_article(search)
    return catalog_service.get_all_articles()


@router.get("/{article_id}", response_model=ArticleOutputSchema | None)
async def get_article_by_id(article_id: str, catalog_service=Depends(CatalogService)):
    """Retrieve an article by its ID"""
    return catalog_service.get_article_by_id(article_id)


@router.delete(
    "/{article_id}",
    dependencies=[
        Depends(get_user_online_dep(roles=[UserRole.ADMIN, UserRole.SECRETARY]))
    ],
)
async def delete_article(
    article_id: str, catalog_service=Depends(CatalogService)
) -> str | None:
    """Delete an article by its ID
    Only an admin or a secretary can delete an article
    """
    return catalog_service.delete_article_by_id(article_id)

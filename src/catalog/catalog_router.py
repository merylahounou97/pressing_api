from fastapi import APIRouter, Depends
from src.users.users_model import UserRole
from src.users.users_router import get_user_online_dep
from src.utils.constants import Constants
from src.catalog.catalog_schemas import ArticleCreateInputSchema, ArticleOutputSchema
from src.catalog.catalog_service import CatalogService
router = APIRouter(prefix=f"/{Constants.ARTICLES}", tags=[Constants.ARTICLES])


@router.post("/", dependencies=[Depends(get_user_online_dep(
    roles=[UserRole.ADMIN, UserRole.SECRETARY]))])
async def create_article(article_input: ArticleCreateInputSchema,
                         catalog_service=Depends(CatalogService))-> ArticleOutputSchema:
    """Create an article

    The user must be an admin or a secretary to create an article

    """
    return catalog_service.create(article_input)

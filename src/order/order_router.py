from typing_extensions import Annotated
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

from src.config import Settings
from src.users.users_router import get_user_online_dep
from src.users.users_model import UserRole
from src.utils.constants import Constants
from src.order.order_service import OrderService
from src.order.order_schemas import OrderCreateInputSchema, OrderCreateOutputSchema


settings = Settings()

router = APIRouter(prefix=f"/{Constants.ORDERS}", tags=[Constants.ORDERS])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


AccessTokenDep = Annotated[str, Depends(oauth2_scheme)]

OrderServiceDep = Annotated[OrderService, Depends()]


@router.post("/", response_model=OrderCreateOutputSchema)
def create_order(
    create_order_input: OrderCreateInputSchema,
    order_service: OrderServiceDep,
    user=Depends(get_user_online_dep()),
):
    """Create an order"""
    if user.role in (UserRole.SECRETARY, UserRole.ADMIN):
        if create_order_input.customer_id is None:
            raise HTTPException(status_code=400, detail="The customer_id is required")
        return order_service.create(create_order_input=create_order_input)
    # If the user is a customer, we set the customer_id to the user id
    create_order_input.customer_id = user.id
    return order_service.create(create_order_input=create_order_input, user_id=user.id)

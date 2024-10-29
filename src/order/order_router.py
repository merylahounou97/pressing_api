from typing import Optional
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from src.users.users_router import get_user_online_dep
from src.users.users_model import UserRole
from src.utils.constants import Constants
from src.order.order_schemas import OrderCreateInputSchema, OrderCreateOutputSchema
from src.order.order_service import OrderService
from src.utils.error_messages import ErrorMessages

router = APIRouter(prefix=f"/{Constants.ORDERS}", tags=[Constants.ORDERS])


@router.post("/", response_model=OrderCreateOutputSchema)
async def create_order(
    order_input: OrderCreateInputSchema,
    order_service=Depends(OrderService),
    user=Depends(get_user_online_dep()),
):
    """Create an order. The customer can create an order for themselves, admins and secretaries can create for any customer."""
    if user.role == UserRole.CUSTOMER:
        #Ici l'utilisateur est un client et veut créer une commande pour lui-même
        order_input.customer_id = user.id
        return order_service.create_order(order_input)
    else:
        #Ici l'utilisateur est un admin ou un secrétaire et veut créer une commande pour un client
        #Dans ce cas, le client ID doit être fourni dans le paramètre de requête user_id
        if not order_input.customer_id:
            raise HTTPException(status_code=400, detail=ErrorMessages.USER_ID_NOT_PROVIDED)
        return order_service.create_order(order_input)


# @router.get("/", response_model=list[OrderCreateOutputSchema])
# async def get_all_orders(order_service=Depends(OrderService), user=Depends(get_user_online_dep())):
#     """Get all orders. Customers get their own, admins and secretaries get all orders."""
#     if user.role == UserRole.CUSTOMER:
#         return order_service.get_order_history(user.id)
#     return order_service.get_all_orders()

# @router.get("/{order_id}", response_model=OrderCreateOutputSchema)
# async def get_order_by_id(order_id: str, order_service=Depends(OrderService), user=Depends(get_user_online_dep())):
#     """Get order by ID."""
#     return order_service.get_order_by_id(order_id)

# @router.delete("/{order_id}")
# async def delete_order(order_id: str, order_service=Depends(OrderService), user=Depends(get_user_online_dep(roles=[UserRole.ADMIN, UserRole.SECRETARY]))):
#     """Delete an order. Only admins and secretaries can delete orders."""
#     return order_service.delete_order(order_id)

# @router.patch("/{order_id}", response_model=OrderCreateOutputSchema)
# async def edit_order(
#     order_id: str,
#     order_edit_input: OrderEditInputSchema,
#     order_service=Depends(OrderService),
#     user=Depends(get_user_online_dep(roles=[UserRole.ADMIN, UserRole.SECRETARY]))
# ):
#     """Edit an order. Only admins and secretaries can edit orders."""
#     return order_service.edit_order(order_id, order_edit_input)

# @router.get("/{order_id}/quote")
# async def get_order_quote(order_id: str, order_service=Depends(OrderService), user=Depends(get_user_online_dep())):
#     """Get the quote of an order."""
#     return order_service.get_order_quote(order_id)

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.dependencies.db import get_db
from src.order.order_enums import OrderStatusEnum
from src.order.order_model import OrderDetailsModel, OrderModel
from src.order.order_schemas import OrderCreateInputSchema, OrderCreateOutputSchema
from uuid import uuid4


class OrderService:
    db: Session

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_order(
        self, order_input: OrderCreateInputSchema
    ) -> OrderCreateOutputSchema:
        """Create a new order."""
        order_input_dict = order_input.model_dump()
        new_order = OrderModel(
            # id=str(uuid4()),
            order_date=order_input.order_date,
            delivery_date=order_input.delivery_date,
            type_order=order_input.type_order,
            collect=order_input.collect,
            delivery=order_input.delivery,
            customer_id=order_input.customer_id,
            status=OrderStatusEnum.PENDING,
        )
        self.db.add(new_order)
        self.db.commit()
        self.db.refresh(new_order)

        for order_detail in order_input.order_details:
            new_order_detail = OrderDetailsModel(
                order_id=new_order.id,
                article_id=order_detail.article_id,
                specificity=order_detail.specificity,
                divider_coef=order_detail.divider_coef,
                multiplier_coef=order_detail.multiplier_coef,
                discount_article=order_detail.discount_article,
                quantity=order_detail.quantity,
            )
            self.db.add(new_order_detail)
        
        self.db.commit()
        return OrderCreateOutputSchema(**order_input_dict,id=new_order.id,status=new_order.status)

    # def get_order_by_id(self, order_id: str) -> OrderCreateOutputSchema:
    #     """Get order by ID."""
    #     order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
    #     if not order:
    #         raise HTTPException(status_code=404, detail="Order not found")
    #     return OrderCreateOutputSchema(**order.__dict__)

    # def delete_order(self, order_id: str):
    #     """Delete an order."""
    #     order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
    #     if not order:
    #         raise HTTPException(status_code=404, detail="Order not found")
    #     self.db.delete(order)
    #     self.db.commit()
    #     return {"detail": "Order deleted successfully"}

    # def edit_order(self, order_id: str, order_edit_input: OrderEditInputSchema) -> OrderCreateOutputSchema:
    #     """Edit an order."""
    #     order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
    #     if not order:
    #         raise HTTPException(status_code=404, detail="Order not found")
    #     for key, value in order_edit_input.dict(exclude_unset=True).items():
    #         setattr(order, key, value)
    #     self.db.commit()
    #     self.db.refresh(order)
    #     return OrderCreateOutputSchema(**order.__dict__)

    # def get_all_orders(self):
    #     """Get all orders."""
    #     orders = self.db.query(OrderModel).all()
    #     return orders

    # def get_order_history(self, customer_id: str):
    #     """Get order history for a specific customer."""
    #     return self.db.query(OrderModel).filter(OrderModel.customer_id == customer_id).all()

    # def get_order_quote(self, order_id: str):
    #     """Calculate and return the order quote."""
    #     order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
    #     if not order:
    #         raise HTTPException(status_code=404, detail="Order not found")
    #     # Example quote calculation logic
    #     return {"order_id": order_id, "total_price": 100.0, "discounted_price": 90.0}

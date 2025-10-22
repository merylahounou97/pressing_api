from fastapi import Depends, HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.dependencies.db import get_db
from src.order.order_enums import OrderStatusEnum
from src.order.order_model import OrderDetailsModel, OrderModel
from src.order.order_schemas import (
    OrderCreateInputSchema,
    OrderCreateOutputSchema,
    OrderEditInputSchema,
    OrderDetailSchema,
    FullOrderSchema
)
from src.users.users_model import UserModel, UserRole


class OrderService:
    db: Session

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_order(
        self, order_input: OrderCreateInputSchema
    ) -> OrderCreateOutputSchema:
        """Create a new order."""

        try:
            order_input_dict = order_input.model_dump()
            new_order = OrderModel(
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
            order_input_dict["order_details"] = order_input.order_details
            return OrderCreateOutputSchema(
                **order_input_dict, id=new_order.id, status=new_order.status
            )
        except Exception as e:
            raise HTTPException(status_code=400) from e
        

    def get_order_by_id(self, order_id: int) -> OrderCreateOutputSchema:
        """Get order by ID."""

        order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()

        order_details = (
            self.db.query(OrderDetailsModel)
            .filter(OrderDetailsModel.order_id == order_id)
            .all()
        )
        order_dict = order.__dict__.copy()
        order_dict["order_details"] = [
            OrderDetailSchema(**detail.__dict__) for detail in order_details
        ]

        return OrderCreateOutputSchema(**order_dict)
    
    
    def get_order(self, order_id: int) -> OrderCreateOutputSchema:
        """Get order by ID, including user and details."""
        
        # order_details = (
        #     self.db.query(OrderDetailsModel)
        #     .filter(OrderDetailsModel.order_id == order_id)
        #                 .join(OrderDetailsModel.article)
        #     .options(joinedload(OrderDetailsModel.article))
        #     .all()

        # )

        # print("ORDER DETAILSsssssssssssssssssssssssss", order_details.__dict__)
        
        # Récupération de la commande + jointure avec user
        order = (
                self.db.query(OrderModel)
                .filter(OrderModel.id == order_id)
                .options(
                    joinedload(OrderModel.customer),              # jointure avec UserModel
                    joinedload(OrderModel.order_details)          # jointure avec OrderDetailsModel
                    .joinedload(OrderDetailsModel.article)        # jointure avec ArticleModel depuis OrderDetails
                )
                .first()
            )

        if not order:
            raise  HTTPException(status_code=400,detail="Order not found") 
        return order
                               
                


    def edit_order(
        self, order_id: str, order_edit_input: OrderEditInputSchema
    ) -> OrderCreateOutputSchema:
        """Edit an order."""
        # Get the order
        order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        # Check if the order exists
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Update the order
        for key, value in order_edit_input.model_dump(exclude_unset=True).items():
            # Update the order details
            if key == "order_details":
                for detail in value:
                    # update the order details if they exist
                    order_detail = (
                        self.db.query(OrderDetailsModel)
                        .filter(
                            OrderDetailsModel.order_id == order_id,
                            OrderDetailsModel.article_id == detail["article_id"],
                        )
                        .first()
                    )
                    if order_detail:
                        for key, value in detail.items():
                            setattr(order_detail, key, value)
                    else:
                        # Create a new order detail if it does not exist
                        new_order_detail = OrderDetailsModel(
                            order_id=order_id,
                            article_id=detail["article_id"],
                            specificity=detail["specificity"],
                            divider_coef=detail["divider_coef"],
                            multiplier_coef=detail["multiplier_coef"],
                            discount_article=detail["discount_article"],
                            quantity=detail["quantity"],
                        )
                        self.db.add(new_order_detail)
            else:
                setattr(order, key, value)

        self.db.commit()

        # Delete the articles to delete
        if order_edit_input.articles_to_delete:
            self.db.query(OrderDetailsModel).filter(
                OrderDetailsModel.order_id == order_id,
                OrderDetailsModel.article_id.in_(order_edit_input.articles_to_delete),
            ).delete()

        self.db.commit()

        # Return the updated order
        return self.get_order_by_id(order_id)

    def get_all_orders(self):
        """Get all orders."""

        # Get all orders with their details in the form [(OrderModel, OrderDetailsModel), ...]
        results = (
            self.db.query(OrderModel)
            .join(OrderDetailsModel, OrderModel.id == OrderDetailsModel.order_id)
            .add_entity(OrderDetailsModel)
            .all()
        )

        return self.match_orders_to_order_details(results)

    def match_orders_to_order_details(self, results):
        # Convert the results to a list of orders in the form {OrderModel1, OrderModel2, ...}
        orders = {result[0] for result in results}

        # Convert the orders to a list of dictionaries in the form [{OrderModel1}, {OrderModel2}, ...]
        orders = [{**order.__dict__, "order_details": None} for order in orders]

        for order in orders:
            # Get the order details for each order by filtering the results
            order_details_fitered = filter(
                lambda x: x[1].order_id == order["id"], results
            )
            # Extract the order details
            order_details = [order_detail[1] for order_detail in order_details_fitered]
            order["order_details"] = order_details

        return orders

    def cancel_order(self, order_id: str):
        """Cancel an order."""

        order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()

        if order:
            order.status = OrderStatusEnum.CANCELED
            self.db.commit()
            self.db.refresh(order)
        return self.get_order_by_id(order_id)

    def get_order_history(self, customer_id: str):
        """Get order history."""
        # orders = (
        #     self.db.query(OrderModel)
        #     .filter(OrderModel.customer_id == customer_id)
        #     .all()
        # )
        results = (
            self.db.query(OrderModel)
            .join(OrderDetailsModel, OrderModel.id == OrderDetailsModel.order_id)
            .add_entity(OrderDetailsModel)
            .filter(OrderModel.customer_id == customer_id)
            .all()
        )

        return self.match_orders_to_order_details(results)

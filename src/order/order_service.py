import uuid
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.config import Settings
from src.dependencies.db import get_db
from src.mail import mail_service
from src.security import security_service
from src.sms import sms_service

from src.utils.error_messages import ErrorMessages
from src.utils.functions import get_identifier_type
from src.utils.mail_constants import MailConstants
from src.utils.sms_constants import SmsConstants
from src.order.order_schemas import OrderCreateInputSchema, OrderCreateOutputSchema



class OrderService:
    """User service class"""

    db: Session

    def __init__(self,db: Session = Depends(get_db)):
        self.db = db

    def create(self, user_create_input: OrderCreateInputSchema) -> OrderCreateOutputSchema:
        """Create a user

        Args:
            user_create_input (UserCreateInput): The user input

        Returns:
            UserOutput: The created user
        """

        return None
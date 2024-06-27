import uuid
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.config import Settings
from src.dependencies.db import get_db
from src.dependencies.get_api_url import get_api_url
from src.mail import mail_service
from src.security import security_service
from src.sms import sms_service
from src.users.user_model import UserModel
from src.users.user_schemas import (ChangeUserPassword, IdentifierEnum,
                                    ResetPasswordInput, UserBaseSchema,
                                    UserCreateInput, VerifyIdentifierInput)
from src.utils.error_messages import ErrorMessages
from src.utils.functions import get_identifier_type
from src.utils.mail_constants import MailConstants
from src.utils.sms_constants import SmsConstants

settings = Settings()


class UserService:
    """User service class"""

    db: Session

    def __init__(self,db: Session = Depends(get_db)):
        self.db = db

    def create(self, user_create_input: UserCreateInput):
        """Create a user in the database


        Args:
            user_create_input (UserCreateInput): User create input

        Returns:
            UserModel: The created user
        """

        if user_create_input.phone_number is None and user_create_input.email is None:
            raise HTTPException(
                status_code=400, detail="Phone number and email cannot be both empty"
            )

        try:
            hashed_password = security_service.hash_text(user_create_input.password)

            verification_code_email = security_service.generate_random_code()
            verification_code_phone_number = security_service.generate_random_code()
            expiry_time = datetime.now() + timedelta(minutes=settings.code_expiry_time)

            user_id = (str(uuid.uuid4()),)
            db_user = UserModel(
                id=user_id,
                email=user_create_input.email,
                phone_number=user_create_input.phone_number,
                last_name=user_create_input.last_name,
                first_name=user_create_input.first_name,
                phone_number_verification_code=verification_code_phone_number,
                email_verification_code=verification_code_email,
                address=user_create_input.address,
                password=hashed_password,
                phone_number_verification_expiry=expiry_time,
                email_verification_expiry=expiry_time,
            )

            self.db.add(db_user)

            self.db.commit()

            # Send welcome email
            if user_create_input.email is not None:
                api_url = get_api_url()

                mail_service.send_mail_from_template(
                    MailConstants.WELCOME_EMAIL,
                    db_user.email,
                    app_name=settings.app_name,
                    person=db_user,
                    api_url=api_url,
                )

            if user_create_input.phone_number is not None:
                # Envoyer le SMS de vérification
                sms_service.send_welcome_sms(db_user)

            return db_user
        except Exception as e:
            is_unique_violation = str(e).count("psycopg2.errors.UniqueViolation") == 1
            if is_unique_violation:
                raise HTTPException(
                    status_code=400, detail="Phone number or email already registered"
                ) from e
            raise HTTPException(status_code=400, detail=str(e)) from e

    def verify_code(self,verification: VerifyIdentifierInput):
        """Verify the code

        Args:
            verification (Customer_verify_code): Verification object
            strategy (str): Verification strategy
            db (Session): Database session

        Returns:
            Customer_model: Customer object
        """

        strategy = get_identifier_type(verification.identifier)

        strategy_string = strategy.name.lower()

        if strategy == IdentifierEnum.EMAIL:
            db_user = (
                self.db.query(UserModel)
                .filter(
                    UserModel.email == verification.identifier,
                    UserModel.email_verification_code == verification.verification_code,
                )
                .first()
            )

            if db_user is not None:
                expiry_date_time = db_user.email_verification_expiry

        elif strategy == IdentifierEnum.PHONE_NUMBER:
            db_user = (
                self.db.query(UserModel)
                .filter(
                    UserModel.phone_number == verification.identifier,
                    UserModel.phone_number_verification_code
                    == verification.verification_code,
                ).first()
            )
            if db_user is not None:
                expiry_date_time = db_user.phone_number_verification_expiry
        else:
            raise HTTPException(status_code=500, detail="Unknown strategy")

        if not db_user:
            raise HTTPException(status_code=400, detail="Code de vérification invalid")

        if expiry_date_time <= datetime.now():
            setattr(db_user, f"{strategy_string}_verification_code", None)
            self.db.commit()
            self.db.refresh(db_user)
            raise HTTPException(status_code=400, detail="Code de vérification expiré")

        setattr(db_user, f"{strategy_string}_verified", 1)
        setattr(db_user, f"{strategy_string}_verification_code", None)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def generate_new_validation_code(self,identifier: str):
        """Generate a new validation code

        Args:
            generate_new_validation_code
            (user_schema.Customer_generate_new_validation_code_input): Generate new validation
                                                                                        code object

        Returns:
            None
        """

        strategy = get_identifier_type(identifier)

        user = self.get_user_by_identifier(identifier)

        if user is not None:
            random_code = security_service.generate_random_code()

            if strategy == IdentifierEnum.EMAIL and not user.email_verified:
                self.set_new_email(user, user.email, random_code=random_code)
                self.db.commit()

                mail_service.send_mail_from_template(
                    MailConstants.EMAIL_VERIFICATION, email=user.email, person=user
                )

                return user

            if (
                strategy == IdentifierEnum.PHONE_NUMBER
                and not user.phone_number_verified
            ):
                user.phone_number_verification_code = random_code
                user.phone_number_verification_expiry = datetime.now() + timedelta(
                    minutes=settings.code_expiry_time
                )

                self.db.commit()

                sms_service.send_verification_sms(identifier, random_code)

                return user
            elif user.phone_number_verified or user.email_verified:
                return None
            else:
                raise HTTPException(status_code=400, detail="Unknown strategy")
        return None
    

    def get_user_by_identifier(self,identifier: str) -> UserModel | None:
        """Get a user by identifier from the database
        Args:
            identifier (str): The user identifier can be email or phone number

        Returns:
            Customer_model: The user object
        """
        return (
            self.db.query(UserModel)
            .filter(
                or_(
                    UserModel.phone_number == identifier,
                    UserModel.email == identifier,
                )
            )
            .first()
        )
    

    def set_new_email(self,user_online: UserModel, email: str, random_code: int):
        """Set a new email for a user
        Change the email of the user and generate a new verification code for the new email.
        put the new email to non verified
        and add the expiration of the verification code

        Args:
            user_online (Customer_model): Customer object
            email (str): New email

            Returns:
                Customer_model: Customer object
        """
        user_online.email = email
        user_online.email_verification_code = random_code
        user_online.email_verification_expiry = datetime.now() + timedelta(
            minutes=settings.code_expiry_time
        )
        user_online.email_verified = 0
        return None
    
    def authenticate_user(self, identifier: str, password: str):
        """Authenticate a user by email or phone number

        args:
            db (Session): The database session
            identifier (str): The identifier
            password (str): The password

        Returns:
            Customer_model: The user
        """
        user = self.get_user_by_identifier( identifier)
        if user is not None and security_service.compare_hashed_text(
            password, user.password
        ):
            return user
        return None
        
    def change_password(self,
        user_online: UserModel,
        change_password_input: ChangeUserPassword
    ):
        """Change the password

        Args:
            user_online (Customer_model): Customer object
            change_password_input (Customer_change_password_input): Change password input

            Returns:
                Customer_model: Customer object
        """

        if not (
            user_online.is_valid_email() or user_online.is_valid_phone_number()
        ):
            raise HTTPException(
                status_code=400,
                detail=ErrorMessages.EMAIL_OR_PHONE_NUMBER_VERIFICATION_REQUIRED,
            )

        if change_password_input.old_password == change_password_input.new_password:
            raise HTTPException(
                status_code=400, detail=ErrorMessages.NEW_PASSWORD_SAME_AS_OLD
            )

        if security_service.compare_hashed_text(
            change_password_input.old_password, user_online.password
        ):
            user_online.password = security_service.hash_text(
                change_password_input.new_password
            )
            self.db.commit()

            if user_online.is_valid_phone_number():
                sms_service.send_sms(
                    user_online.phone_number,
                    template_name=SmsConstants.PASSWORD_CHANGED,
                    user=user_online,
                    support_address=settings.support_address,
                )

            if user_online.is_valid_email():
                mail_service.send_mail_from_template(
                    MailConstants.PASSWORD_CHANGED,
                    email=user_online.email,
                    user=user_online,
                    support_address=settings.support_address,
                )
            return user_online

        raise HTTPException(status_code=400, detail=ErrorMessages.WRONG_OLD_PASSWORD)

    def validate_token(self,access_token: str):
        """Validate the access token

        Args:
            access_token (str): Access token
            db (Session): Database session

        Returns:
            Customer_model: Customer object
        """
        payload = security_service.decode_token(access_token)
        user = self.get_user_by_id(payload["sub"])
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return user
        
    def get_user_by_id(self,user_id: str):
        """Get a user by id

        Args:
            user_id (str): The user id
            db (Session): The database session

        Returns:
            Customer_model: The user object
        """
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()
    
    def reset_password(self,identifier: str):
        """Reset the password

        Args:
            identifier (str): The identifier
            db (Session): Database session

        Returns:
            Customer_model: The user
        """

        user = self.get_user_by_identifier( identifier)


        if user is None:
            raise HTTPException(status_code=400, detail="User not found")

        random_code = security_service.generate_random_code()
        user.reset_password_code = random_code
        self.db.commit()

        strategy = get_identifier_type(identifier)
        if strategy == IdentifierEnum.EMAIL and user.email is not None:
            mail_service.send_mail_from_template(
                MailConstants.PASSWORD_RESET, email=user.email, user=user
            )
        elif (
            strategy == IdentifierEnum.PHONE_NUMBER
            and user.phone_number is not None
        ):
            sms_service.send_sms(
                user.phone_number,
                template_name=SmsConstants.PASSWORD_RESET,
                user=user,
            )
        else:
            raise HTTPException(status_code=500, detail="Invalid user identifier")

        return user
    
    def submit_reset_password(self,reset_input: ResetPasswordInput):
        """Submit the reset password

        Args:
            reset_input (ResetPasswordInput): The reset input
        Returns:
            Customer_model: The user
        """
        user = self.get_user_by_identifier( reset_input.identifier)
        if user is None:
            raise HTTPException(status_code=400, detail="User not found")

        if user.reset_password_code != reset_input.verification_code:
            raise HTTPException(status_code=400, detail="Invalid verification code")

        user.password = security_service.hash_text(reset_input.new_password)
        user.reset_password_code = None
        self.db.commit()
        return user
    
    def edit_user(self,
        user_online: UserModel,
        user_edit_input: UserBaseSchema
    ):
        """Edit a user

        Args:
            user_id (str): Customer ID
            user_edit_input (Customer_edit_input): Customer edit input
            db (Session): Database session

        Returns:
            Customer_model: Customer object
        """

        user_old_mail = user_online.email
        user_old_sms = user_online.phone_number
        if user_edit_input.last_name is not None:
            user_online.last_name = user_edit_input.last_name
        if user_edit_input.first_name is not None:
            user_online.first_name = user_edit_input.first_name
        if user_edit_input.address is not None:
            user_online.address = user_edit_input.address

        if (
            user_edit_input.email is not None
            and user_edit_input.email != user_online.email
        ):
            random_code = security_service.generate_random_code()
            self.set_new_email(user_online, user_edit_input.email, random_code)

        if (
            user_edit_input.phone_number is not None
            and user_edit_input.phone_number != user_online.phone_number
        ):
            self.set_new_phone_number(user_online, user_edit_input.phone_number)

        self.db.commit()

        # Sent email if it has been changed
        if (
            user_edit_input.email is not None
            and user_edit_input.email != user_old_mail
        ):
            mail_service.send_mail_from_template(
                MailConstants.UPDATE_EMAIL,
                email=user_edit_input.email,
                user=user_online,
                redirect_url="google.com",
            )

        # Send SMS if it has been changed
        if (
            user_edit_input.phone_number is not None
            and user_edit_input.phone_number != user_old_sms
        ):
            sms_service.send_sms(
                user_online.phone_number,
                template_name=SmsConstants.PHONE_NUMBER_CHANGED,
                user=user_online,
                support_address=settings.support_address,
            )


        return user_online

    def set_new_phone_number(self,user_online: UserModel, phone_number: str):
        """Set a new phone number for a user
        Change the phone number of the user 
        and generate a new verification code for the new phone number.
        put the new phone number to non verified
        and add the expiration of the verification code
        """

        user_online.phone_number = phone_number
        user_online.phone_number_verification_code = (
            security_service.generate_random_code()
        )
        user_online.phone_number_verification_expiry = datetime.now() + timedelta(
            minutes=settings.code_expiry_time
        )
        user_online.phone_number_verified = 0
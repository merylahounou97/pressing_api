import random
from datetime import datetime, timedelta, timezone
from typing import Union

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from passlib.hash import bcrypt
from fastapi import HTTPException

from src.config import get_settings, Settings

settings = get_settings()


def hash_text(text: str) -> str:
    """Hashes the given text using bcrypt algorithm
    and returns the hashed text.

    Args:
        text (str): The text to hash.

        Returns:
        str: The hashed text.
    """
    return bcrypt.hash(text)


def compare_hashed_text(text: str, hashed_text: str) -> bool:
    """Compares the given text with the given hashed text.

    Args:
        text (str): The text to compare.
        hashed_text (str): The hashed text to compare.

    Returns:
        bool: True if the text matches the hashed text, False otherwise.
    """
    return bcrypt.verify(text, hashed_text)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """Creates an access token with the given data and expiration time.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (Union[timedelta, None], optional): The expiration time.

    Returns:
        str: The encoded token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_token(token: str):
    """Decodes the given token and returns the payload.

    Args:
        token (str): The token to decode.

    Returns:
        dict: The payload of the token.
    """
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Expired token. Please provide a valid token."
        )
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid token. Please provide a valid token."
        )


def generate_random_code(low=100, high=99999):
    """Generates a random code between the given range.

    Args:
        low (int, optional): The lower bound of the range.
        high (int, optional): The upper bound of the range.

    Returns:
        str: The generated code.
    """
    return str(random.randint(low, high))

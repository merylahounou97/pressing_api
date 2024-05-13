from passlib.hash import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Union
from jose import jwt

SECRET_KEY = "AJyt451u#a@QKHFS9584TF-'Srfg"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hashText(text: str) -> str:
    return bcrypt.hash(text)

def compareHashedText(text: str, hashed_text: str) -> bool:
    return bcrypt.verify(text, hashed_text)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    return jwt.decode(str(token), SECRET_KEY, algorithms=[ALGORITHM])
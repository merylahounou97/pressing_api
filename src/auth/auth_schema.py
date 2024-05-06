from pydantic import BaseModel

class Login_input(BaseModel):
    identifier: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
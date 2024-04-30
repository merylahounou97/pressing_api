from pydantic import BaseModel

class Login_input(BaseModel):
    identifier: str
    password: str

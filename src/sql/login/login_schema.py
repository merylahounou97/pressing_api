from pydantic import BaseModel

class Login_schema(BaseModel):
    identifier: str
    password: str

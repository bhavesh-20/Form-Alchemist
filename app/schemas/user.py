from pydantic import BaseModel


class RegisterUser(BaseModel):
    username: str
    email: str
    mobile_number: str
    password: str

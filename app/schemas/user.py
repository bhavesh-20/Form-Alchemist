from uuid import UUID

from pydantic import BaseModel


class RegisterUser(BaseModel):
    username: str
    email: str
    mobile_number: str
    password: str


class LoginUserResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    mobile_number: str

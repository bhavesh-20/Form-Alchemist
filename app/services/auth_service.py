import re
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import or_
from sqlalchemy.sql.expression import insert, select

from app import Config, db, oauth2_scheme
from app.models import User
from app.schemas import RegisterUser


class AuthService:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    async def validate_user_payload(cls, payload: RegisterUser):
        # regex payload.email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", payload.email):
            raise HTTPException(status_code=400, detail="Invalid email")
        # regex payload.mobile_number
        if not re.match(r"^[0-9]{10}$", payload.mobile_number):
            raise HTTPException(status_code=400, detail="Invalid mobile number")

    @classmethod
    async def register_user(cls, payload: RegisterUser):
        await cls.validate_user_payload(payload)
        existing_user = await db.fetch_one(
            select([User]).where(
                or_(
                    User.username == payload.username,
                    User.email == payload.email,
                    User.mobile_number == payload.mobile_number,
                )
            )
        )
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="User already exists",
            )
        await db.execute(
            insert(User).values(
                username=payload.username,
                email=payload.email,
                mobile_number=payload.mobile_number,
                password=cls.pwd_context.hash(payload.password),
            )
        )
        return {"message": "Signup Successful"}

    @classmethod
    async def create_access_token(cls, data: int):
        to_encode = data.copy()
        to_encode.update({"exp": datetime.now() + timedelta(minutes=60)})
        access_token = jwt.encode(to_encode, Config.SECRET_KEY, algorithm="HS256")
        return access_token

    @classmethod
    async def get_authenticated_user(cls, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except JWTError:
            raise HTTPException(
                status_code=400,
                detail="Invalid token",
            )
        user_data = payload
        user = await db.fetch_one(select([User]).where(User.id == user_data["user_id"]))
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )
        return user

    @classmethod
    async def login_user(cls, payload: OAuth2PasswordRequestForm):
        user = await db.fetch_one(
            select([User]).where(User.username == payload.username)
        )
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User with given username does not exist",
            )
        if not cls.pwd_context.verify(payload.password, user.password):
            raise HTTPException(
                status_code=400,
                detail="Incorrect password",
            )
        access_token = await cls.create_access_token(
            {"username": user.username, "user_id": str(user.id)}
        )
        return {"access_token": access_token, "token_type": "bearer"}

import re

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import or_
from sqlalchemy.sql.expression import insert, select

from app import db
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

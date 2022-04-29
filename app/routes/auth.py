from fastapi import APIRouter

from app.schemas import RegisterUser
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def RegisterUser(payload: RegisterUser):
    return await AuthService.register_user(payload)

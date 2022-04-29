from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import LoginUserResponse, RegisterUser, UserResponse
from app.services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def RegisterUser(payload: RegisterUser):
    return await AuthService.register_user(payload)


@router.post("/login", response_model=LoginUserResponse)
async def LoginUser(payload: OAuth2PasswordRequestForm = Depends()):
    return await AuthService.login_user(payload)


@router.post("/user", response_model=UserResponse)
async def GetUser(user: UserResponse = Depends(AuthService.get_authenticated_user)):
    return user

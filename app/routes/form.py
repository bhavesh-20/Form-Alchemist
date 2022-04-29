from fastapi import APIRouter, Depends

from app.schemas import FormCreateResponse, FormMetadata, FormResponse, UserResponse
from app.services import AuthService, FormService

router = APIRouter(prefix="/form", tags=["forms"])


@router.post("", response_model=FormCreateResponse)
async def CreateForm(
    form_metadata: FormMetadata,
    user: UserResponse = Depends(AuthService.get_authenticated_user),
):
    return await FormService.create_form(form_metadata, user)


@router.get("/{form_id}", response_model=FormResponse)
async def GetForm(form_id: str):
    return await FormService.get_form(form_id)


@router.patch("/{form_id}", response_model=FormResponse)
async def UpdateForm(
    form_id: str,
    form_metadata: FormMetadata,
    user: UserResponse = Depends(AuthService.get_authenticated_user),
):
    return await FormService.update_form(form_id, form_metadata, user)


@router.delete("/{form_id}")
async def DeleteForm(
    form_id: str, user: UserResponse = Depends(AuthService.get_authenticated_user)
):
    return await FormService.delete_form(form_id, user)

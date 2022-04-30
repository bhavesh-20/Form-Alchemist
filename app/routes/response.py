from fastapi import APIRouter, BackgroundTasks, Depends

from app.services import AuthService, ResponseService

router = APIRouter(prefix="/form", tags=["response"])


@router.post("/{form_id}/response")
async def CreateResponse(
    form_id: str,
    response_data: dict[str, str],
    background_tasks: BackgroundTasks,
):
    return await ResponseService.create_response(
        form_id, response_data, background_tasks
    )


@router.get("/{form_id}/response")
async def GetResponses(
    form_id: str,
    limit: int = 10,
    user: dict = Depends(AuthService.get_authenticated_user),
):
    return await ResponseService.get_responses(form_id, limit, user)

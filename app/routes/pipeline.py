from fastapi import APIRouter, Depends

from app.schemas import UserResponse
from app.services import AuthService, PipelineService

router = APIRouter(prefix="/pipeline", tags=["Monitoring Pipelines"])


@router.get("/form/{form_id}")
async def get_pipelines(
    form_id: str,
    limit: int = 10,
    user: UserResponse = Depends(AuthService.get_authenticated_user),
):
    return await PipelineService.get_pipelines(form_id, limit, user)


@router.get("/{pipeline_id}")
async def get_pipeline_by_id(
    pipeline_id: str, user: UserResponse = Depends(AuthService.get_authenticated_user)
):
    return await PipelineService.get_pipeline_by_id(pipeline_id, user)

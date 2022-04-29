from fastapi import APIRouter, Depends

from app.schemas import (
    QuestionMetadata,
    QuestionResponse,
    QuestionsResponse,
    UserResponse,
)
from app.services import AuthService, QuestionService

router = APIRouter(prefix="/form", tags=["questions"])


@router.post("/{form_id}/question")
async def CreateQuestion(
    form_id: str,
    question_metadata: QuestionMetadata,
    user: UserResponse = Depends(AuthService.get_authenticated_user),
):
    return await QuestionService.create_question(form_id, question_metadata, user)


@router.get("/{form_id}/question", response_model=QuestionsResponse)
async def GetQuestionsForForm(
    form_id: str, user: UserResponse = Depends(AuthService.get_authenticated_user)
):
    return await QuestionService.get_form_questions(form_id, user)


@router.get("/{form_id}/question/{question_id}", response_model=QuestionResponse)
async def GetQuestion(
    form_id: str,
    question_id: str,
    user: UserResponse = Depends(AuthService.get_authenticated_user),
):
    return await QuestionService.get_question(form_id, question_id, user)


@router.patch("/{form_id}/question/{question_id}", response_model=QuestionResponse)
async def UpdateQuestion(
    form_id: str,
    question_id: str,
    question_metadata: QuestionMetadata,
    user: UserResponse = Depends(AuthService.get_authenticated_user),
):
    return await QuestionService.update_question(
        form_id, question_id, question_metadata, user
    )


@router.delete("/{form_id}/question/{question_id}")
async def DeleteQuestion(
    form_id: str,
    question_id: str,
    user: UserResponse = Depends(AuthService.get_authenticated_user),
):
    return await QuestionService.delete_question(form_id, question_id, user)

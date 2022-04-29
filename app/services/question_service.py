from fastapi import HTTPException
from sqlalchemy.sql.expression import delete, insert, select, update

from app import db
from app.models import Question
from app.schemas import QuestionMetadata, UserResponse
from app.services import FormService


class QuestionService:
    @classmethod
    async def create_question(
        cls, form_id: str, question_metadata: QuestionMetadata, user: UserResponse
    ):
        form = await FormService.get_user_form(form_id, user)
        question = await db.execute(
            insert(Question).values(
                form_id=form.id,
                question=question_metadata.question,
                is_required=question_metadata.is_required,
            )
        )
        return {"message": "Question created successfully", "question_id": question}

    @classmethod
    async def get_form_questions(cls, form_id: str):
        form = await FormService.get_form(form_id)
        questions = await db.fetch_all(
            select([Question]).where(Question.form_id == form.id)
        )
        return {"questions": questions}

    @classmethod
    async def get_question(cls, form_id: str, question_id: str):
        form = await FormService.get_form(form_id)
        question = await db.fetch_one(
            select([Question]).where(
                Question.id == question_id, Question.form_id == form.id
            )
        )
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return question

    @classmethod
    async def update_question(
        cls,
        form_id: str,
        question_id: str,
        question_metadata: QuestionMetadata,
        user: UserResponse,
    ):
        form = await FormService.get_user_form(form_id, user)
        await db.execute(
            update(Question)
            .where(Question.id == question_id, Question.form_id == form.id)
            .values(
                question=question_metadata.question,
                is_required=question_metadata.is_required,
            )
        )
        return await cls.get_question(form_id, question_id, user)

    @classmethod
    async def delete_question(cls, form_id: str, question_id: str, user: UserResponse):
        form = await FormService.get_user_form(form_id, user)
        await db.execute(
            delete(Question).where(
                Question.id == question_id, Question.form_id == form.id
            )
        )
        return {"message": "Question deleted successfully"}

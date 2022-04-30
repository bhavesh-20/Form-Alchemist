from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.sql.expression import insert, select
from sqlalchemy.sql.functions import func

from app import db
from app.models import Answer, Question, Response
from app.schemas import UserResponse

from .form_service import FormService
from .pipeline_service import PipelineService
from .question_service import QuestionService


class ResponseService:
    @classmethod
    async def create_response(
        cls, form_id: str, response_data: dict, background_tasks: BackgroundTasks
    ):
        form = await FormService.get_form(form_id)
        questions = await QuestionService.get_form_questions(form_id)
        if "user_mobile_number" not in response_data:
            raise HTTPException(
                status_code=400, detail="Missing Response user mobile number"
            )

        for question in questions["questions"]:
            if question.is_required and str(question.id) not in response_data:
                raise HTTPException(
                    status_code=400,
                    detail="Missing required field: {}".format(question.id),
                )

        response_id = await db.execute(
            insert(Response).values(
                form_id=form_id, user_mobile_number=response_data["user_mobile_number"]
            )
        )

        answers = []
        for question in questions["questions"]:
            answer = response_data.get(str(question.id))
            if answer:
                answers.append(
                    {
                        "question_id": question.id,
                        "answer": answer,
                        "response_id": response_id,
                    }
                )
        query = "insert into answers (question_id, answer, response_id) values (:question_id, :answer, :response_id)"
        await db.execute_many(query, values=answers)
        background_tasks.add_task(PipelineService.create_pipeline, response_id)
        return {
            "message": "Response submitted successfully",
            "response_id": response_id,
        }

    @classmethod
    async def get_responses(cls, form_id: str, limit: int, user: UserResponse):
        form = await FormService.get_user_form(form_id, user)
        query = (
            select(
                Response.id,
                func.json_agg(
                    func.json_build_object(Question.question, Answer.answer)
                ).label("response"),
            )
            .select_from(Response.__table__.join(Answer).join(Question))
            .group_by(Response.id)
            .where(Response.form_id == form_id)
            .order_by(Response.created_at.desc())
            .limit(limit)
        )
        responses = await db.fetch_all(query)
        return responses

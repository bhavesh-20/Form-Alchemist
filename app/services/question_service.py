import xlsxwriter
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.sql.expression import delete, insert, select, update
from sqlalchemy.sql.functions import func

from app import db, spreadsheet_service
from app.db import SessionLocal
from app.models import Answer, Question, SheetsMetadata
from app.schemas import QuestionMetadata, UserResponse

from .form_service import FormService


class QuestionService:
    @classmethod
    def add_question_spreadsheet(cls, form_id: str, question_id: str, question: str):
        spreadsheet = spreadsheet_service.open(form_id)
        worksheet = spreadsheet.get_worksheet(0)
        with SessionLocal() as session:
            sheets_metadata = (
                session.query(func.max(SheetsMetadata.question_column).label("column"))
                .filter(SheetsMetadata.form_id == form_id)
                .first()
            )
            if not sheets_metadata.column:
                sheets_metadata = SheetsMetadata(
                    form_id=form_id, question_column=2, question_id=question_id
                )
                session.add(sheets_metadata)
            else:
                sheets_metadata = SheetsMetadata(
                    form_id=form_id,
                    question_column=sheets_metadata.column + 1,
                    question_id=question_id,
                )
                session.add(sheets_metadata)
            if sheets_metadata.question_column > worksheet.col_count:
                worksheet.add_cols(1)
            worksheet.update_cell(1, sheets_metadata.question_column, question)
            worksheet.format(
                xlsxwriter.utility.xl_range(
                    0,
                    sheets_metadata.question_column - 1,
                    0,
                    sheets_metadata.question_column - 1,
                ),
                {
                    "backgroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0},
                    "horizontalAlignment": "CENTER",
                    "textFormat": {
                        "foregroundColor": {"red": 0.0, "green": 0.0, "blue": 0.0},
                        "fontSize": 12,
                        "bold": True,
                    },
                },
            )
            worksheet.columns_auto_resize(0, worksheet.col_count - 1)
            session.commit()

    @classmethod
    async def create_question(
        cls,
        form_id: str,
        question_metadata: QuestionMetadata,
        user: UserResponse,
        background_tasks: BackgroundTasks,
    ):
        form = await FormService.get_user_form(form_id, user)
        question = await db.execute(
            insert(Question).values(
                form_id=form.id,
                question=question_metadata.question,
                is_required=question_metadata.is_required,
            )
        )
        background_tasks.add_task(
            cls.add_question_spreadsheet,
            form_id,
            str(question),
            question_metadata.question,
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
    def update_question_spreadsheet(cls, form_id: str, question_id: str, question: str):
        spreadsheet = spreadsheet_service.open(form_id)
        worksheet = spreadsheet.get_worksheet(0)
        with SessionLocal() as session:
            sheets_metadata = (
                session.query(SheetsMetadata)
                .filter(
                    SheetsMetadata.form_id == form_id,
                    SheetsMetadata.question_id == question_id,
                )
                .first()
            )
            worksheet.update_cell(1, sheets_metadata.question_column, question)

    @classmethod
    async def update_question(
        cls,
        form_id: str,
        question_id: str,
        question_metadata: QuestionMetadata,
        user: UserResponse,
        background_tasks: BackgroundTasks,
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
        background_tasks.add_task(
            cls.update_question_spreadsheet,
            form_id,
            question_id,
            question_metadata.question,
        )
        return await cls.get_question(form_id, question_id)

    @classmethod
    def delete_question_spreadsheet(cls, form_id: str, question_column: int):
        spreadsheet = spreadsheet_service.open(form_id)
        worksheet = spreadsheet.get_worksheet(0)
        worksheet.delete_columns(question_column, question_column)
        with SessionLocal() as session:
            session.query(SheetsMetadata).filter(
                SheetsMetadata.form_id == form_id,
                SheetsMetadata.question_column > question_column,
            ).update(
                {SheetsMetadata.question_column: SheetsMetadata.question_column - 1}
            )
            session.commit()

    @classmethod
    async def delete_question(
        cls,
        form_id: str,
        question_id: str,
        user: UserResponse,
        background_tasks: BackgroundTasks,
    ):
        form = await FormService.get_user_form(form_id, user)
        question_column = await db.fetch_one(
            select([SheetsMetadata.question_column]).where(
                SheetsMetadata.form_id == form.id,
                SheetsMetadata.question_id == question_id,
            )
        )
        await db.execute(
            delete(Question).where(
                Question.id == question_id, Question.form_id == form.id
            )
        )
        background_tasks.add_task(
            cls.delete_question_spreadsheet, form_id, question_column.question_column
        )
        return {"message": "Question deleted successfully"}

    @classmethod
    async def get_answers_for_question(
        cls, form_id: str, question_id: str, user: UserResponse
    ):
        form = await FormService.get_user_form(form_id, user)
        question = await cls.get_question(form_id, question_id)

        answers = await db.fetch_all(
            select([Answer]).where(Answer.question_id == question.id)
        )
        print(answers)
        return {"question": question.question, "answers": answers}

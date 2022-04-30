from sqlalchemy.sql.expression import select
from sqlalchemy.sql.functions import func

from app import spreadsheet_service
from app.db import SessionLocal
from app.models import Answer, Question, Response, SheetsMetadata
from app.schemas import TriggerEnum
from app.utils import write_log


class JobService:
    @classmethod
    def run_job(cls, job, response_id):
        try:
            if job.trigger == TriggerEnum.RECEIPT_SMS:
                cls.send_receipt_sms(response_id)
            elif job.trigger == TriggerEnum.GOOGLE_SHEETS:
                cls.update_google_sheets(response_id)
            job.status = "completed"
        except Exception as e:
            write_log(f"Job {job.id} failed with error: {e}")
            job.status = "failed"

    @classmethod
    def send_receipt_sms(cls, response_id):
        with SessionLocal() as session:
            query = (
                select(
                    Response.id,
                    Response.user_mobile_number,
                    func.json_agg(
                        func.json_build_object(Question.question, Answer.answer)
                    ).label("response"),
                )
                .select_from(Response.__table__.join(Answer).join(Question))
                .group_by(Response.id)
                .where(Response.id == response_id)
            )
            response = session.execute(query).fetchone()
            write_log(
                f"SMS sent to {response.user_mobile_number}, Content: {response.response}"
            )

    @classmethod
    def update_google_sheets(cls, response_id):
        with SessionLocal() as session:
            response = (
                session.query(Response).filter(Response.id == response_id).first()
            )
            spreadsheet = spreadsheet_service.open(str(response.form_id))
            worksheet = spreadsheet.get_worksheet(0)
            query = (
                select(
                    Response.user_mobile_number,
                    func.json_agg(
                        func.json_build_object(
                            SheetsMetadata.question_column, Answer.answer
                        )
                    ).label("response"),
                )
                .select_from(
                    Response.__table__.join(Answer).join(Question).join(SheetsMetadata)
                )
                .group_by(Response.id)
                .where(Response.id == response_id)
            )
            values = ["" for _ in range(worksheet.col_count)]
            response = session.execute(query).fetchone()
            values[0] = response.user_mobile_number
            for r in response.response:
                keys = list(r.keys())
                values[int(keys[0]) - 1] = r[keys[0]]
            worksheet.append_row(values)
            worksheet.columns_auto_resize(0, worksheet.col_count)
            write_log(f"Google Sheets updated, Content: {values}")

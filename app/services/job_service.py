from sqlalchemy.sql.expression import select
from sqlalchemy.sql.functions import func

from app.db import SessionLocal
from app.models import Answer, Question, Response
from app.schemas import TriggerEnum
from app.utils import write_log


class JobService:
    @classmethod
    def run_job(cls, job, response_id):
        try:
            if job.trigger == TriggerEnum.RECEIPT_SMS:
                cls.send_receipt_sms(response_id)
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

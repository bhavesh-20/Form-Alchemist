from datetime import datetime

from sqlalchemy.sql import select

from app import db
from app.db import SessionLocal
from app.models import Form, Job, Pipeline, Response
from app.schemas import TriggerEnum, UserResponse
from app.utils import write_log

from .job_service import JobService


class PipelineService:
    @classmethod
    def create_pipeline(cls, response_id):
        with SessionLocal() as session:
            try:
                response_id = str(response_id)
                pipeline = Pipeline(response_id=response_id)
                session.add(pipeline)
                session.flush()

                jobs = []
                for trigger in TriggerEnum.__members__:
                    jobs.append(Job(trigger=trigger, pipeline_id=pipeline.id))

                session.bulk_save_objects(jobs)
                session.commit()
                write_log(f"Pipeline created with id: {pipeline.id}")
                return pipeline
            except Exception as e:
                write_log(f"Error creating pipeline: {e}")
                return None

    @classmethod
    def run_pipelines(cls):
        with SessionLocal() as session:
            pipelines = (
                session.query(Pipeline)
                .filter(Pipeline.status != "finished")
                .order_by(Pipeline.created_at.asc())
                .limit(5)
                .all()
            )
            for pipeline in pipelines:
                pipeline.status = "running"
                session.commit()
                write_log(f"Pipeline {pipeline.id} is running")
                jobs = (
                    session.query(Job)
                    .filter(Job.pipeline_id == pipeline.id, Job.status == "pending")
                    .all()
                )
                for job in jobs:
                    JobService.run_job(job, str(pipeline.response_id))
                pipeline.status = "finished"
                pipeline.finished_at = datetime.now()
                session.commit()
                write_log(f"Pipeline {pipeline.id} is finished")

    @classmethod
    async def get_pipeline_by_id(cls, pipeline_id: str, user: UserResponse):
        pipeline = await db.fetch_all(
            select([Pipeline, Job])
            .select_from(Pipeline.__table__.join(Job))
            .where(Pipeline.id == pipeline_id)
        )
        pipelines = await cls.format_pipelines(pipeline)
        return pipelines[0]

    @classmethod
    async def get_pipelines(cls, form_id: str, limit: int, user: UserResponse):
        pipelines = await db.fetch_all(
            select([Pipeline, Job])
            .select_from(Pipeline.__table__.join(Job).join(Response).join(Form))
            .where(Form.id == form_id)
            .limit(limit)
        )
        return await cls.format_pipelines(pipelines)

    @classmethod
    async def format_pipelines(cls, data):
        pipelines = {}
        for record in data:
            if record.id not in pipelines:
                pipelines[record.id] = {
                    "id": record.id,
                    "status": record.status,
                    "created_at": record.created_at,
                    "finished_at": record.finished_at,
                    "jobs": [],
                }
            pipelines[record.id]["jobs"].append(
                {
                    "id": record.id_1,
                    "trigger": record.trigger,
                    "status": record.status_1,
                    "created_at": record.created_at_1,
                }
            )
        return [val for _, val in pipelines.items()]

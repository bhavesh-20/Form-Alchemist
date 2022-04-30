from datetime import datetime

from app.db import SessionLocal
from app.models import Job, Pipeline
from app.schemas import TriggerEnum
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

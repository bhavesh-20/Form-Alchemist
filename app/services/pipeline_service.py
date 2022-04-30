from app.db import SessionLocal
from app.models import Job, Pipeline
from app.schemas import TriggerEnum


class PipelineService:
    @classmethod
    def create_pipeline(cls, response_id):
        with SessionLocal() as session:
            response_id = str(response_id)
            pipeline = Pipeline(response_id=response_id)
            session.add(pipeline)
            session.flush()

            jobs = []
            for trigger in TriggerEnum.__members__:
                jobs.append(Job(trigger=trigger, pipeline_id=pipeline.id))

            session.bulk_save_objects(jobs)
            session.commit()
            print(f"Pipeline created with id: {pipeline.id}")
            return pipeline

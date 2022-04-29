from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String

from app.db import Base
from app.schemas import TriggerEnum


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid4().hex))
    pipeline_id = Column(String, ForeignKey("pipelines.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False, server_default="pending")
    trigger = Column(Enum(TriggerEnum), nullable=False)

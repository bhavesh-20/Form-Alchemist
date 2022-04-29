from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from app.db import Base
from app.schemas import TriggerEnum


class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()")
    )
    pipeline_id = Column(
        UUID(as_uuid=False),
        ForeignKey("pipelines.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime, server_default=func.now())
    status = Column(String, nullable=False, server_default="pending")
    trigger = Column(Enum(TriggerEnum), nullable=False)

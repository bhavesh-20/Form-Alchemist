from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from app.db import Base


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(
        UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()")
    )
    response_id = Column(
        UUID(as_uuid=False),
        ForeignKey("responses.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(DateTime, server_default=func.now())
    status = Column(String, nullable=False, server_default="pending")
    finished_at = Column(DateTime, nullable=True)

    jobs = relationship("Job", cascade="all, delete", backref="pipelines")

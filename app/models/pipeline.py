from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db import Base


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(String, primary_key=True, default=lambda: str(uuid4().hex))
    response_id = Column(String, ForeignKey("responses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False, server_default="pending")
    finished_at = Column(DateTime, nullable=True)

    jobs = relationship("Job", cascade="all, delete", backref="pipelines")

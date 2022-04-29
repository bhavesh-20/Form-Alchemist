from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db import Base


class Response(Base):
    __tablename__ = "responses"
    id = Column(String, primary_key=True, default=lambda: str(uuid4().hex))
    form_id = Column(String, ForeignKey("forms.id"), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)

    answers = relationship("Answer", cascade="all, delete", backref="responses")
    pipelines = relationship("Pipeline", cascade="all, delete", backref="responses")

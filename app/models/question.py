from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db import Base


class Question(Base):
    __tablename__ = "questions"
    id = Column(String, primary_key=True, default=lambda: str(uuid4().hex))
    form_id = Column(String, ForeignKey("forms.id"), nullable=False)
    question = Column(String, nullable=False)
    is_required = Column(Boolean, server_default="0")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    answers = relationship("Answer", cascade="all, delete", backref="questions")

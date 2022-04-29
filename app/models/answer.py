from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String

from app.db import Base


class Answer(Base):
    __tablename__ = "answers"
    id = Column(String, primary_key=True, default=lambda: str(uuid4().hex))
    response_id = Column(String, ForeignKey("responses.id"), nullable=False)
    question_id = Column(String, ForeignKey("questions.id"), nullable=False)
    answer = Column(String, nullable=False, server_default="")
    created_at = Column(DateTime, default=datetime.utcnow)

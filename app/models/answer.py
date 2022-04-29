from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from app.db import Base


class Answer(Base):
    __tablename__ = "answers"
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    response_id = Column(UUID(as_uuid=True), ForeignKey("responses.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    answer = Column(String, nullable=False, server_default="")
    created_at = Column(DateTime, server_default=func.now())

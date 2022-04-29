from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from app.db import Base


class Answer(Base):
    __tablename__ = "answers"
    id = Column(
        UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()")
    )
    response_id = Column(
        UUID(as_uuid=False),
        ForeignKey("responses.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_id = Column(
        UUID(as_uuid=False),
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    answer = Column(String, nullable=False, server_default="")
    created_at = Column(DateTime, server_default=func.now())

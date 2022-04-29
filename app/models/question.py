from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from app.db import Base


class Question(Base):
    __tablename__ = "questions"
    id = Column(
        UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()")
    )
    form_id = Column(UUID(as_uuid=False), ForeignKey("forms.id"), nullable=False)
    question = Column(String, nullable=False)
    is_required = Column(Boolean, server_default="0")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    answers = relationship("Answer", cascade="all, delete", backref="questions")

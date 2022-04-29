from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from app.db import Base


class Form(Base):
    __tablename__ = "forms"
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    multiple_submissions_allowed = Column(Boolean, server_default="0")
    open_till = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    questions = relationship("Question", cascade="all, delete", backref="forms")
    responses = relationship("Response", cascade="all, delete", backref="forms")

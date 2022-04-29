from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from app.db import Base


class Form(Base):
    __tablename__ = "forms"
    id = Column(
        UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()")
    )
    owner_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)

    multiple_submissions_allowed = Column(Boolean, server_default="0")
    open_till = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    questions = relationship("Question", cascade="all, delete", backref="forms")
    responses = relationship("Response", cascade="all, delete", backref="forms")

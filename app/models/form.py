from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db import Base


class Form(Base):
    __tablename__ = "forms"
    id = Column(String, primary_key=True, server_default=str(uuid4().hex))
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)

    multiple_submissions_allowed = Column(Boolean, server_default="0")
    open_till = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("Question", cascade="all, delete", backref="forms")
    responses = relationship("Response", cascade="all, delete", backref="forms")

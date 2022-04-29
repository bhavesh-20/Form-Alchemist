from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from app.db import Base


class Response(Base):
    __tablename__ = "responses"
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    form_id = Column(UUID(as_uuid=True), ForeignKey("forms.id"), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())

    answers = relationship("Answer", cascade="all, delete", backref="responses")
    pipelines = relationship("Pipeline", cascade="all, delete", backref="responses")

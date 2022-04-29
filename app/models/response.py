from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from app.db import Base


class Response(Base):
    __tablename__ = "responses"
    id = Column(
        UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()")
    )
    form_id = Column(UUID(as_uuid=False), ForeignKey("forms.id"), nullable=False)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    answers = relationship("Answer", cascade="all, delete", backref="responses")
    pipelines = relationship("Pipeline", cascade="all, delete", backref="responses")

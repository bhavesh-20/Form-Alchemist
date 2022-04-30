from sqlalchemy import Column, DateTime, ForeignKey, String
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
    form_id = Column(
        UUID(as_uuid=False), ForeignKey("forms.id", ondelete="CASCADE"), nullable=False
    )
    user_mobile_number = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    answers = relationship("Answer", cascade="all, delete", backref="responses")
    pipelines = relationship("Pipeline", cascade="all, delete", backref="responses")

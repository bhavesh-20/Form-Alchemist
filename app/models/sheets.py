from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class SheetsMetadata(Base):
    __tablename__ = "sheets_metadata"
    id = Column(Integer, primary_key=True, autoincrement=True)
    form_id = Column(
        UUID(as_uuid=False), ForeignKey("forms.id", ondelete="CASCADE"), nullable=False
    )
    question_id = Column(
        UUID(as_uuid=False),
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_column = Column(Integer, nullable=False)

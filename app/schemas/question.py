from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: UUID
    form_id: UUID
    question: str
    is_required: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class QuestionMetadata(BaseModel):
    question: str
    is_required: bool


class QuestionsResponse(BaseModel):
    questions: Optional[List[QuestionResponse]] = []

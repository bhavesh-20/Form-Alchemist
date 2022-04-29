from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class AnswerResponse(BaseModel):
    response_id: UUID
    answer: str


class AnswersResponse(BaseModel):
    question: str
    answers: Optional[List[AnswerResponse]] = []

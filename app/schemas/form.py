from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class FormMetadata(BaseModel):
    title: str
    description: str


class FormResponse(BaseModel):
    id: UUID
    title: str
    description: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class FormCreateResponse(BaseModel):
    message: str
    form_id: UUID

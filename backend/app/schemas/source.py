from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from backend.app.schemas.common import SourceType


class SourceCreate(BaseModel):
    source_type: SourceType
    title: str | None = Field(default=None, max_length=500)
    content: str = Field(min_length=1)
    metadata: dict = Field(default_factory=dict)


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_type: SourceType
    title: str | None
    content: str
    metadata: dict
    created_at: datetime
    updated_at: datetime
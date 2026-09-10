from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from backend.app.schemas.common import OutputStatus, OutputType


class OutputDraftCreate(BaseModel):
    job_id: UUID
    output_type: OutputType
    version: int = Field(default=1, ge=1)
    content: str = Field(min_length=1)
    status: OutputStatus = OutputStatus.DRAFT
    quality_metadata: dict = Field(default_factory=dict)


class OutputDraftRead(BaseModel):
    id: UUID
    job_id: UUID
    output_type: OutputType
    version: int
    content: str
    status: OutputStatus
    quality_metadata: dict
    created_at: datetime
    updated_at: datetime
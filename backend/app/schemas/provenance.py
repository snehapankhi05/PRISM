from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProvenanceLinkCreate(BaseModel):
    output_draft_id: UUID
    source_id: UUID
    source_reference: str = Field(min_length=1)
    claim_reference: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)


class ProvenanceLinkRead(BaseModel):
    id: UUID
    output_draft_id: UUID
    source_id: UUID
    source_reference: str
    claim_reference: str
    confidence: float
    created_at: datetime
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Fact(BaseModel):
    id: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    predicate: str = Field(min_length=1)
    object: str = Field(min_length=1)
    source_reference: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)


class FactGraphData(BaseModel):
    facts: list[Fact] = Field(default_factory=list)


class FactGraphCreate(BaseModel):
    source_id: UUID
    version: int = Field(ge=1)
    graph_data: FactGraphData
    extraction_metadata: dict = Field(default_factory=dict)


class FactGraphRead(BaseModel):
    id: UUID
    source_id: UUID
    version: int
    graph_data: FactGraphData
    extraction_metadata: dict
    created_at: datetime
    updated_at: datetime
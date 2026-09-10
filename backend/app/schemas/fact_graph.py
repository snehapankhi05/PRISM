from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Fact(BaseModel):
    id: str = Field(min_length=1)
    category: str = Field(
        min_length=1,
        max_length=100,
    )
    subject: str = Field(min_length=1)
    predicate: str = Field(min_length=1)
    object: str = Field(min_length=1)
    source_reference: str = Field(min_length=1)
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )
    valid_from: str | None = None
    valid_to: str | None = None
    uncertainty: str | None = None
class FactGraphData(BaseModel):
    facts: list[Fact] = Field(
        default_factory=list,
    )
class FactGraphExtractionResult(BaseModel):
    schema_version: str = "1.0"
    facts: list[Fact] = Field(default_factory=list)
    extraction_method: str = Field(
        default="llm",
        min_length=1,
    )
    extraction_confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )


class FactGraphCreate(BaseModel):
    source_id: UUID
    version: int = Field(
        ge=1,
    )
    graph_data: FactGraphData
    extraction_metadata: dict = Field(
        default_factory=dict,
    )


class FactGraphRead(BaseModel):
    id: UUID
    source_id: UUID
    version: int
    graph_data: FactGraphData
    extraction_metadata: dict
    created_at: datetime
    updated_at: datetime
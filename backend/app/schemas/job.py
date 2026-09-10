from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from backend.app.schemas.common import JobStatus, OutputType
from backend.app.schemas.controls import GenerationControls


class JobCreate(BaseModel):
    source_id: UUID
    fact_graph_id: UUID
    controls: GenerationControls
    output_types: list[OutputType] = Field(min_length=1)


class JobRead(BaseModel):
    id: UUID
    source_id: UUID
    fact_graph_id: UUID
    status: JobStatus
    controls: GenerationControls
    created_at: datetime
    updated_at: datetime
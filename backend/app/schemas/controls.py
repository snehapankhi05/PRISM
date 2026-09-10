from pydantic import BaseModel, Field


class GenerationControls(BaseModel):
    target_audience: str = Field(min_length=1, max_length=500)
    tone: str = Field(min_length=1, max_length=100)
    language: str = Field(default="English", min_length=1, max_length=100)
    level_of_detail: str = Field(min_length=1, max_length=100)
    communication_objective: str = Field(min_length=1, max_length=500)
    content_style: str = Field(min_length=1, max_length=200)
from pydantic import BaseModel, Field


class PresentationSlide(BaseModel):
    slide_number: int = Field(ge=1)
    title: str = Field(min_length=1)
    content: list[str] = Field(min_length=1)
    source_references: list[str] = Field(default_factory=list)


class PresentationContent(BaseModel):
    title: str = Field(min_length=1)
    slides: list[PresentationSlide] = Field(min_length=1)


class InfographicSection(BaseModel):
    heading: str = Field(min_length=1)
    key_points: list[str] = Field(min_length=1)
    source_references: list[str] = Field(default_factory=list)


class InfographicContent(BaseModel):
    title: str = Field(min_length=1)
    subtitle: str = ""
    sections: list[InfographicSection] = Field(min_length=1)


class VideoScene(BaseModel):
    scene_number: int = Field(ge=1)
    title: str = Field(min_length=1)
    on_screen_text: str = Field(min_length=1)
    narration: str = Field(min_length=1)
    visual_direction: str = Field(min_length=1)
    source_references: list[str] = Field(default_factory=list)


class VideoContent(BaseModel):
    title: str = Field(min_length=1)
    scenes: list[VideoScene] = Field(min_length=1)
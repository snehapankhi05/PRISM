from pydantic import BaseModel, Field


class PresentationSlide(BaseModel):
    slide_number: int = Field(ge=1)
    title: str = Field(min_length=1, max_length=120)
    subtitle: str = ""
    content: list[str] = Field(min_length=1, max_length=6)
    key_stat: str | None = None
    speaker_notes: str = ""
    source_references: list[str] = Field(default_factory=list)


class PresentationContent(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    subtitle: str = ""
    audience: str = ""
    slides: list[PresentationSlide] = Field(
        min_length=6,
        max_length=10,
    )


class InfographicMetric(BaseModel):
    label: str = Field(min_length=1, max_length=80)
    value: str = Field(min_length=1, max_length=60)
    explanation: str = ""
    source_references: list[str] = Field(default_factory=list)


class InfographicTimelineItem(BaseModel):
    time: str = Field(min_length=1, max_length=60)
    event: str = Field(min_length=1, max_length=160)
    source_references: list[str] = Field(default_factory=list)


class InfographicSection(BaseModel):
    heading: str = Field(min_length=1, max_length=100)
    key_points: list[str] = Field(min_length=1, max_length=5)
    source_references: list[str] = Field(default_factory=list)


class InfographicContent(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    subtitle: str = ""
    headline_metrics: list[InfographicMetric] = Field(
        default_factory=list,
        max_length=6,
    )
    timeline: list[InfographicTimelineItem] = Field(
        default_factory=list,
        max_length=8,
    )
    sections: list[InfographicSection] = Field(
        min_length=1,
        max_length=6,
    )
    footer_note: str = ""


class VideoScene(BaseModel):
    scene_number: int = Field(ge=1)
    duration_seconds: int = Field(ge=4, le=30)

    title: str = Field(min_length=1, max_length=120)

    video_prompt: str = Field(
        min_length=20,
        max_length=1200,
    )

    character_description: str = Field(
        min_length=1,
        max_length=500,
    )

    environment: str = Field(
        min_length=1,
        max_length=500,
    )

    camera_direction: str = Field(
        min_length=1,
        max_length=500,
    )

    action: str = Field(
        min_length=1,
        max_length=500,
    )

    on_screen_text: str = Field(
        min_length=1,
        max_length=300,
    )

    narration: str = Field(
        min_length=1,
        max_length=700,
    )

    negative_prompt: str = Field(
        min_length=1,
        max_length=500,
    )

    source_references: list[str] = Field(
        default_factory=list,
    )


class VideoContent(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    description: str = ""
    total_duration_seconds: int = Field(ge=20, le=300)
    scenes: list[VideoScene] = Field(
        min_length=4,
        max_length=10,
    )


class ExecutiveSummaryContent(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    overview: str = Field(min_length=1, max_length=1200)

    key_findings: list[str] = Field(
        min_length=2,
        max_length=6,
    )

    impact: str = Field(min_length=1, max_length=1000)

    response: list[str] = Field(
        min_length=1,
        max_length=5,
    )

    recommendations: list[str] = Field(
        default_factory=list,
        max_length=6,
    )

    source_references: list[str] = Field(
        default_factory=list,
    )
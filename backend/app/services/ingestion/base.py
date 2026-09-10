from dataclasses import dataclass, field


@dataclass(slots=True)
class IngestionResult:
    content: str
    source_type: str
    title: str | None = None
    metadata: dict = field(default_factory=dict)
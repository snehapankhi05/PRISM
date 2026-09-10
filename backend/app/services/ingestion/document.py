from dataclasses import dataclass, field


@dataclass(slots=True)
class DocumentSection:
    section_id: str
    content: str
    source_reference: str


@dataclass(slots=True)
class NormalizedDocument:
    content: str
    source_type: str
    title: str | None
    sections: list[DocumentSection] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
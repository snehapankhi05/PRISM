from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class RenderedResult:
    output_type: str
    file_path: Path
    mime_type: str
    metadata: dict = field(default_factory=dict)


class Renderer(ABC):
    output_type: str

    @abstractmethod
    def render(self, content, output_dir: Path) -> RenderedResult:
        raise NotImplementedError
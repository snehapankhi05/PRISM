from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from backend.app.schemas.controls import GenerationControls
from backend.app.services.knowledge.context import KnowledgeContext


@dataclass(slots=True)
class SpecialistInput:
    knowledge_context: KnowledgeContext
    controls: GenerationControls


@dataclass(slots=True)
class SpecialistOutput:
    output_type: str
    content: object
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        content = self.content

        if hasattr(content, "model_dump"):
            content = content.model_dump()

        return {
            "output_type": self.output_type,
            "content": content,
            "metadata": self.metadata,
        }


class SpecialistAgent(ABC):
    output_type: str

    @abstractmethod
    def generate(
        self,
        input_data: SpecialistInput,
    ) -> SpecialistOutput:
        raise NotImplementedError
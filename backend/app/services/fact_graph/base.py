from abc import ABC, abstractmethod

from backend.app.schemas.fact_graph import FactGraphExtractionResult
from backend.app.services.ingestion.document import NormalizedDocument


class FactGraphExtractor(ABC):
    @abstractmethod
    def extract(self, document: NormalizedDocument) -> FactGraphExtractionResult:
        """Extract a structured Fact Graph from a normalized document."""
        raise NotImplementedError
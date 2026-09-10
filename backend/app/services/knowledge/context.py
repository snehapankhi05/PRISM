from dataclasses import dataclass

from backend.app.schemas.fact_graph import Fact
from backend.app.services.rag.base import RetrievalResult


@dataclass(slots=True)
class KnowledgeContext:
    facts: list[Fact]
    evidence: list[RetrievalResult]
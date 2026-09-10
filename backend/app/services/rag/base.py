from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class RetrievalResult:
    chunk_id: str
    content: str
    source_reference: str
    score: float
    metadata: dict


class EmbeddingProvider(ABC):

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        raise NotImplementedError


class Retriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        query: str,
        *,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        raise NotImplementedError
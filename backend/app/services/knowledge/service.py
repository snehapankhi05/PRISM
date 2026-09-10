from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.schemas.fact_graph import Fact, FactGraphData
from backend.app.services.fact_graph.repository import FactGraphRepository
from backend.app.services.knowledge.context import KnowledgeContext
from backend.app.services.rag.base import Retriever


class KnowledgeService:
    def __init__(
        self,
        fact_graph_repository: FactGraphRepository,
        retriever: Retriever,
    ):
        self.fact_graph_repository = fact_graph_repository
        self.retriever = retriever

    def build_context(
        self,
        db: Session,
        *,
        source_id: UUID,
        query: str,
        top_k: int = 5,
    ) -> KnowledgeContext:
        fact_graph = self.fact_graph_repository.get_latest(
            db,
            source_id,
        )

        if fact_graph is None:
            raise ValueError(
                "No Fact Graph exists for this source."
            )

        graph_data = FactGraphData.model_validate(
            fact_graph.graph_data
        )

        facts: list[Fact] = graph_data.facts

        evidence = self.retriever.retrieve(
            query,
            top_k=top_k,
        )

        return KnowledgeContext(
            facts=facts,
            evidence=evidence,
        )
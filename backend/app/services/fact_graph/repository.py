from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models import FactGraph


class FactGraphRepository:
    def create(
        self,
        db: Session,
        *,
        source_id: UUID,
        graph_data: dict,
        extraction_metadata: dict,
    ) -> FactGraph:
        latest_version = db.scalar(
            select(FactGraph.version)
            .where(FactGraph.source_id == source_id)
            .order_by(FactGraph.version.desc())
            .limit(1)
        )

        next_version = (latest_version or 0) + 1

        fact_graph = FactGraph(
            source_id=source_id,
            version=next_version,
            graph_data=graph_data,
            extraction_metadata=extraction_metadata,
        )

        db.add(fact_graph)
        db.flush()

        return fact_graph
    
    def get_by_id(
        self,
        db: Session,
        fact_graph_id: UUID,
    ) -> FactGraph | None:
        return db.scalar(
            select(FactGraph).where(
                FactGraph.id == fact_graph_id
            )
        )

    def get_version(
        self,
        db: Session,
        source_id: UUID,
        version: int,
    ) -> FactGraph | None:
        return db.scalar(
            select(FactGraph)
            .where(
                FactGraph.source_id == source_id,
                FactGraph.version == version,
            )
        )

    def get_latest(
        self,
        db: Session,
        source_id: UUID,
    ) -> FactGraph | None:
        return db.scalar(
            select(FactGraph)
            .where(FactGraph.source_id == source_id)
            .order_by(FactGraph.version.desc())
            .limit(1)
        )
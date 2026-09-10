from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.models import FactGraph
from backend.app.schemas.fact_graph import FactGraphExtractionResult
from backend.app.services.fact_graph.base import FactGraphExtractor
from backend.app.services.fact_graph.repository import FactGraphRepository
from backend.app.services.ingestion.document import NormalizedDocument


class FactGraphService:
    def __init__(
        self,
        extractor: FactGraphExtractionResult,
        repository: FactGraphRepository,
    ):
        self.extractor = extractor
        self.repository = repository

    def create(
        self,
        db: Session,
        *,
        source_id: UUID,
        document: NormalizedDocument,
    ) -> FactGraph:
        extracted = self.extractor.extract(document)
        if not extracted.facts:
            raise ValueError("Fact Graph extraction returned no facts.")


        return self.repository.create(
            db,
            source_id=source_id,
            graph_data=extracted.model_dump(),
            extraction_metadata={
                "method": extracted.extraction_method,
                "schema_version": extracted.schema_version,
                "extraction_confidence": extracted.extraction_confidence,
},
        )
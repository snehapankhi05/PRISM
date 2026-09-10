from backend.app.schemas.fact_graph import FactGraphData
from backend.app.services.ingestion.document import NormalizedDocument
from backend.app.services.fact_graph.base import FactGraphExtractor


class DeterministicFactGraphExtractor(FactGraphExtractor):
    def extract(self, document: NormalizedDocument) -> FactGraphData:
        return FactGraphData(facts=[])
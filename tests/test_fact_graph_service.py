from backend.app.core.config import settings
from backend.app.db.session import SessionLocal
from backend.app.models import Source
from backend.app.services.fact_graph.llm import LLMFactGraphExtractor
from backend.app.services.fact_graph.repository import FactGraphRepository
from backend.app.services.fact_graph.service import FactGraphService
from backend.app.services.ingestion.document import DocumentSection, NormalizedDocument
from backend.app.services.llm import GroqLLMProvider


def main():
    db = SessionLocal()

    try:
        source = Source(
    source_type="text",
    title="PRISM Fact Graph Integration Test",
    content="The incident affected 310 customers.",
    source_metadata={},
)

        db.add(source)
        db.flush()

        document = NormalizedDocument(
    content="The incident affected 310 customers.",
    source_type="text",
    title="PRISM Fact Graph Integration Test",
    sections=[
        DocumentSection(
            section_id="section-1",
            content="The incident affected 310 customers.",
            source_reference="text:section-1",
        )
    ],
)

        provider = GroqLLMProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )

        extractor = LLMFactGraphExtractor(provider)
        repository = FactGraphRepository()
        service = FactGraphService(extractor, repository)

        graph = service.create(
            db,
            source_id=source.id,
            document=document,
        )

        db.commit()

        print("Fact Graph service successful.")
        print(f"Graph Version: {graph.version}")
        print(f"Facts: {graph.graph_data}")
        print(f"Metadata: {graph.extraction_metadata}")

        db.delete(source)
        db.commit()

        print("Test data cleaned up.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
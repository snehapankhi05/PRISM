from backend.app.core.config import settings
from backend.app.db.session import SessionLocal
from backend.app.models import Source
from backend.app.services.fact_graph.llm import LLMFactGraphExtractor
from backend.app.services.fact_graph.repository import FactGraphRepository
from backend.app.services.fact_graph.service import FactGraphService
from backend.app.services.ingestion.document import (
    DocumentSection,
    NormalizedDocument,
)
from backend.app.services.knowledge.service import KnowledgeService
from backend.app.services.llm import GroqLLMProvider
from backend.app.services.rag.chroma import ChromaVectorStore
from backend.app.services.rag.embeddings import LocalEmbeddingProvider
from backend.app.services.rag.indexer import RAGIndexer
from backend.app.services.rag.retriever import ChromaRetriever


def main():
    db = SessionLocal()

    try:
        # -----------------------------------------------------
        # 1. Source
        # -----------------------------------------------------
        source = Source(
            source_type="text",
            title="PRISM Knowledge Integration Test",
            content=(
                "The incident affected 310 customers. "
                "The incident occurred on September 3, 2026."
            ),
            source_metadata={},
        )

        db.add(source)
        db.flush()

        # -----------------------------------------------------
        # 2. Normalized document
        # -----------------------------------------------------
        document = NormalizedDocument(
            content=(
                "The incident affected 310 customers. "
                "The incident occurred on September 3, 2026."
            ),
            source_type="text",
            title="PRISM Knowledge Integration Test",
            sections=[
                DocumentSection(
                    section_id="knowledge-test-section-1",
                    content="The incident affected 310 customers.",
                    source_reference="text:section-1",
                ),
                DocumentSection(
                    section_id="knowledge-test-section-2",
                    content="The incident occurred on September 3, 2026.",
                    source_reference="text:section-2",
                ),
            ],
        )

        # -----------------------------------------------------
        # 3. Fact Graph
        # -----------------------------------------------------
        provider = GroqLLMProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )

        extractor = LLMFactGraphExtractor(provider)
        fact_graph_repository = FactGraphRepository()

        fact_graph_service = FactGraphService(
            extractor,
            fact_graph_repository,
        )

        fact_graph = fact_graph_service.create(
            db,
            source_id=source.id,
            document=document,
        )

        # -----------------------------------------------------
        # 4. RAG
        # -----------------------------------------------------
        embeddings = LocalEmbeddingProvider()
        vector_store = ChromaVectorStore()

        indexer = RAGIndexer(
            embedding_provider=embeddings,
            vector_store=vector_store,
        )

        indexer.index(
    document,
    source_id=str(source.id),
)

        retriever = ChromaRetriever(
            vector_store=vector_store,
            embedding_provider=embeddings,
        )

        # -----------------------------------------------------
        # 5. Knowledge Service
        # -----------------------------------------------------
        knowledge_service = KnowledgeService(
            fact_graph_repository=fact_graph_repository,
            retriever=retriever,
        )

        context = knowledge_service.build_context(
            db,
            source_id=source.id,
            query="How many customers were affected?",
            top_k=1,
        )

        db.commit()

        # -----------------------------------------------------
        # 6. Verify
        # -----------------------------------------------------
        print("Knowledge integration successful.")
        print(f"Fact Graph version: {fact_graph.version}")
        print(f"Facts found: {len(context.facts)}")
        print(f"Evidence found: {len(context.evidence)}")

        for fact in context.facts:
            print(f"Fact: {fact}")

        for evidence in context.evidence:
            print(f"Evidence: {evidence.content}")
            print(f"Source: {evidence.source_reference}")
            print(f"Distance: {evidence.score}")

        # -----------------------------------------------------
        # 7. Cleanup
        # -----------------------------------------------------
        db.delete(source)
        db.commit()

        print("Test data cleaned up.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
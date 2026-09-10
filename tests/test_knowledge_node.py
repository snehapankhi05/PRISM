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
from backend.app.services.orchestration.knowledge import knowledge_node
from backend.app.services.rag.chroma import ChromaVectorStore
from backend.app.services.rag.embeddings import LocalEmbeddingProvider
from backend.app.services.rag.indexer import RAGIndexer
from backend.app.services.rag.retriever import ChromaRetriever


def main():
    db = SessionLocal()

    try:
        source = Source(
            source_type="text",
            title="PRISM Knowledge Node Test",
            content="The incident affected 310 customers.",
            source_metadata={},
        )

        db.add(source)
        db.flush()

        document = NormalizedDocument(
            content="The incident affected 310 customers.",
            source_type="text",
            title="PRISM Knowledge Node Test",
            sections=[
                DocumentSection(
                    section_id="knowledge-node-section-1",
                    content="The incident affected 310 customers.",
                    source_reference="text:section-1",
                )
            ],
        )

        provider = GroqLLMProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )

        fact_graph_repository = FactGraphRepository()

        fact_graph_service = FactGraphService(
            LLMFactGraphExtractor(provider),
            fact_graph_repository,
        )

        fact_graph_service.create(
            db,
            source_id=source.id,
            document=document,
        )

        embeddings = LocalEmbeddingProvider()
        vector_store = ChromaVectorStore()

        RAGIndexer(
            embedding_provider=embeddings,
            vector_store=vector_store,
        ).index(document)

        retriever = ChromaRetriever(
            vector_store=vector_store,
            embedding_provider=embeddings,
        )

        knowledge_service = KnowledgeService(
            fact_graph_repository=fact_graph_repository,
            retriever=retriever,
        )

        state = {
            "source_id": str(source.id),
            "query": "How many customers were affected?",
        }

        result = knowledge_node(
            state,
            db=db,
            knowledge_service=knowledge_service,
        )

        context = result["knowledge_context"]

        print("Knowledge node successful.")
        print(f"Facts: {len(context.facts)}")
        print(f"Evidence: {len(context.evidence)}")

        for fact in context.facts:
            print(f"Fact: {fact}")

        for evidence in context.evidence:
            print(f"Evidence: {evidence.content}")
            print(f"Source: {evidence.source_reference}")

        db.rollback()
        print("Test data rolled back.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
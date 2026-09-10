from backend.app.services.ingestion.document import (
    DocumentSection,
    NormalizedDocument,
)
from backend.app.services.rag.chroma import ChromaVectorStore
from backend.app.services.rag.embeddings import LocalEmbeddingProvider
from backend.app.services.rag.indexer import RAGIndexer
from backend.app.services.rag.retriever import ChromaRetriever


def main():
    # ---------------------------------------------------------
    # 1. Create a normalized multi-section document
    # ---------------------------------------------------------
    document = NormalizedDocument(
        content=(
            "The incident affected 310 customers. "
            "The incident occurred on September 3, 2026. "
            "All support credentials were rotated by 09:00 UTC."
        ),
        source_type="text",
        title="PRISM RAG Integration Test",
        sections=[
            DocumentSection(
                section_id="rag-test-section-1",
                content="The incident affected 310 customers.",
                source_reference="text:section-1",
            ),
            DocumentSection(
                section_id="rag-test-section-2",
                content="The incident occurred on September 3, 2026.",
                source_reference="text:section-2",
            ),
            DocumentSection(
                section_id="rag-test-section-3",
                content="All support credentials were rotated by 09:00 UTC.",
                source_reference="text:section-3",
            ),
        ],
    )

    # ---------------------------------------------------------
    # 2. Initialize embedding provider and vector store
    # ---------------------------------------------------------
    embeddings = LocalEmbeddingProvider()
    vector_store = ChromaVectorStore()

    # ---------------------------------------------------------
    # 3. Index the document
    # ---------------------------------------------------------
    indexer = RAGIndexer(
        embedding_provider=embeddings,
        vector_store=vector_store,
    )

    indexer.index(document)

    # ---------------------------------------------------------
    # 4. Initialize retriever
    # ---------------------------------------------------------
    retriever = ChromaRetriever(
        vector_store=vector_store,
        embedding_provider=embeddings,
    )

    # ---------------------------------------------------------
    # 5. Test customer-impact retrieval
    # ---------------------------------------------------------
    results = retriever.retrieve(
        "How many customers were affected?",
        top_k=1,
    )

    print("Customer query:")
    print(f"Results: {len(results)}")

    for result in results:
        print(f"Content: {result.content}")
        print(f"Source: {result.source_reference}")
        print(f"Score: {result.score}")

    # ---------------------------------------------------------
    # 6. Test date retrieval
    # ---------------------------------------------------------
    results = retriever.retrieve(
        "When did the incident occur?",
        top_k=1,
    )

    print("\nDate query:")
    print(f"Results: {len(results)}")

    for result in results:
        print(f"Content: {result.content}")
        print(f"Source: {result.source_reference}")
        print(f"Score: {result.score}")

    # ---------------------------------------------------------
    # 7. Test credential retrieval
    # ---------------------------------------------------------
    results = retriever.retrieve(
        "When were the support credentials rotated?",
        top_k=1,
    )

    print("\nCredential query:")
    print(f"Results: {len(results)}")

    for result in results:
        print(f"Content: {result.content}")
        print(f"Source: {result.source_reference}")
        print(f"Score: {result.score}")

    # ---------------------------------------------------------
    # 8. Test empty query validation
    # ---------------------------------------------------------
    empty_results = retriever.retrieve("   ")

    print("\nEmpty query:")
    print(f"Results: {empty_results}")

    # ---------------------------------------------------------
    # 9. Test top_k validation
    # ---------------------------------------------------------
    try:
        retriever.retrieve(
            "customer impact",
            top_k=0,
        )
    except ValueError as exc:
        print("\ntop_k validation successful:")
        print(exc)

    # ---------------------------------------------------------
    # 10. Final status
    # ---------------------------------------------------------
    print("\nRAG integration test completed successfully.")


if __name__ == "__main__":
    main()
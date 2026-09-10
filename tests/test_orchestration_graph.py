from uuid import uuid4

from backend.app.models import Source
from backend.app.schemas.fact_graph import Fact, FactGraphData
from backend.app.services.fact_graph.repository import FactGraphRepository
from backend.app.services.ingestion.document import (
    DocumentSection,
    NormalizedDocument,
)
from backend.app.services.knowledge.service import KnowledgeService
from backend.app.services.llm.mock import MockLLMProvider
from backend.app.services.orchestration.graph import build_prism_graph
from backend.app.services.orchestration.runtime import PRISMRuntime
from backend.app.services.rag.chroma import ChromaVectorStore
from backend.app.services.rag.embeddings import LocalEmbeddingProvider
from backend.app.services.rag.indexer import RAGIndexer
from backend.app.services.rag.retriever import ChromaRetriever
from backend.app.services.orchestration.controls import ControlResolver
from backend.app.schemas.controls import GenerationControls
from backend.app.services.orchestration.specialists.linkedin import LinkedInSpecialist
from backend.app.services.orchestration.specialists.registry import SpecialistRegistry
from backend.app.services.llm.mock import MockLLMProvider
from backend.app.services.orchestration.specialists.factory import (
    build_specialist_registry,
)

def test_prism_langgraph_integration(db_session):
    # ---------------------------------------------------------
    # 1. Create source
    # ---------------------------------------------------------
    source = Source(
        source_type="text",
        title="LangGraph Test",
        content="The incident affected 310 customers.",
        source_metadata={},
    )

    db_session.add(source)
    db_session.flush()

    # ---------------------------------------------------------
    # 2. Create Fact Graph for the source
    # ---------------------------------------------------------
    fact_graph_repository = FactGraphRepository()

    graph_data = FactGraphData(
        facts=[
            Fact(
                id="fact-1",
                category="Incident Impact",
                subject="incident",
                predicate="affected",
                object="310 customers",
                source_reference="paragraph-1",
                confidence=1.0,
            )
        ]
    )

    fact_graph = fact_graph_repository.create(
        db_session,
        source_id=source.id,
        graph_data=graph_data.model_dump(),
        extraction_metadata={
            "method": "test",
            "schema_version": "1.0",
            "extraction_confidence": 1.0,
        },
    )

    assert fact_graph.version == 1

    # ---------------------------------------------------------
    # 3. Create normalized document
    # ---------------------------------------------------------
    document = NormalizedDocument(
        content=source.content,
        source_type="text",
        title=source.title,
        sections=[
            DocumentSection(
                section_id=f"test-{uuid4()}",
                content=source.content,
                source_reference="paragraph-1",
            )
        ],
    )

    # ---------------------------------------------------------
    # 4. Create RAG components
    # ---------------------------------------------------------
    embedding_provider = LocalEmbeddingProvider()

    vector_store = ChromaVectorStore(
        path="data/chroma"
    )

    indexer = RAGIndexer(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    retriever = ChromaRetriever(
        vector_store=vector_store,
        embedding_provider=embedding_provider,
    )

    # ---------------------------------------------------------
    # 5. Index document into RAG
    # ---------------------------------------------------------
    indexer.index(document)

    # ---------------------------------------------------------
    # 6. Create KnowledgeService
    # ---------------------------------------------------------
    knowledge_service = KnowledgeService(
        fact_graph_repository=fact_graph_repository,
        retriever=retriever,
    )

    # ---------------------------------------------------------
    # 7. Create PRISM runtime
    # ---------------------------------------------------------
    linkedin_specialist = LinkedInSpecialist(
        provider=MockLLMProvider()
    )

    specialist_registry = SpecialistRegistry(
        specialists=[linkedin_specialist]
    )

    runtime = PRISMRuntime(
        db=db_session,
        knowledge_service=knowledge_service,
        control_resolver=ControlResolver(),
        specialist_registry=specialist_registry,
    )

    # ---------------------------------------------------------
    # 8. Build LangGraph
    # ---------------------------------------------------------
    graph = build_prism_graph(runtime)

    # ---------------------------------------------------------
    # 9. Invoke LangGraph
    # ---------------------------------------------------------
    result = graph.invoke(
    {
        "source_id": str(source.id),
        "query": "How many customers were affected?",
        "requested_outputs": ["linkedin"],
        "controls": GenerationControls(
            target_audience="General public",
            tone="Professional",
            language="English",
            level_of_detail="Concise",
            communication_objective="Inform the audience",
            content_style="Clear and factual",
        ),
    }
)

    # ---------------------------------------------------------
    # 10. Verify complete orchestration result
    # ---------------------------------------------------------
    assert "knowledge_context" in result

    knowledge_context = result["knowledge_context"]
    assert "controls" in result
    assert result["controls"].target_audience == "General public"
    assert result["controls"].tone == "Professional"
    assert result["controls"].language == "English"

    assert knowledge_context is not None

    # Fact Graph data reached LangGraph
    assert len(knowledge_context.facts) == 1
    assert knowledge_context.facts[0].object == "310 customers"

    # RAG evidence reached LangGraph
    assert len(knowledge_context.evidence) > 0

    assert any(
        "310 customers" in evidence.content
        for evidence in knowledge_context.evidence
    )

    db_session.rollback()


def test_prism_generates_multiple_outputs(db_session):
    # ---------------------------------------------------------
    # 1. Create source
    # ---------------------------------------------------------
    source = Source(
        source_type="text",
        title="Multi Output Test",
        content="The incident affected 310 customers.",
        source_metadata={},
    )

    db_session.add(source)
    db_session.flush()

    # ---------------------------------------------------------
    # 2. Create Fact Graph
    # ---------------------------------------------------------
    fact_graph_repository = FactGraphRepository()

    graph_data = FactGraphData(
        facts=[
            Fact(
                id="fact-1",
                category="Incident Impact",
                subject="incident",
                predicate="affected",
                object="310 customers",
                source_reference="paragraph-1",
                confidence=1.0,
            )
        ]
    )

    fact_graph_repository.create(
        db_session,
        source_id=source.id,
        graph_data=graph_data.model_dump(),
        extraction_metadata={
            "method": "test",
            "schema_version": "1.0",
            "extraction_confidence": 1.0,
        },
    )

    # ---------------------------------------------------------
    # 3. Create RAG
    # ---------------------------------------------------------
    embedding_provider = LocalEmbeddingProvider()

    vector_store = ChromaVectorStore(
        path="data/chroma"
    )

    indexer = RAGIndexer(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    retriever = ChromaRetriever(
        vector_store=vector_store,
        embedding_provider=embedding_provider,
    )

    document = NormalizedDocument(
        content=source.content,
        source_type="text",
        title=source.title,
        sections=[
            DocumentSection(
                section_id=f"test-{uuid4()}",
                content=source.content,
                source_reference="paragraph-1",
            )
        ],
    )

    indexer.index(document)

    # ---------------------------------------------------------
    # 4. Knowledge Service
    # ---------------------------------------------------------
    knowledge_service = KnowledgeService(
        fact_graph_repository=fact_graph_repository,
        retriever=retriever,
    )

    # ---------------------------------------------------------
    # 5. All specialists
    # ---------------------------------------------------------
    specialist_registry = build_specialist_registry(
        MockLLMProvider()
    )

    # ---------------------------------------------------------
    # 6. Runtime
    # ---------------------------------------------------------
    runtime = PRISMRuntime(
        db=db_session,
        knowledge_service=knowledge_service,
        control_resolver=ControlResolver(),
        specialist_registry=specialist_registry,
    )

    # ---------------------------------------------------------
    # 7. Build graph
    # ---------------------------------------------------------
    graph = build_prism_graph(runtime)

    # ---------------------------------------------------------
    # 8. Generate all outputs
    # ---------------------------------------------------------
    result = graph.invoke(
        {
            "source_id": str(source.id),
            "query": "incident impact and affected customers",
            "controls": GenerationControls(
                target_audience="General audience",
                tone="Professional",
                language="English",
                level_of_detail="Concise",
                communication_objective="Inform",
                content_style="Professional",
            ),
            "requested_outputs": [
                "linkedin",
                "twitter",
                "advisory",
                "executive_summary",
                "presentation",
                "infographic",
                "video",
            ],
        }
    )

    # ---------------------------------------------------------
    # 9. Verify
    # ---------------------------------------------------------
    outputs = result["generated_outputs"]

    assert len(outputs) == 7

    for output_type in [
        "linkedin",
        "twitter",
        "advisory",
        "executive_summary",
        "presentation",
        "infographic",
        "video",
    ]:
        assert output_type in outputs
        assert outputs[output_type].content
        assert outputs[output_type].output_type == output_type

    db_session.rollback()
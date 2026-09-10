from backend.app.models.job import Job
from backend.app.models.output_draft import OutputDraft
from backend.app.models.source import Source
from backend.app.services.fact_graph.repository import FactGraphRepository
from backend.app.schemas.fact_graph import Fact, FactGraphData
from backend.app.services.ingestion.document import (
    DocumentSection,
    NormalizedDocument,
)
from backend.app.services.knowledge.service import KnowledgeService
from backend.app.services.rag.embeddings import LocalEmbeddingProvider
from backend.app.services.rag.chroma import ChromaVectorStore
from backend.app.services.rag.indexer import RAGIndexer
from backend.app.services.rag.retriever import ChromaRetriever
from backend.app.services.orchestration.controls import ControlResolver
from backend.app.services.orchestration.runtime import PRISMRuntime
from backend.app.services.orchestration.specialists.factory import (
    build_specialist_registry,
)
from backend.app.services.llm.mock import MockLLMProvider
from backend.app.schemas.controls import GenerationControls
from backend.app.services.orchestration.graph import build_prism_graph


def test_generated_output_is_persisted(db_session):

    source = Source(
        source_type="text",
        title="Persistence Test",
        content="The incident affected 310 customers.",
        source_metadata={},
    )

    db_session.add(source)
    db_session.flush()

    fact_graph_repository = FactGraphRepository()

    fact_graph = fact_graph_repository.create(
        db_session,
        source_id=source.id,
        graph_data=FactGraphData(
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
        ).model_dump(),
        extraction_metadata={
            "method": "test",
            "schema_version": "1.0",
            "extraction_confidence": 1.0,
        },
    )

    job = Job(
        source_id=source.id,
        fact_graph_id=fact_graph.id,
        status="pending",
        controls={},
    )

    db_session.add(job)
    db_session.flush()

    document = NormalizedDocument(
        content=source.content,
        source_type="text",
        title=source.title,
        sections=[
            DocumentSection(
                section_id="persistence-test",
                content=source.content,
                source_reference="paragraph-1",
            )
        ],
    )

    embedding_provider = LocalEmbeddingProvider()

    vector_store = ChromaVectorStore(path="data/chroma")

    indexer = RAGIndexer(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    retriever = ChromaRetriever(
        vector_store=vector_store,
        embedding_provider=embedding_provider,
    )

    indexer.index(document)

    knowledge_service = KnowledgeService(
        fact_graph_repository=fact_graph_repository,
        retriever=retriever,
    )

    runtime = PRISMRuntime(
        db=db_session,
        knowledge_service=knowledge_service,
        control_resolver=ControlResolver(),
        specialist_registry=build_specialist_registry(
            MockLLMProvider()
        ),
    )

    graph = build_prism_graph(runtime)

    graph.invoke(
        {
            "source_id": str(source.id),
            "job_id": str(job.id),
            "query": "How many customers were affected?",
            "requested_outputs": ["linkedin"],
            "controls": GenerationControls(
                target_audience="General public",
                tone="Professional",
                language="English",
                level_of_detail="Concise",
                communication_objective="Inform",
                content_style="Clear and factual",
            ),
        }
    )

    output = (
        db_session.query(OutputDraft)
        .filter(OutputDraft.job_id == job.id)
        .first()
    )

    assert output is not None
    assert output.output_type == "linkedin"
    assert output.status == "draft"
    assert "310" in output.content
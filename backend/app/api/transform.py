from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.session import SessionLocal

from backend.app.models import Job, Source

from backend.app.schemas.controls import GenerationControls
from backend.app.services.ingestion import TextIngestor, ContentNormalizer

from backend.app.services.llm.groq import GroqLLMProvider
from backend.app.services.fact_graph.llm import LLMFactGraphExtractor
from backend.app.services.fact_graph.repository import FactGraphRepository
from backend.app.services.fact_graph.service import FactGraphService

from backend.app.services.rag.embeddings import LocalEmbeddingProvider
from backend.app.services.rag.chroma import ChromaVectorStore
from backend.app.services.rag.indexer import RAGIndexer

from backend.app.services.rag.retriever import ChromaRetriever

from backend.app.services.knowledge.service import KnowledgeService

from backend.app.services.orchestration.controls import ControlResolver
from backend.app.services.orchestration.specialists.factory import (
    build_specialist_registry,
)
from backend.app.services.orchestration.runtime import PRISMRuntime
from backend.app.services.orchestration.graph import build_prism_graph

from backend.app.services.guardrails.provenance import ProvenanceService
from backend.app.services.guardrails.critic import BasicGuardrailCritic
from backend.app.services.guardrails.factual import FactualGuardrailCritic
from backend.app.services.guardrails.llm_critic import LLMGuardrailCritic
from backend.app.services.guardrails.revision import BoundedRevisionService


router = APIRouter(prefix="/transform", tags=["transformation"])


class TransformRequest(BaseModel):
    content: str = Field(min_length=1)
    title: str | None = None
    controls: GenerationControls
    output_types: list[str] = Field(min_length=1)


class TransformResponse(BaseModel):
    job_id: UUID
    source_id: UUID
    fact_graph_id: UUID
    status: str
    outputs: dict
    guardrails: dict


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=TransformResponse)
def transform(
    request: TransformRequest,
    db: Session = Depends(get_db),
):
    if not settings.llm_api_key:
        raise HTTPException(
            status_code=500,
            detail="LLM API key is not configured.",
        )

    try:
        # -------------------------
        # 1. LLM PROVIDER
        # -------------------------
        provider = GroqLLMProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )

        # -------------------------
        # 2. SOURCE
        # -------------------------
        ingestion = TextIngestor()
        normalizer = ContentNormalizer()

        ingestion_result = ingestion.ingest(
            request.content,
            title=request.title,
        )

        document = normalizer.normalize(
            ingestion_result
        )

        source = Source(
            source_type=document.source_type,
            title=document.title,
            content=document.content,
            source_metadata=document.metadata,
        )

        db.add(source)
        db.flush()

        # -------------------------
        # 3. FACT GRAPH
        # -------------------------
        fact_graph_repository = FactGraphRepository()

        fact_graph_extractor = LLMFactGraphExtractor(
            provider
        )

        fact_graph_service = FactGraphService(
            extractor=fact_graph_extractor,
            repository=fact_graph_repository,
        )

        fact_graph = fact_graph_service.create(
            db,
            source_id=source.id,
            document=document,
        )

        # -------------------------
        # 4. RAG
        # -------------------------
        embedding_provider = LocalEmbeddingProvider()

        vector_store = ChromaVectorStore()

        rag_indexer = RAGIndexer(
            embedding_provider=embedding_provider,
            vector_store=vector_store,
        )

        rag_indexer.index(
            document=document,
            source_id=str(source.id),
)

        retriever = ChromaRetriever(
            embedding_provider=embedding_provider,
            vector_store=vector_store,
        )

        knowledge_service = KnowledgeService(
            fact_graph_repository=fact_graph_repository,
            retriever=retriever,
        )

        # -------------------------
        # 5. JOB
        # -------------------------
        job = Job(
            source_id=source.id,
            fact_graph_id=fact_graph.id,
            status="running",
            controls=request.controls.model_dump(),
        )

        db.add(job)
        db.flush()

        # -------------------------
        # 6. SPECIALISTS
        # -------------------------
        specialist_registry = build_specialist_registry(
            provider
        )

        runtime = PRISMRuntime(
            db=db,
            knowledge_service=knowledge_service,
            control_resolver=ControlResolver(),
            specialist_registry=specialist_registry,
            provenance_service=ProvenanceService(),
            basic_guardrail=BasicGuardrailCritic(),
            factual_guardrail=FactualGuardrailCritic(),
            llm_guardrail=LLMGuardrailCritic(provider),
            revision_service=BoundedRevisionService(provider),
        )

        # -------------------------
        # 7. LANGGRAPH
        # -------------------------
        graph = build_prism_graph(runtime)

        state = {
            "source_id": str(source.id),
            "job_id": str(job.id),
            "query": document.content[:1000],
            "controls": request.controls,
            "requested_outputs": request.output_types,
        }

        result = graph.invoke(state)

        # -------------------------
        # 8. JOB COMPLETE
        # -------------------------
        job.status = "completed"

        db.commit()

        outputs = {}

        for output_type, output in result.get(
            "generated_outputs",
            {},
        ).items():

            content = output.content

            if hasattr(content, "model_dump"):
                content = content.model_dump()

            outputs[output_type] = {
                "output_type": output.output_type,
                "content": content,
                "metadata": output.metadata,
            }

        guardrails = {}

        for output_type, guardrail in result.get(
            "guardrail_results",
            {},
        ).items():

            if hasattr(guardrail, "model_dump"):
                guardrails[output_type] = (
                    guardrail.model_dump()
                )
            else:
                guardrails[output_type] = guardrail

        return TransformResponse(
            job_id=job.id,
            source_id=source.id,
            fact_graph_id=fact_graph.id,
            status=job.status,
            outputs=outputs,
            guardrails=guardrails,
        )

    except Exception as exc:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
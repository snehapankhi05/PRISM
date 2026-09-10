import pytest

from backend.app.core.config import settings
from backend.app.schemas.controls import GenerationControls
from backend.app.schemas.fact_graph import Fact
from backend.app.services.knowledge.context import KnowledgeContext
from backend.app.services.llm.groq import GroqLLMProvider
from backend.app.services.orchestration.specialists.base import SpecialistInput
from backend.app.services.orchestration.specialists.linkedin import LinkedInSpecialist
from backend.app.services.rag.base import RetrievalResult


@pytest.mark.skipif(
    not settings.llm_api_key,
    reason="Groq API key is not configured",
)
def test_linkedin_specialist_with_groq():
    knowledge_context = KnowledgeContext(
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
        ],
        evidence=[
            RetrievalResult(
                chunk_id="chunk-1",
                content="The incident affected 310 customers.",
                source_reference="paragraph-1",
                score=0.1,
                metadata={},
            )
        ],
    )

    controls = GenerationControls(
        target_audience="General public",
        tone="Professional",
        language="English",
        level_of_detail="Concise",
        communication_objective="Inform the audience",
        content_style="Clear and factual",
    )

    provider = GroqLLMProvider(
        api_key=settings.llm_api_key,
        model=settings.llm_model,
    )

    specialist = LinkedInSpecialist(provider)

    result = specialist.generate(
        SpecialistInput(
            knowledge_context=knowledge_context,
            controls=controls,
        )
    )

    assert result.output_type == "linkedin"
    assert result.content.strip() != ""
    assert "310" in result.content

    print("\nGenerated LinkedIn post:\n")
    print(result.content)
from backend.app.schemas.controls import GenerationControls
from backend.app.schemas.fact_graph import Fact
from backend.app.services.knowledge.context import KnowledgeContext
from backend.app.services.orchestration.specialists.base import SpecialistInput
from backend.app.services.orchestration.specialists.linkedin import LinkedInSpecialist
from backend.app.services.rag.base import RetrievalResult
from backend.app.services.llm.mock import MockLLMProvider


def test_linkedin_specialist():
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

    specialist_input = SpecialistInput(
        knowledge_context=knowledge_context,
        controls=controls,
    )

    specialist = LinkedInSpecialist(
        provider=MockLLMProvider()
    )

    result = specialist.generate(specialist_input)

    assert result.output_type == "linkedin"
    assert isinstance(result.content, str)
    assert result.content.strip() != ""
    assert result.metadata["specialist"] == "LinkedInSpecialist"
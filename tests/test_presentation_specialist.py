from backend.app.schemas.controls import GenerationControls
from backend.app.schemas.fact_graph import Fact
from backend.app.services.knowledge.context import KnowledgeContext
from backend.app.services.orchestration.specialists.base import SpecialistInput
from backend.app.services.orchestration.specialists.presentation import (
    PresentationSpecialist,
)
from backend.app.services.llm.mock import MockLLMProvider


def test_presentation_specialist():
    knowledge_context = KnowledgeContext(
        facts=[
            Fact(
                id="fact-1",
                category="incident",
                subject="incident",
                predicate="affected",
                object="310 customers",
                source_reference="section-1",
                confidence=1.0,
            )
        ],
        evidence=[],
    )

    controls = GenerationControls(
        target_audience="Management",
        tone="Professional",
        language="English",
        level_of_detail="Detailed",
        communication_objective="Inform",
        content_style="Presentation",
    )

    specialist = PresentationSpecialist(MockLLMProvider())

    result = specialist.generate(
        SpecialistInput(
            knowledge_context=knowledge_context,
            controls=controls,
        )
    )

    assert result.output_type == "presentation"
    assert result.content
    assert result.metadata["specialist"] == "PresentationSpecialist"
    assert result.metadata["format"] == "structured"
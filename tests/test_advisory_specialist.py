from backend.app.schemas.controls import GenerationControls
from backend.app.schemas.fact_graph import Fact
from backend.app.services.knowledge.context import KnowledgeContext
from backend.app.services.orchestration.specialists.advisory import (
    AdvisorySpecialist,
)
from backend.app.services.orchestration.specialists.base import SpecialistInput
from backend.app.services.llm.mock import MockLLMProvider


def test_advisory_specialist():
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
        target_audience="General audience",
        tone="Professional",
        language="English",
        level_of_detail="Detailed",
        communication_objective="Inform",
        content_style="Advisory",
    )

    specialist = AdvisorySpecialist(MockLLMProvider())

    result = specialist.generate(
        SpecialistInput(
            knowledge_context=knowledge_context,
            controls=controls,
        )
    )

    assert result.output_type == "advisory"
    assert result.content
    assert result.metadata["specialist"] == "AdvisorySpecialist"
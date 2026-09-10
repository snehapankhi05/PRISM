from backend.app.services.llm.mock import MockLLMProvider
from backend.app.services.orchestration.specialists.linkedin import LinkedInSpecialist
from backend.app.services.orchestration.specialists.registry import SpecialistRegistry


def test_specialist_registry():
    linkedin_specialist = LinkedInSpecialist(
        provider=MockLLMProvider()
    )

    registry = SpecialistRegistry(
        specialists=[linkedin_specialist]
    )

    # Verify registration
    assert registry.has("linkedin")

    # Verify retrieval
    specialist = registry.get("linkedin")

    assert specialist is linkedin_specialist
    assert specialist.output_type == "linkedin"

    # Verify available outputs
    assert registry.available_outputs() == ["linkedin"]
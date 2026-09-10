from backend.app.services.llm.mock import MockLLMProvider
from backend.app.services.orchestration.specialists.factory import (
    build_specialist_registry,
)


def test_specialist_factory_registers_all_outputs():
    registry = build_specialist_registry(MockLLMProvider())

    expected_outputs = {
        "linkedin",
        "twitter",
        "advisory",
        "executive_summary",
        "presentation",
        "infographic",
        "video",
    }

    assert set(registry.available_outputs()) == expected_outputs

    for output_type in expected_outputs:
        assert registry.has(output_type)
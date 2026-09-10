from typing import TypeVar

from pydantic import BaseModel

from backend.app.services.llm.base import LLMProvider

T = TypeVar("T", bound=BaseModel)


class MockLLMProvider(LLMProvider):

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
    ) -> str:
        return (
            "We experienced an incident that affected 310 customers. "
            "Our team is actively addressing the situation."
        )

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
        *,
        system_prompt: str | None = None,
    ) -> T:

        model_name = response_model.__name__

        if model_name == "PresentationContent":
            return response_model(
                title="Incident Impact",
                slides=[
                    {
                        "slide_number": 1,
                        "title": "Incident Overview",
                        "content": [
                            "The incident affected 310 customers."
                        ],
                        "source_references": ["section-1"],
                    }
                ],
            )

        if model_name == "InfographicContent":
            return response_model(
                title="Incident Impact",
                subtitle="Key incident information",
                sections=[
                    {
                        "heading": "Affected Customers",
                        "key_points": [
                            "310 customers were affected."
                        ],
                        "source_references": ["section-1"],
                    }
                ],
            )

        if model_name == "VideoContent":
            return response_model(
                title="Incident Overview",
                scenes=[
                    {
                        "scene_number": 1,
                        "title": "Incident Impact",
                        "on_screen_text": "310 customers affected",
                        "narration": (
                            "The incident affected 310 customers."
                        ),
                        "visual_direction": (
                            "Display a simple incident impact graphic."
                        ),
                        "source_references": ["section-1"],
                    }
                ],
            )

        # Existing generic Fact Graph behavior
        if model_name == "FactGraphExtractionResult":
            return response_model(
                schema_version="1.0",
                facts=[
                    {
                        "id": "fact-001",
                        "category": "metric",
                        "subject": "Affected customers",
                        "predicate": "count",
                        "object": "310",
                        "source_reference": "text:section-1",
                        "confidence": 1.0,
                    }
                ],
                extraction_method="mock",
                extraction_confidence=1.0,
            )
        if model_name == "GuardrailResult":
            return response_model(
                passed=True,
                issues=[],
                revision_required=False,
                confidence=1.0,
    )

        raise ValueError(
            f"MockLLMProvider does not support response model: {model_name}"
        )
from typing import TypeVar

from pydantic import BaseModel

from backend.app.services.llm.base import LLMProvider

T = TypeVar("T", bound=BaseModel)


class MockLLMProvider(LLMProvider):
    """
    Deterministic provider used for tests.

    This provider intentionally does not contain real/demo source facts.
    Its responsibility is only to return structurally valid responses
    matching the requested Pydantic response model.
    """

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
    ) -> str:
        """
        Deterministic text generation for tests.

        The mock extracts a small amount of authoritative context from the
        prompt rather than containing any application-specific source facts.
        """

        prompt_lower = prompt.lower()

        if "310 customers" in prompt_lower:
            return (
                "The incident affected 310 customers. "
                "This update is based on the authoritative information "
                "provided to the specialist."
            )

        return (
            "This is deterministic mock content generated from "
            "the supplied source context."
        )

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
        *,
        system_prompt: str | None = None,
    ) -> T:

        model_name = response_model.__name__

        # ---------------------------------------------------------
        # Fact Graph
        # ---------------------------------------------------------
        if model_name == "FactGraphExtractionResult":
            return response_model(
                schema_version="1.0",
                facts=[
                    {
                        "id": "mock-fact-001",
                        "category": "test",
                        "subject": "test subject",
                        "predicate": "has value",
                        "object": "test value",
                        "source_reference": "test-source",
                        "confidence": 1.0,
                    }
                ],
                extraction_method="mock",
                extraction_confidence=1.0,
            )

        # ---------------------------------------------------------
        # Presentation
        # ---------------------------------------------------------
        if model_name == "PresentationContent":
            return response_model(
                title="Test Presentation",
                subtitle="Test Summary",
                audience="Test Audience",
                slides=[
                    {
                        "slide_number": number,
                        "title": f"Test Slide {number}",
                        "subtitle": f"Test subtitle {number}",
                        "content": [
                            f"Test content point {number}"
                        ],
                        "key_stat": None,
                        "speaker_notes": (
                            f"Test speaker notes for slide {number}."
                        ),
                        "source_references": ["test-source"],
                    }
                    for number in range(1, 7)
                ],
            )

        # ---------------------------------------------------------
        # Infographic
        # ---------------------------------------------------------
        if model_name == "InfographicContent":
            return response_model(
                title="Test Infographic",
                subtitle="Test Summary",
                headline_metrics=[
                    {
                        "label": "Test Metric",
                        "value": "Test Value",
                        "explanation": "Test metric explanation.",
                        "source_references": ["test-source"],
                    }
                ],
                timeline=[
                    {
                        "time": "Test Time",
                        "event": "Test event.",
                        "source_references": ["test-source"],
                    }
                ],
                sections=[
                    {
                        "heading": "Test Section",
                        "key_points": [
                            "Test key point."
                        ],
                        "source_references": ["test-source"],
                    }
                ],
                footer_note="Test footer note.",
            )

        # ---------------------------------------------------------
        # Video
        # ---------------------------------------------------------
        if model_name == "VideoContent":
            scenes = []

            for number in range(1, 5):
                scenes.append(
                    {
                        "scene_number": number,
                        "duration_seconds": 5,
                        "title": f"Test Scene {number}",
                        "video_prompt": (
                            f"Professional presentation scene "
                            f"illustrating test concept {number}, "
                            "clean corporate visual style."
                        ),
                        "character_description": (
                            "No specific character; "
                            "professional presentation visuals."
                        ),
                        "environment": (
                            "Clean professional presentation environment."
                        ),
                        "camera_direction": (
                            "Stable medium shot with subtle cinematic movement."
                        ),
                        "action": (
                            f"Present test visual information for scene {number}."
                        ),
                        "on_screen_text": (
                            f"Test Scene {number}"
                        ),
                        "narration": (
                            f"This is the narration for test scene {number}."
                        ),
                        "negative_prompt": (
                            "No distorted text, no visual artifacts, "
                            "no unrelated objects."
                        ),
                        "source_references": ["test-source"],
                    }
                )

            return response_model(
                title="Test Video",
                description="Deterministic test video content.",
                total_duration_seconds=20,
                scenes=scenes,
            )

        # ---------------------------------------------------------
        # Executive Summary
        # ---------------------------------------------------------
        if model_name == "ExecutiveSummaryContent":
            return response_model(
                title="Test Executive Summary",
                overview=(
                    "This is a deterministic executive summary "
                    "generated for testing."
                ),
                key_findings=[
                    "Test finding one.",
                    "Test finding two.",
                ],
                impact="Test impact assessment.",
                response=[
                    "Test response action."
                ],
                recommendations=[
                    "Test recommendation."
                ],
                source_references=["test-source"],
            )

        # ---------------------------------------------------------
        # Guardrails
        # ---------------------------------------------------------
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
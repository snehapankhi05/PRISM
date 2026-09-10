from backend.app.schemas.guardrails import GuardrailResult
from backend.app.services.orchestration.specialists.base import SpecialistOutput


class FailingBasicGuardrail:
    def evaluate(self, output):
        return GuardrailResult(
            passed=False,
            issues=[
                {
                    "issue_type": "test_failure",
                    "message": "Forced guardrail failure for integration test.",
                    "severity": "high",
                }
            ],
            revision_required=True,
            confidence=1.0,
        )


class PassingFactualGuardrail:
    def evaluate(self, output, knowledge_context):
        return GuardrailResult(
            passed=True,
            issues=[],
            revision_required=False,
            confidence=1.0,
        )


class PassingLLMGuardrail:
    def evaluate(self, output, knowledge_context):
        return GuardrailResult(
            passed=True,
            issues=[],
            revision_required=False,
            confidence=1.0,
        )


def test_guardrails_node_records_failure():
    from backend.app.services.orchestration.guardrails import guardrails_node

    output = SpecialistOutput(
        output_type="linkedin",
        content="Incident affected 310 customers.",
    )

    state = {
        "generated_outputs": {
            "linkedin": output,
        },
        "knowledge_context": object(),
    }

    result = guardrails_node(
        state,
        basic_guardrail=FailingBasicGuardrail(),
        factual_guardrail=PassingFactualGuardrail(),
        llm_guardrail=PassingLLMGuardrail(),
    )

    guardrail_result = result["guardrail_results"]["linkedin"]

    assert guardrail_result.passed is False
    assert guardrail_result.revision_required is True
    assert len(guardrail_result.issues) == 1

class FakeRevisionService:
    def revise(self, output, feedback, verified_facts=None):
        return SpecialistOutput(
            output_type=output.output_type,
            content="Revised content with verified facts.",
            metadata={"revision_count": 1},
        )


class RevisionTriggerGuardrail:
    def evaluate(self, output):
        return GuardrailResult(
            passed=False,
            issues=[
                {
                    "issue_type": "test_failure",
                    "message": "Forced revision.",
                    "severity": "high",
                }
            ],
            revision_required=True,
            confidence=1.0,
        )


def test_guardrails_revision_path():
    from backend.app.services.orchestration.guardrails import guardrails_node

    output = SpecialistOutput(
        output_type="linkedin",
        content="Incorrect content.",
    )

    state = {
        "generated_outputs": {"linkedin": output},
        "knowledge_context": object(),
    }

    result = guardrails_node(
        state,
        basic_guardrail=RevisionTriggerGuardrail(),
        factual_guardrail=PassingFactualGuardrail(),
        llm_guardrail=PassingLLMGuardrail(),
        revision_service=FakeRevisionService(),
    )

    revised = result["generated_outputs"]["linkedin"]

    assert revised.content == "Revised content with verified facts."
    assert revised.metadata["revision_count"] == 1
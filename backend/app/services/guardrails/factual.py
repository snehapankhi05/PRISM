from backend.app.schemas.guardrails import GuardrailIssue, GuardrailResult
from backend.app.services.orchestration.specialists.base import SpecialistOutput
from backend.app.services.knowledge.context import KnowledgeContext


class FactualGuardrailCritic:

    def evaluate(
        self,
        output: SpecialistOutput,
        knowledge_context: KnowledgeContext,
    ) -> GuardrailResult:

        issues: list[GuardrailIssue] = []

        content = output.content

        if hasattr(content, "model_dump_json"):
            text = content.model_dump_json()
        else:
            text = str(content)

        for fact in knowledge_context.facts:
            expected_value = fact.object

            if expected_value.isdigit():
                if expected_value not in text:
                    issues.append(
                        GuardrailIssue(
                            issue_type="factual_mismatch",
                            message=(
                                f"Expected factual value '{expected_value}' "
                                f"from source {fact.source_reference} "
                                f"was not found in the generated output."
                            ),
                            severity="high",
                        )
                    )

        passed = not issues

        return GuardrailResult(
            passed=passed,
            issues=issues,
            revision_required=not passed,
            confidence=1.0 if passed else 0.0,
        )
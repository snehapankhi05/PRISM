from backend.app.schemas.guardrails import GuardrailIssue, GuardrailResult
from backend.app.services.orchestration.specialists.base import SpecialistOutput


class BasicGuardrailCritic:

    def evaluate(
        self,
        output: SpecialistOutput,
    ) -> GuardrailResult:

        issues: list[GuardrailIssue] = []

        if output.content is None:
            issues.append(
                GuardrailIssue(
                    issue_type="empty_output",
                    message="Generated output is empty.",
                    severity="high",
                )
            )

        if isinstance(output.content, str):
            if not output.content.strip():
                issues.append(
                    GuardrailIssue(
                        issue_type="empty_output",
                        message="Generated output contains no content.",
                        severity="high",
                    )
                )

        passed = len(issues) == 0

        return GuardrailResult(
            passed=passed,
            issues=issues,
            revision_required=not passed,
            confidence=1.0 if passed else 0.0,
        )
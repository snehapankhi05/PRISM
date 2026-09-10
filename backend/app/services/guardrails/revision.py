from backend.app.services.llm.base import LLMProvider
from backend.app.services.orchestration.specialists.base import SpecialistOutput


class BoundedRevisionService:
    MAX_REVISIONS = 1

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def revise(
        self,
        output: SpecialistOutput,
        feedback: str,
        verified_facts: list | None = None,
    ) -> SpecialistOutput:
        revision_count = output.metadata.get("revision_count", 0)

        if revision_count >= self.MAX_REVISIONS:
            return output

        if not feedback.strip():
            return output

        facts_text = "\n".join(
            f"- {fact.object}: {fact.value}"
            for fact in (verified_facts or [])
        )

        prompt = f"""
Revise the generated content to address the critic feedback.

VERIFIED FACTS:
{facts_text}

CURRENT CONTENT:
{output.content}

CRITIC FEEDBACK:
{feedback}

Rules:
- Do not invent facts.
- Do not change verified numbers.
- Do not add information absent from the verified facts.
- Preserve the requested output format.
- Correct only the identified issues.
"""

        if hasattr(output.content, "model_dump_json"):
            content_type = type(output.content)
            revised_content = self.provider.generate_structured(
                prompt,
                content_type,
            )
        else:
            revised_content = self.provider.generate(prompt)

        return SpecialistOutput(
            output_type=output.output_type,
            content=revised_content,
            metadata={
                **output.metadata,
                "revision_count": revision_count + 1,
                "revision_reason": feedback,
            },
        )
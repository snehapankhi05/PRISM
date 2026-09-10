from backend.app.schemas.guardrails import GuardrailResult
from backend.app.services.llm.base import LLMProvider
from backend.app.services.orchestration.specialists.base import SpecialistOutput
from backend.app.services.knowledge.context import KnowledgeContext


class LLMGuardrailCritic:

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def evaluate(
        self,
        output: SpecialistOutput,
        knowledge_context: KnowledgeContext,
    ) -> GuardrailResult:

        if hasattr(output.content, "model_dump_json"):
            generated_content = output.content.model_dump_json()
        else:
            generated_content = str(output.content)

        facts = "\n".join(
            f"- {fact.subject} | {fact.predicate} | {fact.object} "
            f"(source: {fact.source_reference})"
            for fact in knowledge_context.facts
        )

        prompt = f"""
Evaluate the generated content against the verified facts.

VERIFIED FACTS:
{facts}

GENERATED CONTENT:
{generated_content}

Check for:
1. Invented facts
2. Incorrect numbers
3. Incorrect dates or times
4. Contradictions
5. Unsupported claims

Return only structured data matching GuardrailResult.
Do not rewrite the content.
""".strip()

        return self.provider.generate_structured(
            prompt,
            GuardrailResult,
            system_prompt=(
                "You are PRISM's factual consistency critic. "
                "Be strict. Never approve unsupported factual claims."
            ),
        )
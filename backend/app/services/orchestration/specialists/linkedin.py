from backend.app.services.llm.base import LLMProvider
from backend.app.services.orchestration.specialists.base import (
    SpecialistAgent,
    SpecialistInput,
    SpecialistOutput,
)
from backend.app.services.orchestration.specialists.prompt_builder import (
    SpecialistPromptBuilder,
)

class LinkedInSpecialist(SpecialistAgent):
    output_type = "linkedin"

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate(self, input_data: SpecialistInput) -> SpecialistOutput:
        prompt = self._build_prompt(input_data)

        content = self.provider.generate(
            prompt,
            system_prompt=(
                "You are PRISM's LinkedIn content specialist. "
                "Create professional, factual LinkedIn content. "
                "Use only information supported by the provided "
                "knowledge context. Never invent facts."
            ),
        )

        return SpecialistOutput(
            output_type=self.output_type,
            content=content.strip(),
            metadata={
                "specialist": self.__class__.__name__,
            },
        )

    @staticmethod
    def _build_prompt(input_data: SpecialistInput) -> str:
        controls = input_data.controls
        knowledge = input_data.knowledge_context

        facts = "\n".join(
            (
                f"- {fact.subject} | "
                f"{fact.predicate} | "
                f"{fact.object} "
                f"(source: {fact.source_reference})"
            )
            for fact in knowledge.facts
        )

        evidence = "\n".join(
            (
                f"- {item.content} "
                f"(source: {item.source_reference})"
            )
            for item in knowledge.evidence
        )

        return f"""
Create a LinkedIn post using the following requirements.

TARGET AUDIENCE:
{controls.target_audience}

TONE:
{controls.tone}

LANGUAGE:
{controls.language}

LEVEL OF DETAIL:
{controls.level_of_detail}

COMMUNICATION OBJECTIVE:
{controls.communication_objective}

CONTENT STYLE:
{controls.content_style}

FACT GRAPH:
{facts}

SOURCE EVIDENCE:
{evidence}

Rules:
1. Use only supported facts.
2. Do not invent numbers, dates, names, events, or claims.
3. Preserve factual values exactly.
4. Follow all requested controls.
5. Do not mention the Fact Graph, RAG, or internal PRISM system.
6. Return only the LinkedIn post.
""".strip()
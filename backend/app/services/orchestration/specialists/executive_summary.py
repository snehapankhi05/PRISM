from backend.app.services.llm.base import LLMProvider
from backend.app.services.orchestration.specialists.base import (
    SpecialistAgent,
    SpecialistInput,
    SpecialistOutput,
)
from backend.app.services.orchestration.specialists.prompt_builder import (
    SpecialistPromptBuilder,
)


class ExecutiveSummarySpecialist(SpecialistAgent):
    output_type = "executive_summary"

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate(
        self,
        input_data: SpecialistInput,
    ) -> SpecialistOutput:
        context = SpecialistPromptBuilder.build_context(input_data)

        prompt = f"""
Create an executive summary using the following context.

{context}

EXECUTIVE SUMMARY REQUIREMENTS:
1. Start with a concise overview of the key situation.
2. Highlight the most important facts, impact, and actions.
3. Prioritize information relevant to decision-makers.
4. Preserve all important numbers, dates, and measurements exactly.
5. Do not introduce unsupported conclusions.
6. Keep the structure concise and easy to scan.
7. Use headings or bullet points where appropriate.
8. Return only the executive summary.
""".strip()

        content = self.provider.generate(
            prompt,
            system_prompt=(
                "You are PRISM's executive summary specialist. "
                "Create concise, decision-oriented summaries using "
                "only supported source information."
            ),
        )

        return SpecialistOutput(
            output_type=self.output_type,
            content=content.strip(),
            metadata={
                "specialist": self.__class__.__name__,
            },
        )
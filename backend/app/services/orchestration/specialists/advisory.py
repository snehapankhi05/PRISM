from backend.app.services.llm.base import LLMProvider
from backend.app.services.orchestration.specialists.base import (
    SpecialistAgent,
    SpecialistInput,
    SpecialistOutput,
)
from backend.app.services.orchestration.specialists.prompt_builder import (
    SpecialistPromptBuilder,
)


class AdvisorySpecialist(SpecialistAgent):
    output_type = "advisory"

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate(
        self,
        input_data: SpecialistInput,
    ) -> SpecialistOutput:
        context = SpecialistPromptBuilder.build_context(input_data)

        prompt = f"""
Create a clear professional advisory using the following context.

{context}

ADVISORY REQUIREMENTS:
1. Include a clear title.
2. Clearly explain the situation or issue.
3. Present only supported facts.
4. Include relevant actions or recommendations only when supported
   by the source evidence.
5. Clearly distinguish facts from recommendations.
6. Do not invent deadlines, risks, statistics, or actions.
7. Use a professional advisory structure.
8. Return only the advisory content.
""".strip()

        content = self.provider.generate(
            prompt,
            system_prompt=(
                "You are PRISM's advisory content specialist. "
                "Create accurate, structured advisories using only "
                "supported source information."
            ),
        )

        return SpecialistOutput(
            output_type=self.output_type,
            content=content.strip(),
            metadata={
                "specialist": self.__class__.__name__,
            },
        )
from backend.app.services.llm.base import LLMProvider
from backend.app.services.orchestration.specialists.base import (
    SpecialistAgent,
    SpecialistInput,
    SpecialistOutput,
)
from backend.app.services.orchestration.specialists.prompt_builder import (
    SpecialistPromptBuilder,
)


class TwitterSpecialist(SpecialistAgent):
    output_type = "twitter"

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate(
        self,
        input_data: SpecialistInput,
    ) -> SpecialistOutput:
        context = SpecialistPromptBuilder.build_context(input_data)

        prompt = f"""
Create a professional Twitter/X post using the following context.

{context}

TWITTER/X REQUIREMENTS:
1. Keep the post concise.
2. Stay within a single-post format.
3. Make the key message immediately clear.
4. Preserve factual accuracy.
5. Do not invent hashtags, numbers, dates, or claims.
6. Return only the Twitter/X post.
""".strip()

        content = self.provider.generate(
            prompt,
            system_prompt=(
                "You are PRISM's Twitter/X content specialist. "
                "Create concise, factual content using only "
                "supported information."
            ),
        )

        return SpecialistOutput(
            output_type=self.output_type,
            content=content.strip(),
            metadata={
                "specialist": self.__class__.__name__,
            },
        )
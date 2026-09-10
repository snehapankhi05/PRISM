from backend.app.services.llm.base import LLMProvider
from backend.app.services.orchestration.specialists.base import (
    SpecialistAgent,
    SpecialistInput,
    SpecialistOutput,
)
from backend.app.services.orchestration.specialists.prompt_builder import (
    SpecialistPromptBuilder,
)
from backend.app.schemas.generated_outputs import InfographicContent

class InfographicSpecialist(SpecialistAgent):
    output_type = "infographic"

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate(
        self,
        input_data: SpecialistInput,
    ) -> SpecialistOutput:
        context = SpecialistPromptBuilder.build_context(input_data)

        prompt = f"""
Create structured infographic content using the following context.

{context}

INFOGRAPHIC REQUIREMENTS:
1. Identify the most important facts and numbers.
2. Organize the information into clear visual sections.
3. Keep each section concise.
4. Preserve factual values exactly.
5. Do not invent statistics, dates, names, or claims.
6. Include source references for factual elements.
7. Do not create the image itself.
8. Return valid JSON only.

Return this structure:

{{
  "title": "Infographic title",
  "subtitle": "Short description",
  "sections": [
    {{
      "heading": "Section heading",
      "key_points": ["Point 1", "Point 2"],
      "source_references": ["section-1"]
    }}
  ]
}}
""".strip()

        content = self.provider.generate_structured(
            prompt,
            InfographicContent,
            system_prompt=(
                "You are PRISM's infographic content specialist. "
                "Create concise, visually structured and factual "
                "content using only supported information."
            ),
        )

        return SpecialistOutput(
    output_type=self.output_type,
    content=content,
    metadata={
        "specialist": self.__class__.__name__,
        "format": "structured",
    },
)
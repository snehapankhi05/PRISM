from backend.app.services.llm.base import LLMProvider
from backend.app.services.orchestration.specialists.base import (
    SpecialistAgent,
    SpecialistInput,
    SpecialistOutput,
)
from backend.app.services.orchestration.specialists.prompt_builder import (
    SpecialistPromptBuilder,
)
from backend.app.schemas.generated_outputs import PresentationContent

class PresentationSpecialist(SpecialistAgent):
    output_type = "presentation"

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate(
        self,
        input_data: SpecialistInput,
    ) -> SpecialistOutput:
        context = SpecialistPromptBuilder.build_context(input_data)

        prompt = f"""
Create structured presentation content using the following context.

{context}

PRESENTATION REQUIREMENTS:
1. Create a logical presentation structure.
2. Include a clear title.
3. Create concise slides with clear headings.
4. Each slide should contain a small number of focused points.
5. Preserve all factual values exactly.
6. Do not invent statistics, dates, names, or claims.
7. Include source references for factual slide content.
8. Do not create the actual PowerPoint file.
9. Return valid JSON only.

Return this structure:

{{
  "title": "Presentation title",
  "slides": [
    {{
      "slide_number": 1,
      "title": "Slide title",
      "content": ["Point 1", "Point 2"],
      "source_references": ["section-1"]
    }}
  ]
}}
""".strip()

        content = self.provider.generate_structured(
            prompt,
            PresentationContent,
            system_prompt=(
                "You are PRISM's presentation content specialist. "
                "Create structured, factual presentation content. "
                "Never invent unsupported information."
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
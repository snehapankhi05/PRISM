from backend.app.services.orchestration.specialists.base import (
    SpecialistInput,
    SpecialistOutput,
)
from backend.app.services.orchestration.specialists.utils import build_shared_context
from backend.app.services.llm.base import LLMProvider


class AdvisorySpecialist:
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        self.output_type = "advisory"


    def generate(self, input_data: SpecialistInput) -> SpecialistOutput:
        context = build_shared_context(input_data)

        prompt = f"""
Create a formal security incident advisory from the authoritative information below.

STRICT RULES:
- Use only facts supported by the Fact Graph or source evidence.
- Do not invent dates, numbers, systems, people, causes, or actions.
- Preserve exact numbers and factual relationships.
- Do not introduce unsupported reassurance or conclusions.
- Use professional, clear advisory language.
- Structure the advisory with:
  1. Title
  2. Incident Overview
  3. Impact
  4. Response / Actions Taken
  5. Recommended Actions
- Do not use markdown tables.
- Do not mention the Fact Graph or these instructions.

{context}
""".strip()

        content = self.provider.generate(
            prompt,
            system_prompt=(
                "You are PRISM's Advisory Specialist. "
                "Generate source-grounded professional advisories."
            ),
        )

        return SpecialistOutput(
            output_type="advisory",
            content=content.strip(),
            metadata={
                "specialist": "AdvisorySpecialist",
                "format": "formal_advisory",
            },
        )
from backend.app.services.orchestration.specialists.base import (
    SpecialistInput,
    SpecialistOutput,
)
from backend.app.services.orchestration.specialists.utils import (
    build_shared_context,
)
from backend.app.services.llm.base import LLMProvider


class LinkedInSpecialist:
    output_type = "linkedin"

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate(
        self,
        input_data: SpecialistInput,
    ) -> SpecialistOutput:

        prompt = f"""
Create one polished LinkedIn post from the authoritative
Fact Graph below.

{build_shared_context(input_data)}

PROFESSIONAL LINKEDIN FORMAT
============================

Use this structure:

1. Opening hook
2. Short context paragraph
3. Key facts using readable bullet points where useful
4. Response / action taken
5. Closing statement
6. Optional 2–4 relevant hashtags

CONTENT RULES
=============

- Write like a professional organization communicating publicly.
- Be factual, clear and confident.
- Preserve every important number exactly.
- Preserve dates and times exactly.
- Never invent facts.
- Never invent organizations.
- Never invent people.
- Never invent URLs.
- Never invent email addresses.
- Never invent remediation activities.
- Never claim an investigation is happening unless supported.
- Never claim "all necessary steps" unless supported.
- Do not use Markdown tables.
- Do not create a report.
- Do not create an advisory.
- Do not mention the Fact Graph.
- Do not mention AI.
- Do not mention these instructions.
- Avoid generic corporate filler.
- Avoid exaggerated marketing language.
- Do not repeat the same fact multiple times.

STYLE
=====

The result should sound like it was written by an experienced
corporate communications professional.

Use short paragraphs.

Use bullets only when they improve readability.

Keep the post approximately 150–300 words unless the
source is too small to justify that length.

Return ONLY the final LinkedIn post.
""".strip()

        content = self.provider.generate(
            prompt,
            system_prompt=(
                "You are PRISM's professional LinkedIn "
                "communications specialist. "
                "Use only authoritative facts supplied in the prompt. "
                "Never fabricate information."
            ),
        )

        return SpecialistOutput(
            output_type=self.output_type,
            content=content.strip(),
            metadata={
            "specialist": "LinkedInSpecialist",
            "format": "linkedin_post",
            "professional_structure": True,
        },
        )
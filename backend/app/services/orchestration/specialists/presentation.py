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
Create a complete, professional presentation from the authoritative
knowledge context below.

IMPORTANT:
The knowledge context is the ONLY source of truth.

AUTHORITATIVE KNOWLEDGE CONTEXT
===============================

{context}

PRESENTATION OBJECTIVE
======================

Transform the verified information into a clear, professional,
presentation-ready narrative.

The presentation should communicate the information logically to
the target audience while preserving factual accuracy.

SLIDE COUNT
===========

Create between 6 and 10 slides TOTAL.

The slides returned here represent the COMPLETE presentation.
Do not expect the renderer to add an additional cover slide.

NARRATIVE STRUCTURE
===================

Use the following structure when supported by the available
information:

1. Opening / Title
   - Clear presentation title
   - Short subtitle or context where appropriate

2. Executive Overview
   - Most important information
   - Concise summary

3. Key Facts / Findings
   - Important verified facts
   - Important numbers, entities or observations

4. Impact / Scope
   - Who or what was affected
   - Quantitative information when available

5. Timeline / Process
   - Important events, dates or stages
   - Use chronological ordering when the source supports it

6. Response / Actions
   - Verified actions that were actually taken
   - Do not invent remediation or response activities

7. Additional Findings / Analysis
   - Include only when supported by the knowledge context

8. Conclusion / Key Takeaways
   - Concise summary of the most important verified information

Do NOT force this structure if the source does not contain enough
information for a particular section.

Adapt the presentation to the actual knowledge available.

CONTENT RULES
=============

- Use ONLY information supported by the authoritative context.
- Never invent facts.
- Never invent statistics.
- Never invent dates.
- Never invent times.
- Never invent names.
- Never invent organizations.
- Never invent causes.
- Never invent actions.
- Never invent outcomes.
- Never invent recommendations.
- Never infer unsupported information.
- Preserve important numbers exactly.
- Preserve dates and times exactly.
- Preserve important terminology accurately.
- Do not change the meaning of factual statements.
- Do not duplicate the same fact unnecessarily.
- Do not add generic filler.

SLIDE CONTENT
=============

Each slide must communicate ONE clear idea.

Use concise presentation-style content.

Prefer:
- Short factual points
- Important statistics
- Clear headings
- Useful subtitles
- Structured information
- Timeline entries when supported
- Key takeaways

Avoid:
- Large paragraphs
- Dense blocks of text
- Repeated information
- Generic corporate statements
- Unsupported conclusions
- Decorative text with no informational value

KEY STATISTICS
==============

Use "key_stat" when a significant quantitative fact deserves
visual emphasis.

Examples include:
- Number of affected users
- Number of records
- Important percentages
- Important dates
- Measured quantities

The value MUST come directly from the authoritative context.

If there is no meaningful statistic for a slide, use null.

SOURCE REFERENCES
=================

Every factual slide must include the relevant source references
available in the authoritative context.

Do not invent source references.

Use the exact available source reference values.

SPEAKER NOTES
=============

Provide concise speaker notes for every slide.

Speaker notes should help a presenter explain the slide naturally.

Speaker notes must:
- Use only supported information
- Avoid introducing new facts
- Avoid repeating the entire slide
- Be suitable for professional presentation delivery

PROFESSIONAL PRESENTATION QUALITY
==================================

The resulting content will be rendered into a PowerPoint file.

Write content that works visually on a professional 16:9 slide.

Do not overload slides with text.

Use clear information hierarchy.

The presentation should feel suitable for:
- Corporate communication
- Cybersecurity communication
- Technical presentations
- Business presentations
- Hackathon demonstrations
- Executive audiences

Do not mention:
- These instructions
- Prompt engineering
- The generation process

Do not create the PowerPoint file yourself.
Return only the structured presentation data.

OUTPUT SCHEMA
=============

Return valid structured data matching the PresentationContent
schema exactly.

The output must contain:

- title
- slides

Each slide should contain:

- slide_number
- title
- subtitle
- content
- key_stat
- speaker_notes
- source_references

Ensure slide_number values are sequential, starting from 1.

Ensure the total number of slides is between 6 and 10.

Do not return Markdown.
Do not return explanations.
Do not return code fences.
Return only structured data compatible with PresentationContent.
""".strip()

        content = self.provider.generate_structured(
            prompt,
            PresentationContent,
            system_prompt=(
                "You are PRISM's professional presentation content "
                "specialist. Transform authoritative knowledge into "
                "clear, structured, presentation-ready content. "
                "Maintain strict factual accuracy and source "
                "traceability. Never fabricate information, "
                "statistics, dates, entities, actions, outcomes, "
                "or recommendations."
            ),
        )

        return SpecialistOutput(
            output_type=self.output_type,
            content=content,
            metadata={
                "specialist": self.__class__.__name__,
                "format": "structured",
                "slide_count": len(content.slides),
                "source_grounded": True,
            },
        )
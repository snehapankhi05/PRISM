from backend.app.services.llm.base import LLMProvider
from backend.app.services.orchestration.specialists.base import (
    SpecialistAgent,
    SpecialistInput,
    SpecialistOutput,
)
from backend.app.services.orchestration.specialists.prompt_builder import (
    SpecialistPromptBuilder,
)
from backend.app.schemas.generated_outputs import VideoContent

class VideoSpecialist(SpecialistAgent):
    output_type = "video"

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate(
        self,
        input_data: SpecialistInput,
    ) -> SpecialistOutput:
        context = SpecialistPromptBuilder.build_context(input_data)

        prompt = f"""
Create structured presentation-style video content using the
following context.

{context}

VIDEO REQUIREMENTS:
1. Create a logical sequence of scenes.
2. Each scene must have a short title.
3. Include concise on-screen text.
4. Include narration text.
5. Include suggested visual direction.
6. Preserve factual values exactly.
7. Do not invent statistics, dates, names, or claims.
8. Include source references for factual scenes.
9. Do not generate the video file itself.
10. Return valid JSON only.

Return this structure:

{{
  "title": "Video title",
  "scenes": [
    {{
      "scene_number": 1,
      "title": "Scene title",
      "on_screen_text": "Short text",
      "narration": "Narration",
      "visual_direction": "Suggested visual",
      "source_references": ["section-1"]
    }}
  ]
}}
""".strip()

        content = self.provider.generate_structured(
            prompt,
            VideoContent,
            system_prompt=(
                "You are PRISM's video content specialist. "
                "Create structured, factual presentation-style "
                "video content using only supported information."
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
from backend.app.services.orchestration.specialists.base import (
    SpecialistInput,
    SpecialistOutput,
)
from backend.app.services.orchestration.specialists.utils import (
    build_shared_context,
)
from backend.app.services.llm.base import LLMProvider


MAX_TWEET_LENGTH = 280


class TwitterSpecialist:
    output_type = "twitter"

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate(
        self,
        input_data: SpecialistInput,
    ) -> SpecialistOutput:

        prompt = f"""
Create professional Twitter/X content from the authoritative
Fact Graph below.

{build_shared_context(input_data)}

TWITTER/X REQUIREMENTS
======================

Create ONE concise Twitter/X post.

HARD LIMIT:
Maximum 260 characters.

The 20-character buffer is intentional so the final renderer
can safely add formatting if required.

RULES
=====

- Communicate the most important verified information.
- Preserve critical numbers exactly.
- Preserve critical times/dates exactly.
- Use natural Twitter/X language.
- Be concise.
- No Markdown tables.
- No long paragraphs.
- No report structure.
- No headings such as "Impact", "Remediation", "Timeline".
- No fabricated hashtags.
- Do not invent URLs.
- Do not invent contacts.
- Do not invent facts.
- Do not mention the Fact Graph.
- Do not mention AI.
- Do not use emojis unless they genuinely improve the communication.
- Do not use sensational language.
- Do not use unsupported claims.

If the source contains more information than can reasonably fit,
prioritize:
1. What happened
2. Most important impact
3. Most important response

Return ONLY the final Twitter/X post.
""".strip()

        content = self.provider.generate(
            prompt,
            system_prompt=(
                "You are PRISM's professional Twitter/X "
                "communications specialist. "
                "Be concise and factual. "
                "Never fabricate information."
            ),
        ).strip()

        # Deterministic post-generation enforcement.
        if len(content) > MAX_TWEET_LENGTH:
            content = content[:MAX_TWEET_LENGTH - 1].rstrip() + "…"

        return SpecialistOutput(
            output_type=self.output_type,
            content=content,
            metadata={
            "specialist": "TwitterSpecialist",
            "format": "twitter_post",
            "character_count": len(content),
            "character_limit": MAX_TWEET_LENGTH,
            "professional_structure": True,
},
        )
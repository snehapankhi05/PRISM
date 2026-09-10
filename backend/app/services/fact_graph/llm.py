from backend.app.schemas.fact_graph import (
    FactGraphData,
    FactGraphExtractionResult,
)
from backend.app.services.fact_graph.base import FactGraphExtractor
from backend.app.services.ingestion.document import NormalizedDocument
from backend.app.services.llm.base import LLMProvider


class LLMFactGraphExtractor(FactGraphExtractor):
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def extract(self, document: NormalizedDocument) -> FactGraphExtractionResult:
        prompt = self._build_prompt(document)

        result = self.provider.generate_structured(
            prompt,
            FactGraphExtractionResult,
            system_prompt=(
                "You are PRISM's Fact Graph extraction engine. "
                "Extract only facts supported by source evidence. "
                "Never invent facts."
            ),
        )

        return result

    @staticmethod
    def _build_prompt(document: NormalizedDocument) -> str:
        sections = "\n\n".join(
            f"REFERENCE: {section.source_reference}\n"
            f"{section.content}"
            for section in document.sections
    )

        return f"""
    Extract the factual information from the source below.

    Rules:
    1. Extract only facts explicitly supported by the source.
    2. Do not invent, assume, or infer unsupported information.
    3. Preserve exact numbers, dates, times, names, and measurements.
    4. Every fact must include its source reference.
    5. Assign a confidence score between 0 and 1.
    6. Use uncertainty when the source is ambiguous.
    7. Prefer atomic facts rather than combining unrelated claims.
    8. Do not generate summaries, recommendations, or opinions.

    Return structured data matching the FactGraphExtractionResult schema.

    SOURCE:
    {sections}
    """.strip()
import re

from backend.app.services.ingestion.base import IngestionResult
from backend.app.services.ingestion.document import (
    DocumentSection,
    NormalizedDocument,
)


class ContentNormalizer:
    def normalize(
        self,
        result: IngestionResult,
    ) -> NormalizedDocument:
        content = result.content

        content = content.replace("\r\n", "\n").replace("\r", "\n")

        content = "\n".join(
            line.strip()
            for line in content.split("\n")
        )

        content = re.sub(r"\n{3,}", "\n\n", content)
        content = content.strip()

        if not content:
            raise ValueError(
                "Content is empty after normalization."
            )

        sections = self._build_sections(
            content,
            result.source_type,
        )

        metadata = dict(result.metadata)
        metadata["normalized"] = True
        metadata["normalized_character_count"] = len(content)
        metadata["line_count"] = len(content.splitlines())
        metadata["section_count"] = len(sections)

        return NormalizedDocument(
            content=content,
            source_type=result.source_type,
            title=result.title,
            sections=sections,
            metadata=metadata,
        )

    @staticmethod
    def _build_sections(
        content: str,
        source_type: str,
    ) -> list[DocumentSection]:
        raw_sections = [
            section.strip()
            for section in re.split(r"\n{2,}", content)
            if section.strip()
        ]

        sections: list[DocumentSection] = []

        for index, section in enumerate(raw_sections, start=1):
            sections.append(
                DocumentSection(
                    section_id=f"section-{index}",
                    content=section,
                    source_reference=(
                        f"{source_type}:section-{index}"
                    ),
                )
            )

        return sections
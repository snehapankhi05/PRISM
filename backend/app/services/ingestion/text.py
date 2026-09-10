from backend.app.services.ingestion.base import IngestionResult


class TextIngestor:
    def ingest(
        self,
        content: str,
        title: str | None = None,
    ) -> IngestionResult:
        if not content or not content.strip():
            raise ValueError("Text content cannot be empty.")

        return IngestionResult(
            content=content,
            source_type="text",
            title=title,
            metadata={
                "character_count": len(content),
            },
        )
from pathlib import Path

from docx import Document

from backend.app.services.ingestion.base import IngestionResult


class DOCXIngestor:
    def ingest(self, file_path: str) -> IngestionResult:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"DOCX file not found: {path}")

        if path.suffix.lower() != ".docx":
            raise ValueError("Expected a DOCX file.")

        document = Document(path)

        paragraphs = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        content = "\n\n".join(paragraphs).strip()

        if not content:
            raise ValueError(
                "No extractable text found in the DOCX file."
            )

        return IngestionResult(
            content=content,
            source_type="docx",
            title=path.stem,
            metadata={
                "filename": path.name,
                "paragraph_count": len(paragraphs),
            },
        )
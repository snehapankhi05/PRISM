from pathlib import Path

import pymupdf
from backend.app.services.ingestion.base import IngestionResult


class PDFIngestor:
    def ingest(self, file_path: str) -> IngestionResult:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError("Expected a PDF file.")

        pages: list[str] = []

        with pymupdf.open(path) as document:
            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text").strip()

                if text:
                    pages.append(
                        f"[Page {page_number}]\n{text}"
                    )

            page_count = len(document)

        content = "\n\n".join(pages).strip()

        if not content:
            raise ValueError(
                "No extractable text found in the PDF."
            )

        return IngestionResult(
            content=content,
            source_type="pdf",
            title=path.stem,
            metadata={
                "filename": path.name,
                "page_count": page_count,
            },
        )
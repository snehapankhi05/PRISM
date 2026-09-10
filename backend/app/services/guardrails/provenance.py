from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.models.provenance_link import ProvenanceLink
from backend.app.services.orchestration.specialists.base import SpecialistOutput


class ProvenanceService:

    def create_links(
        self,
        db: Session,
        *,
        output_draft_id: UUID,
        source_id: UUID,
        output: SpecialistOutput,
    ) -> list[ProvenanceLink]:

        links: list[ProvenanceLink] = []

        content = output.content

        if hasattr(content, "model_dump"):
            data = content.model_dump()
            references = self._extract_references(data)
        else:
            references = []

        for reference in references:
            link = ProvenanceLink(
                output_draft_id=output_draft_id,
                source_id=source_id,
                source_reference=reference,
                claim_reference="Generated content",
                confidence=1.0,
            )

            db.add(link)
            links.append(link)

        if links:
            db.commit()

            for link in links:
                db.refresh(link)

        return links

    def _extract_references(self, data: object) -> list[str]:

        references: list[str] = []

        if isinstance(data, dict):
            for key, value in data.items():

                if key == "source_references" and isinstance(value, list):
                    references.extend(
                        str(item)
                        for item in value
                        if item
                    )

                elif isinstance(value, (dict, list)):
                    references.extend(
                        self._extract_references(value)
                    )

        elif isinstance(data, list):
            for item in data:
                references.extend(
                    self._extract_references(item)
                )

        return list(dict.fromkeys(references))
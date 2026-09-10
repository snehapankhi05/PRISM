from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.models.output_draft import OutputDraft
class OutputRepository:
    def create(
        self,
        db: Session,
        *,
        job_id: UUID,
        output_type: str,
        content: str,
        quality_metadata: dict | None = None,
    ) -> OutputDraft:
        output = OutputDraft(
            job_id=job_id,
            output_type=output_type,
            version=1,
            content=content,
            status="draft",
            quality_metadata=quality_metadata or {},
        )

        db.add(output)
        db.commit()
        db.refresh(output)

        return output
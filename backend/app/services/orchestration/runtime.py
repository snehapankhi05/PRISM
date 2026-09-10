from dataclasses import dataclass

from sqlalchemy.orm import Session

from backend.app.services.knowledge.service import KnowledgeService
from backend.app.services.orchestration.controls import ControlResolver
from backend.app.services.orchestration.specialists.registry import SpecialistRegistry
from backend.app.services.orchestration.output_repository import OutputRepository
from dataclasses import dataclass, field
@dataclass(slots=True)
class PRISMRuntime:
    db: Session
    knowledge_service: KnowledgeService
    control_resolver: ControlResolver
    specialist_registry: SpecialistRegistry
    output_repository: OutputRepository = field(
    default_factory=OutputRepository
)
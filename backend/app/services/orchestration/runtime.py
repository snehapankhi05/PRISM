from dataclasses import dataclass, field
from pathlib import Path

from sqlalchemy.orm import Session

from backend.app.services.knowledge.service import KnowledgeService
from backend.app.services.orchestration.controls import ControlResolver
from backend.app.services.orchestration.specialists.registry import SpecialistRegistry
from backend.app.services.orchestration.output_repository import OutputRepository

from backend.app.services.guardrails.provenance import ProvenanceService
from backend.app.services.guardrails.critic import BasicGuardrailCritic
from backend.app.services.guardrails.factual import FactualGuardrailCritic
from backend.app.services.guardrails.llm_critic import LLMGuardrailCritic
from backend.app.services.guardrails.revision import BoundedRevisionService

from backend.app.services.rendering.registry import (
    RendererRegistry,
    create_default_registry,
)

from backend.app.services.llm.mock import MockLLMProvider


@dataclass(slots=True)
class PRISMRuntime:
    db: Session
    knowledge_service: KnowledgeService
    control_resolver: ControlResolver
    specialist_registry: SpecialistRegistry

    output_repository: OutputRepository = field(
        default_factory=OutputRepository
    )

    provenance_service: ProvenanceService = field(
        default_factory=ProvenanceService
    )

    basic_guardrail: BasicGuardrailCritic = field(
        default_factory=BasicGuardrailCritic
    )

    factual_guardrail: FactualGuardrailCritic = field(
        default_factory=FactualGuardrailCritic
    )

    llm_guardrail: LLMGuardrailCritic = field(
        default_factory=lambda: LLMGuardrailCritic(
            MockLLMProvider()
        )
    )

    revision_service: BoundedRevisionService = field(
        default_factory=lambda: BoundedRevisionService(
            MockLLMProvider()
        )
    )

    renderer_registry: RendererRegistry = field(
        default_factory=create_default_registry
    )

    output_root: Path = field(
        default_factory=lambda: Path("data/outputs")
    )
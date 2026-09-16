from typing import TypedDict

from backend.app.schemas.controls import GenerationControls
from backend.app.services.knowledge.context import KnowledgeContext


class PRISMState(TypedDict, total=False):
    source_id: str
    job_id: str
    query: str

    knowledge_context: KnowledgeContext
    controls: GenerationControls

    requested_outputs: list[str]

    generated_outputs: dict
    guardrail_results: dict

    rendered_outputs: dict
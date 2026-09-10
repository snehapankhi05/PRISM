from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.services.knowledge.service import KnowledgeService
from backend.app.services.orchestration.state import PRISMState


def knowledge_node(
    state: PRISMState,
    *,
    db: Session,
    knowledge_service: KnowledgeService,
) -> PRISMState:

    context = knowledge_service.build_context(
        db,
        source_id=UUID(state["source_id"]),
        query=state.get("query", ""),
        top_k=5,
    )

    return {
        **state,
        "knowledge_context": context,
    }
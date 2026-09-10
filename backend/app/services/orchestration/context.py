from backend.app.services.knowledge.context import KnowledgeContext


def build_generation_context(
    knowledge_context: KnowledgeContext,
) -> dict:
    return {
        "facts": knowledge_context.facts,
        "evidence": knowledge_context.evidence,
    }
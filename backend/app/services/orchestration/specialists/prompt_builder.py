from backend.app.services.orchestration.specialists.base import SpecialistInput


class SpecialistPromptBuilder:

    @staticmethod
    def build_context(input_data: SpecialistInput) -> str:
        controls = input_data.controls
        knowledge = input_data.knowledge_context

        facts = "\n".join(
            (
                f"- {fact.subject} | "
                f"{fact.predicate} | "
                f"{fact.object} "
                f"(source: {fact.source_reference}, "
                f"confidence: {fact.confidence})"
            )
            for fact in knowledge.facts
        )

        evidence = "\n".join(
            (
                f"- {item.content} "
                f"(source: {item.source_reference})"
            )
            for item in knowledge.evidence
        )

        return f"""
TARGET AUDIENCE:
{controls.target_audience}

TONE:
{controls.tone}

LANGUAGE:
{controls.language}

LEVEL OF DETAIL:
{controls.level_of_detail}

COMMUNICATION OBJECTIVE:
{controls.communication_objective}

CONTENT STYLE:
{controls.content_style}

FACT GRAPH:
{facts}

SOURCE EVIDENCE:
{evidence}

GLOBAL RULES:
1. Use only information supported by the Fact Graph or source evidence.
2. Never invent numbers, dates, names, events, or claims.
3. Preserve factual values exactly.
4. Follow all requested generation controls.
5. Do not mention the Fact Graph, RAG, or internal PRISM system.
6. If information is uncertain, do not present it as certain.
""".strip()
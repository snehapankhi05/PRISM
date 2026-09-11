from __future__ import annotations

from typing import Iterable


def format_facts(facts: Iterable) -> str:
    """
    Convert Fact Graph facts into a compact, readable context
    for output specialists.

    Specialists should use this as their authoritative factual source.
    """
    lines: list[str] = []

    for fact in facts:
        lines.append(
            f"- [{fact.category}] "
            f"{fact.subject} | {fact.predicate} | {fact.object} "
            f"(source: {fact.source_reference}, "
            f"confidence: {fact.confidence:.2f})"
        )

    return "\n".join(lines)


def format_evidence(evidence: Iterable) -> str:
    """
    Safely format RAG evidence.

    Supports both Evidence objects and dictionary-like values.
    """
    lines: list[str] = []

    for item in evidence:
        if isinstance(item, dict):
            content = item.get("content", "")
            source_reference = item.get("source_reference", "")
        else:
            content = getattr(item, "content", "")
            source_reference = getattr(item, "source_reference", "")

        if content:
            lines.append(
                f"- {content} "
                f"(source: {source_reference})"
            )

    return "\n".join(lines)


def build_shared_context(input_data) -> str:
    """
    Build the authoritative context shared by all specialists.
    """

    knowledge = input_data.knowledge_context
    controls = input_data.controls

    facts = format_facts(knowledge.facts)
    evidence = format_evidence(knowledge.evidence)

    return f"""
AUTHORITATIVE FACT GRAPH
========================

{facts or "No facts available."}

SUPPORTING SOURCE EVIDENCE
==========================

{evidence or "No additional evidence available."}

GENERATION CONTROLS
===================

Target audience: {controls.target_audience}
Tone: {controls.tone}
Language: {controls.language}
Level of detail: {controls.level_of_detail}
Communication objective: {controls.communication_objective}
Content style: {controls.content_style}
""".strip()
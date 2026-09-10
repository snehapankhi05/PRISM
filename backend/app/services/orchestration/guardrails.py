from backend.app.services.orchestration.state import PRISMState


def guardrails_node(
    state: PRISMState,
    *,
    basic_guardrail,
    factual_guardrail,
    llm_guardrail,
    revision_service=None,
    output_repository=None,
    provenance_service=None,
    db=None,
) -> PRISMState:
    outputs = state.get("generated_outputs", {})
    knowledge_context = state.get("knowledge_context")

    if knowledge_context is None:
        raise ValueError("Knowledge context is required for guardrails.")

    guardrail_results = {}
    final_outputs = {}

    verified_facts = getattr(knowledge_context, "facts", [])

    for output_type, output in outputs.items():

        # ---------------------------------------------------------
        # 1. Basic guardrail
        # ---------------------------------------------------------
        basic_result = basic_guardrail.evaluate(output)

        if not basic_result.passed:
            result = basic_result

        else:
            # -----------------------------------------------------
            # 2. Factual guardrail
            # -----------------------------------------------------
            factual_result = factual_guardrail.evaluate(
                output,
                knowledge_context,
            )

            if not factual_result.passed:
                result = factual_result

            else:
                # -------------------------------------------------
                # 3. LLM consistency guardrail
                # -------------------------------------------------
                result = llm_guardrail.evaluate(
                    output,
                    knowledge_context,
                )

        # ---------------------------------------------------------
        # 4. Bounded revision
        # ---------------------------------------------------------
        final_output = output

        if (
            result.revision_required
            and not result.passed
            and revision_service is not None
        ):
            feedback = "\n".join(
                issue.message
                for issue in result.issues
            )

            revised_output = revision_service.revise(
                output,
                feedback,
                verified_facts=verified_facts,
            )

            # -----------------------------------------------------
            # 5. Re-check revised output
            # -----------------------------------------------------
            revised_basic = basic_guardrail.evaluate(
                revised_output
            )

            if not revised_basic.passed:
                revised_result = revised_basic

            else:
                revised_factual = factual_guardrail.evaluate(
                    revised_output,
                    knowledge_context,
                )

                if not revised_factual.passed:
                    revised_result = revised_factual

                else:
                    revised_result = llm_guardrail.evaluate(
                        revised_output,
                        knowledge_context,
                    )

            final_output = revised_output
            result = revised_result

        # ---------------------------------------------------------
        # 6. Store final output and guardrail result
        # ---------------------------------------------------------
        final_outputs[output_type] = final_output
        guardrail_results[output_type] = result

        # ---------------------------------------------------------
        # 7. Persist FINAL output + provenance
        # ---------------------------------------------------------
        if (
            output_repository is not None
            and provenance_service is not None
            and db is not None
            and state.get("job_id")
            and state.get("source_id")
        ):
            content = final_output.content

            if hasattr(content, "model_dump_json"):
                content = content.model_dump_json()

            elif not isinstance(content, str):
                content = str(content)

            output_draft = output_repository.create(
                db,
                job_id=state["job_id"],
                output_type=output_type,
                content=content,
                quality_metadata={
                    **final_output.metadata,
                    "guardrail_passed": result.passed,
                    "guardrail_confidence": result.confidence,
                    "revision_required": result.revision_required,
                },
            )

            provenance_service.create_links(
                db,
                output_draft_id=output_draft.id,
                source_id=state["source_id"],
                output=final_output,
            )

    return {
        **state,
        "generated_outputs": final_outputs,
        "guardrail_results": guardrail_results,
    }
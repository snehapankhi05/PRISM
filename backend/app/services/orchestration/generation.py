from backend.app.services.orchestration.specialists.base import SpecialistInput
from backend.app.services.orchestration.state import PRISMState
from backend.app.services.orchestration.output_repository import OutputRepository


def generation_node(
    state: PRISMState,
    *,
    specialist_registry,
    output_repository: OutputRepository,
    db,
) -> PRISMState:

    knowledge_context = state.get("knowledge_context")
    controls = state.get("controls")
    requested_outputs = state.get("requested_outputs", [])
    job_id = state.get("job_id")

    if knowledge_context is None:
        raise ValueError("Knowledge context is required for generation.")

    if controls is None:
        raise ValueError("Generation controls are required.")

    if not requested_outputs:
        raise ValueError("At least one output type is required.")

    generated_outputs = {}

    specialist_input = SpecialistInput(
        knowledge_context=knowledge_context,
        controls=controls,
    )

    for output_type in requested_outputs:
        specialist = specialist_registry.get(output_type)

        output = specialist.generate(specialist_input)

        generated_outputs[output_type] = output

        content = output.content

        if hasattr(content, "model_dump_json"):
            content = content.model_dump_json()
        elif not isinstance(content, str):
            content = str(content)

        # Persist only when this generation is associated
        # with a real database Job.
        if job_id:
            output_repository.create(
                db,
                job_id=job_id,
                output_type=output_type,
                content=content,
                quality_metadata=output.metadata,
            )

    return {
        **state,
        "generated_outputs": generated_outputs,
    }
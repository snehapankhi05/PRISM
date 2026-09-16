from pathlib import Path

from backend.app.services.orchestration.state import PRISMState


def rendering_node(
    state: PRISMState,
    *,
    renderer_registry,
    output_root: Path,
) -> PRISMState:

    generated_outputs = state.get("generated_outputs", {})
    job_id = state.get("job_id")

    if not generated_outputs:
        raise ValueError("Generated outputs are required for rendering.")

    rendered_outputs = {}

    # Use the job ID when available so every execution gets its own
    # isolated output directory.
    if job_id:
        job_output_dir = output_root / str(job_id)
    else:
        job_output_dir = output_root / "preview"

    job_output_dir.mkdir(parents=True, exist_ok=True)

    for output_type, specialist_output in generated_outputs.items():

        if specialist_output is None:
            continue

        content = specialist_output.content

        renderer = renderer_registry.get(output_type)

        output_dir = job_output_dir / output_type

        rendered_result = renderer.render(
            content,
            output_dir,
        )

        rendered_outputs[output_type] = {
            "output_type": rendered_result.output_type,
            "file_path": str(rendered_result.file_path),
            "mime_type": rendered_result.mime_type,
            "metadata": rendered_result.metadata,
        }

    return {
        **state,
        "rendered_outputs": rendered_outputs,
    }
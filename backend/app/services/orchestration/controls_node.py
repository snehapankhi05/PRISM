from backend.app.services.orchestration.state import PRISMState


def controls_node(
    state: PRISMState,
    *,
    control_resolver,
) -> PRISMState:
    controls = state.get("controls")

    if controls is None:
        raise ValueError("Generation controls are required.")

    resolved_controls = control_resolver.resolve(controls)

    return {
        **state,
        "controls": resolved_controls,
    }
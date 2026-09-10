from backend.app.schemas.controls import GenerationControls
from backend.app.services.orchestration.controls import ControlResolver


def main():
    controls = GenerationControls(
        target_audience="General public",
        tone="Professional",
        language="English",
        level_of_detail="Medium",
        communication_objective="Inform",
        content_style="Clear and concise",
    )

    resolver = ControlResolver()
    resolved = resolver.resolve(controls)

    print("Control resolution successful.")
    print(resolved.model_dump())


if __name__ == "__main__":
    main()
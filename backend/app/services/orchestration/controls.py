from backend.app.schemas.controls import GenerationControls


class ControlResolver:
    def resolve(
        self,
        controls: GenerationControls,
    ) -> GenerationControls:
        return controls
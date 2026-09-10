from backend.app.services.orchestration.specialists.base import SpecialistAgent


class SpecialistRegistry:
    def __init__(self, specialists: list[SpecialistAgent]):
        self._specialists = {
            specialist.output_type: specialist
            for specialist in specialists
        }

    def get(self, output_type: str) -> SpecialistAgent:
        specialist = self._specialists.get(output_type)

        if specialist is None:
            raise ValueError(
                f"No specialist registered for output type: {output_type}"
            )

        return specialist

    def has(self, output_type: str) -> bool:
        return output_type in self._specialists

    def available_outputs(self) -> list[str]:
        return list(self._specialists.keys())
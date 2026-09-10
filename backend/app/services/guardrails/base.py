from abc import ABC, abstractmethod

from backend.app.schemas.guardrails import GuardrailResult
from backend.app.services.orchestration.specialists.base import SpecialistOutput


class GuardrailCritic(ABC):

    @abstractmethod
    def evaluate(
        self,
        output: SpecialistOutput,
    ) -> GuardrailResult:
        raise NotImplementedError
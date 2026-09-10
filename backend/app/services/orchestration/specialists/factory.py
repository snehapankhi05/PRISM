from backend.app.services.llm.base import LLMProvider
from backend.app.services.orchestration.specialists.advisory import AdvisorySpecialist
from backend.app.services.orchestration.specialists.executive_summary import (
    ExecutiveSummarySpecialist,
)
from backend.app.services.orchestration.specialists.infographic import InfographicSpecialist
from backend.app.services.orchestration.specialists.linkedin import LinkedInSpecialist
from backend.app.services.orchestration.specialists.presentation import PresentationSpecialist
from backend.app.services.orchestration.specialists.registry import SpecialistRegistry
from backend.app.services.orchestration.specialists.twitter import TwitterSpecialist
from backend.app.services.orchestration.specialists.video import VideoSpecialist


def build_specialist_registry(provider: LLMProvider) -> SpecialistRegistry:
    return SpecialistRegistry(
        [
            LinkedInSpecialist(provider),
            TwitterSpecialist(provider),
            AdvisorySpecialist(provider),
            ExecutiveSummarySpecialist(provider),
            PresentationSpecialist(provider),
            InfographicSpecialist(provider),
            VideoSpecialist(provider),
        ]
    )
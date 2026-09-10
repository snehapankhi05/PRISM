from backend.app.services.rendering.base import Renderer
from backend.app.services.rendering.text.linkedin import LinkedInRenderer
from backend.app.services.rendering.text.twitter import TwitterRenderer
from backend.app.services.rendering.text.advisory import AdvisoryRenderer
from backend.app.services.rendering.text.executive_summary import (
    ExecutiveSummaryRenderer,
)
from backend.app.services.rendering.presentation.pptx_renderer import (
    PresentationRenderer,
)
from backend.app.services.rendering.infographic.renderer import (
    InfographicRenderer,
)
from backend.app.services.rendering.video.renderer import VideoRenderer

class RendererRegistry:
    def __init__(self):
        self._renderers: dict[str, Renderer] = {}

    def register(self, renderer: Renderer) -> None:
        self._renderers[renderer.output_type] = renderer

    def get(self, output_type: str) -> Renderer:
        try:
            return self._renderers[output_type]
        except KeyError:
            raise ValueError(
                f"No renderer registered for output type: {output_type}"
            )

    def supported_outputs(self) -> list[str]:
        return list(self._renderers.keys())


def create_default_registry() -> RendererRegistry:
    registry = RendererRegistry()

    registry.register(LinkedInRenderer())
    registry.register(TwitterRenderer())
    registry.register(AdvisoryRenderer())
    registry.register(ExecutiveSummaryRenderer())
    registry.register(PresentationRenderer())
    registry.register(InfographicRenderer())
    registry.register(VideoRenderer())
    return registry


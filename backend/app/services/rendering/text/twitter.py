from pathlib import Path

from backend.app.services.rendering.base import RenderedResult, Renderer


class TwitterRenderer(Renderer):
    output_type = "twitter"

    def render(self, content, output_dir: Path) -> RenderedResult:
        output_dir.mkdir(parents=True, exist_ok=True)

        file_path = output_dir / "twitter.txt"
        file_path.write_text(str(content), encoding="utf-8")

        return RenderedResult(
            output_type=self.output_type,
            file_path=file_path,
            mime_type="text/plain",
        )
from pathlib import Path

from backend.app.schemas.generated_outputs import VideoContent
from backend.app.services.rendering.base import RenderedResult, Renderer


class VideoRenderer(Renderer):
    output_type = "video"

    def render(
        self,
        content: VideoContent,
        output_dir: Path,
    ) -> RenderedResult:
        output_dir.mkdir(parents=True, exist_ok=True)

        scenes_dir = output_dir / "scenes"
        scenes_dir.mkdir(exist_ok=True)

        scene_files = []

        for scene in content.scenes:
            scene_file = scenes_dir / f"scene_{scene.scene_number}.txt"

            scene_file.write_text(
                "\n".join(
                    [
                        f"TITLE: {scene.title}",
                        f"ON SCREEN: {scene.on_screen_text}",
                        f"NARRATION: {scene.narration}",
                        f"VISUAL: {scene.visual_direction}",
                        (
                            "SOURCES: "
                            + ", ".join(scene.source_references)
                        ),
                    ]
                ),
                encoding="utf-8",
            )

            scene_files.append(str(scene_file))

        manifest = output_dir / "video_manifest.txt"

        manifest.write_text(
            "\n".join(
                [
                    f"TITLE: {content.title}",
                    f"SCENES: {len(content.scenes)}",
                    "",
                    *scene_files,
                ]
            ),
            encoding="utf-8",
        )

        return RenderedResult(
            output_type=self.output_type,
            file_path=manifest,
            mime_type="text/plain",
            metadata={
                "scene_count": len(content.scenes),
                "render_mode": "presentation_manifest",
            },
        )
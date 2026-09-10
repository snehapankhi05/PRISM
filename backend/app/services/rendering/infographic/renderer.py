from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from backend.app.schemas.generated_outputs import InfographicContent
from backend.app.services.rendering.base import RenderedResult, Renderer


class InfographicRenderer(Renderer):
    output_type = "infographic"

    WIDTH = 1200
    PADDING = 60

    def render(
        self,
        content: InfographicContent,
        output_dir: Path,
    ) -> RenderedResult:
        output_dir.mkdir(parents=True, exist_ok=True)

        font_path = "C:/Windows/Fonts/arial.ttf"
        bold_font_path = "C:/Windows/Fonts/arialbd.ttf"

        title_font = ImageFont.truetype(bold_font_path, 48)
        subtitle_font = ImageFont.truetype(font_path, 26)
        heading_font = ImageFont.truetype(bold_font_path, 32)
        body_font = ImageFont.truetype(font_path, 24)

        height = 300 + len(content.sections) * 220

        image = Image.new("RGB", (self.WIDTH, height), "white")
        draw = ImageDraw.Draw(image)

        y = self.PADDING

        draw.text(
            (self.PADDING, y),
            content.title,
            font=title_font,
            fill="black",
        )
        y += 75

        if content.subtitle:
            draw.text(
                (self.PADDING, y),
                content.subtitle,
                font=subtitle_font,
                fill="gray",
            )
            y += 60

        for section in content.sections:
            draw.text(
                (self.PADDING, y),
                section.heading,
                font=heading_font,
                fill="black",
            )
            y += 50

            for point in section.key_points:
                draw.text(
                    (self.PADDING + 20, y),
                    f"• {point}",
                    font=body_font,
                    fill="black",
                )
                y += 40

            y += 35

        file_path = output_dir / "infographic.png"
        image.save(file_path)

        return RenderedResult(
            output_type=self.output_type,
            file_path=file_path,
            mime_type="image/png",
            metadata={
                "width": self.WIDTH,
                "height": height,
                "section_count": len(content.sections),
            },
        )
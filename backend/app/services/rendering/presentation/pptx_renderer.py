from pathlib import Path

from pptx import Presentation

from backend.app.schemas.generated_outputs import PresentationContent
from backend.app.services.rendering.base import RenderedResult, Renderer


class PresentationRenderer(Renderer):
    output_type = "presentation"

    def render(
        self,
        content: PresentationContent,
        output_dir: Path,
    ) -> RenderedResult:
        output_dir.mkdir(parents=True, exist_ok=True)

        presentation = Presentation()

        # Remove the default empty slide.
        if presentation.slides:
            slide_id = presentation.slides._sldIdLst[0].rId
            presentation.part.drop_rel(slide_id)
            del presentation.slides._sldIdLst[0]

        for slide_data in content.slides:
            slide = presentation.slides.add_slide(
                presentation.slide_layouts[1]
            )

            slide.shapes.title.text = slide_data.title

            text_frame = slide.placeholders[1].text_frame
            text_frame.clear()

            for index, point in enumerate(slide_data.content):
                paragraph = (
                    text_frame.paragraphs[0]
                    if index == 0
                    else text_frame.add_paragraph()
                )
                paragraph.text = point
                paragraph.level = 0

        file_path = output_dir / "presentation.pptx"
        presentation.save(file_path)

        return RenderedResult(
            output_type=self.output_type,
            file_path=file_path,
            mime_type=(
                "application/vnd.openxmlformats-officedocument."
                "presentationml.presentation"
            ),
            metadata={
                "slide_count": len(content.slides),
            },
        )
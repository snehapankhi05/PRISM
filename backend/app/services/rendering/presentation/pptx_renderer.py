from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt

from backend.app.schemas.generated_outputs import PresentationContent
from backend.app.services.rendering.base import RenderedResult, Renderer


class PresentationRenderer(Renderer):
    output_type = "presentation"

    # ---------------------------------------------------------
    # Theme
    # ---------------------------------------------------------

    NAVY = RGBColor(15, 23, 42)
    BLUE = RGBColor(37, 99, 235)
    LIGHT_BLUE = RGBColor(239, 246, 255)
    WHITE = RGBColor(255, 255, 255)
    BLACK = RGBColor(15, 23, 42)
    GRAY = RGBColor(71, 85, 105)
    LIGHT_GRAY = RGBColor(226, 232, 240)
    VERY_LIGHT = RGBColor(248, 250, 252)
    GREEN = RGBColor(22, 163, 74)

    FONT = "Aptos"

    # ---------------------------------------------------------
    # Main renderer
    # ---------------------------------------------------------

    def render(
        self,
        content: PresentationContent,
        output_dir: Path,
    ) -> RenderedResult:

        output_dir.mkdir(parents=True, exist_ok=True)

        presentation = Presentation()

        presentation.slide_width = Inches(13.333)
        presentation.slide_height = Inches(7.5)

        # Remove default slide.
        if presentation.slides:
            slide_id = presentation.slides._sldIdLst[0].rId
            presentation.part.drop_rel(slide_id)
            del presentation.slides._sldIdLst[0]

        # -----------------------------------------------------
        # Cover slide
        # -----------------------------------------------------

        self._add_cover_slide(
            presentation,
            content,
        )

        # -----------------------------------------------------
        # Content slides
        # -----------------------------------------------------

        for slide_data in content.slides:

            self._add_content_slide(
                presentation,
                slide_data,
            )

        # -----------------------------------------------------
        # Save
        # -----------------------------------------------------

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
                "slide_count": len(presentation.slides),
                "generated_slide_count": len(content.slides),
                "format": "pptx",
                "editable": True,
            },
        )

    # =========================================================
    # COVER
    # =========================================================

    def _add_cover_slide(
        self,
        presentation: Presentation,
        content: PresentationContent,
    ):

        slide = presentation.slides.add_slide(
            presentation.slide_layouts[6]
        )

        # Background
        background = slide.background.fill
        background.solid()
        background.fore_color.rgb = self.NAVY

        # Accent block
        accent = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0),
            Inches(0),
            Inches(0.18),
            Inches(7.5),
        )

        accent.fill.solid()
        accent.fill.fore_color.rgb = self.BLUE
        accent.line.fill.background()

        # PRISM label
        label = slide.shapes.add_textbox(
            Inches(1.0),
            Inches(0.85),
            Inches(3.0),
            Inches(0.4),
        )

        self._set_text(
            label.text_frame,
            "PRISM • GENERATED PRESENTATION",
            font_size=12,
            bold=True,
            color=self.BLUE,
        )

        # Title
        title = slide.shapes.add_textbox(
            Inches(1.0),
            Inches(1.65),
            Inches(10.8),
            Inches(1.8),
        )

        self._set_text(
            title.text_frame,
            content.title,
            font_size=34,
            bold=True,
            color=self.WHITE,
        )

        # Subtitle
        if content.subtitle:

            subtitle = slide.shapes.add_textbox(
                Inches(1.0),
                Inches(3.55),
                Inches(9.8),
                Inches(0.9),
            )

            self._set_text(
                subtitle.text_frame,
                content.subtitle,
                font_size=17,
                color=RGBColor(203, 213, 225),
            )

        # Audience
        if content.audience:

            audience = slide.shapes.add_textbox(
                Inches(1.0),
                Inches(5.55),
                Inches(7.5),
                Inches(0.55),
            )

            self._set_text(
                audience.text_frame,
                f"Prepared for • {content.audience}",
                font_size=12,
                color=RGBColor(148, 163, 184),
            )

        # Footer
        footer = slide.shapes.add_textbox(
            Inches(1.0),
            Inches(6.55),
            Inches(10),
            Inches(0.35),
        )

        self._set_text(
            footer.text_frame,
            "Generated from PRISM's structured content pipeline",
            font_size=10,
            color=RGBColor(100, 116, 139),
        )

    # =========================================================
    # CONTENT SLIDE
    # =========================================================

    def _add_content_slide(
        self,
        presentation: Presentation,
        slide_data,
    ):

        slide = presentation.slides.add_slide(
            presentation.slide_layouts[6]
        )

        # Background
        background = slide.background.fill
        background.solid()
        background.fore_color.rgb = self.VERY_LIGHT

        # Top accent
        top_bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            0,
            0,
            presentation.slide_width,
            Inches(0.08),
        )

        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = self.BLUE
        top_bar.line.fill.background()

        # Slide number
        number = slide.shapes.add_textbox(
            Inches(11.9),
            Inches(0.45),
            Inches(0.7),
            Inches(0.35),
        )

        self._set_text(
            number.text_frame,
            f"{slide_data.slide_number:02d}",
            font_size=11,
            bold=True,
            color=self.GRAY,
            align=PP_ALIGN.RIGHT,
        )

        # Title
        title = slide.shapes.add_textbox(
            Inches(0.75),
            Inches(0.55),
            Inches(9.8),
            Inches(0.75),
        )

        self._set_text(
            title.text_frame,
            slide_data.title,
            font_size=27,
            bold=True,
            color=self.BLACK,
        )

        # Subtitle
        if slide_data.subtitle:

            subtitle = slide.shapes.add_textbox(
                Inches(0.78),
                Inches(1.27),
                Inches(10.2),
                Inches(0.45),
            )

            self._set_text(
                subtitle.text_frame,
                slide_data.subtitle,
                font_size=12,
                color=self.GRAY,
            )

        # -----------------------------------------------------
        # Main content card
        # -----------------------------------------------------

        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.75),
            Inches(1.85),
            Inches(8.25),
            Inches(4.65),
        )

        card.fill.solid()
        card.fill.fore_color.rgb = self.WHITE

        card.line.color.rgb = self.LIGHT_GRAY
        card.line.width = Pt(1)

        # Content
        text_box = slide.shapes.add_textbox(
            Inches(1.05),
            Inches(2.15),
            Inches(7.65),
            Inches(4.05),
        )

        frame = text_box.text_frame
        frame.clear()
        frame.word_wrap = True

        for index, point in enumerate(slide_data.content):

            paragraph = (
                frame.paragraphs[0]
                if index == 0
                else frame.add_paragraph()
            )

            paragraph.text = point
            paragraph.level = 0

            paragraph.font.name = self.FONT
            paragraph.font.size = Pt(17)
            paragraph.font.color.rgb = self.BLACK

            paragraph.space_after = Pt(18)

            # Bullet
            paragraph.text = f"•  {point}"

        # -----------------------------------------------------
        # Right-side key statistic
        # -----------------------------------------------------

        if slide_data.key_stat:

            stat_card = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(9.35),
                Inches(1.85),
                Inches(3.2),
                Inches(2.25),
            )

            stat_card.fill.solid()
            stat_card.fill.fore_color.rgb = self.LIGHT_BLUE

            stat_card.line.color.rgb = RGBColor(
                191,
                219,
                254,
            )

            stat_label = slide.shapes.add_textbox(
                Inches(9.7),
                Inches(2.15),
                Inches(2.5),
                Inches(0.35),
            )

            self._set_text(
                stat_label.text_frame,
                "KEY STATISTIC",
                font_size=10,
                bold=True,
                color=self.BLUE,
            )

            stat_value = slide.shapes.add_textbox(
                Inches(9.65),
                Inches(2.65),
                Inches(2.55),
                Inches(1.05),
            )

            self._set_text(
                stat_value.text_frame,
                slide_data.key_stat,
                font_size=24,
                bold=True,
                color=self.NAVY,
                align=PP_ALIGN.CENTER,
            )

        # -----------------------------------------------------
        # Speaker notes
        # -----------------------------------------------------

        if slide_data.speaker_notes:

            notes_slide = slide.notes_slide

            notes_text = notes_slide.notes_text_frame

            notes_text.text = slide_data.speaker_notes

        # -----------------------------------------------------
        # Source reference footer
        # -----------------------------------------------------

        references = getattr(
            slide_data,
            "source_references",
            [],
        )

        if references:

            source_text = "Source: " + ", ".join(
                references[:3]
            )

            source_box = slide.shapes.add_textbox(
                Inches(9.35),
                Inches(4.55),
                Inches(3.15),
                Inches(1.15),
            )

            self._set_text(
                source_box.text_frame,
                source_text,
                font_size=9,
                color=self.GRAY,
            )

        # -----------------------------------------------------
        # Footer
        # -----------------------------------------------------

        footer = slide.shapes.add_textbox(
            Inches(0.75),
            Inches(6.85),
            Inches(11.8),
            Inches(0.3),
        )

        self._set_text(
            footer.text_frame,
            "PRISM • Provenance-Reasoned Intelligent Synthesis",
            font_size=9,
            color=self.GRAY,
        )

    # =========================================================
    # TEXT HELPERS
    # =========================================================

    def _set_text(
        self,
        text_frame,
        text: str,
        *,
        font_size: int,
        color,
        bold: bool = False,
        align=PP_ALIGN.LEFT,
    ):

        text_frame.clear()

        paragraph = text_frame.paragraphs[0]

        paragraph.text = text
        paragraph.alignment = align

        paragraph.font.name = self.FONT
        paragraph.font.size = Pt(font_size)
        paragraph.font.bold = bold
        paragraph.font.color.rgb = color

        text_frame.word_wrap = True
        text_frame.margin_left = 0
        text_frame.margin_right = 0
        text_frame.margin_top = 0
        text_frame.margin_bottom = 0
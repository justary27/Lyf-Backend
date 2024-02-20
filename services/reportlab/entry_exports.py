import io
from django.conf import settings

from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

from apps.diary.models import DiaryEntry


class EntryPDFGen:
    LINE_BREAK: str = "&nbsp;&nbsp;<br />"

    TITLE_STYLE: ParagraphStyle = ParagraphStyle(
        name="Title",
        # fontName="Ubuntu",
        fontSize=25,
        textColor=HexColor("#16856f")
    )

    DATE_STYLE: ParagraphStyle = ParagraphStyle(
        name="Date",
        # fontName="ABZee",
        fontSize=9,
        fontStyle="italic",
        textColor=HexColor("#ff5e0e")
    )

    DESCRIPTION_STYLE: ParagraphStyle = ParagraphStyle(
        name='Description',
        # fontName='ABZee',
        fontSize=10,
        leading=15,
        wordWrap="CJK",
        alignment=TA_JUSTIFY
    )

    def __init__(self, font_data: dict):
        self.diary = None
        self.canvas = None
        self.entry = None
        self.fileBuffer = None

        self.font_data = font_data

        self.register_font()

    @staticmethod
    def text_formatter(text: str):
        text = text.replace(' ', '&nbsp;')
        text = text.replace('\n', '<br />')
        text = text.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp')

        return text

    @staticmethod
    def add_page_number(canvas: Canvas, doc):
        page_number = canvas.getPageNumber()
        text = f"lyf | {page_number}"

        # canvas.setFont("Caveat", 18)
        canvas.setFillColorRGB(22 / 256, 133 / 256, 111 / 256)
        canvas.drawRightString(180 * mm, 17.5 * mm, text)

    def add_linebreaks(self, parts: list, newline_count: int = 1):
        i = 0
        while i < newline_count:
            parts.append(Paragraph(self.LINE_BREAK))
            i += 1

    def register_font(self):
        from reportlab.rl_settings import TTFSearchPath
        TTFSearchPath += (str(settings.BASE_DIR) + "/static/fonts", )

        for font in list(self.font_data.keys()):
            font_file = self.font_data.get(font)
            # new_font = TTFont(font, font_file)
            # pdfmetrics.registerFont(new_font)

    def draw_logo(self, canvas: Canvas, X, Y, width, height):

        # logoPath = str(settings.BASE_DIR) + "/static/assets/lyf.svg"
        # canvas.drawImage(
        #     logoPath,
        #      x=X,
        #      y=Y,
        #      width = width,
        #      height= height
        # )

        pass

    def generate_entry(self, entry: DiaryEntry, file_buffer: io.BytesIO):

        self.fileBuffer = file_buffer
        self.canvas = Canvas(self.fileBuffer, pagesize=A4)
        self.canvas.setCreator("Lyf")
        # self.drawLogo(canvas=self.canva,)

        parts = []

        title = self.text_formatter(entry.title)
        description = self.text_formatter(entry.description)

        date_text = entry.formatted_date()

        parts.append(Paragraph(date_text, style=self.DATE_STYLE))
        parts.append(Paragraph(title, style=self.TITLE_STYLE))

        self.add_linebreaks(parts, 3)

        parts.append(Paragraph(description, style=self.DESCRIPTION_STYLE))

        summary_name = SimpleDocTemplate(
            self.fileBuffer,
            title=entry.title,
            creator="Lyf",
            author=entry.created_by.username,
            subject=entry.created_by.username + "'s " + entry.title
        )
        summary_name.build(
            parts,
            onFirstPage=self.add_page_number,
            onLaterPages=self.add_page_number,
        )

        return self.fileBuffer

    def generate_diary(self, diary: list, file_buffer: io.BytesIO):

        self.fileBuffer = file_buffer
        self.canvas = Canvas(self.fileBuffer, pagesize=A4)
        self.canvas.setCreator("Lyf")

        template_entry: DiaryEntry = diary[0]
        parts: list = []

        for entry in diary:
            title = self.text_formatter(entry.title)
            date_text = entry.formatted_date()
            description = self.text_formatter(entry.description)

            parts.append(Paragraph(date_text, style=self.DATE_STYLE))
            parts.append(Paragraph(title, style=self.TITLE_STYLE))

            self.add_linebreaks(parts, 3)

            parts.append(Paragraph(description, style=self.DESCRIPTION_STYLE))
            self.add_linebreaks(parts)

        summary_name = SimpleDocTemplate(
            self.fileBuffer,
            title=template_entry.created_by.username + "'s Diary",
            creator="Lyf",
            author=template_entry.created_by.username,
            subject=template_entry.created_by.username + "'s " + template_entry.title
        )

        summary_name.build(
            parts,
            onFirstPage=self.add_page_number,
            onLaterPages=self.add_page_number,
        )

        return self.fileBuffer


fontData = {
    "ABZee": "ABeeZee-Regular.ttf",
    "Ubuntu": "Ubuntu-Regular.ttf",
    "Caveat": "Caveat-Regular.ttf"
}


# DiaryGenerator = EntryPDFGenerator(fontData=fontData)

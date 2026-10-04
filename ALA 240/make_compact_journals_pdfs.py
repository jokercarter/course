from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("Vera", r"C:\Users\cyuhe\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\reportlab\fonts\Vera.ttf"))
pdfmetrics.registerFont(TTFont("Vera-Bold", r"C:\Users\cyuhe\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\reportlab\fonts\VeraBd.ttf"))
pdfmetrics.registerFont(TTFont("Deng", r"C:\Windows\Fonts\Deng.ttf"))
pdfmetrics.registerFont(TTFont("Deng-Bold", r"C:\Windows\Fonts\Dengb.ttf"))


def clean_text(value: str) -> str:
    # Keep the PDF text portable and avoid non-ASCII dash glyphs.
    return value.replace("\u2013", "-").replace("\u2014", "-").replace("\u2011", "-")


def parse_entries(path: Path, zh: bool):
    text = path.read_text(encoding="utf-8")
    marker = r"(?m)^# Week (\d+) Journal[:：]\s*" if zh else r"(?m)^# Week (\d+) Journal:\s*"
    parts = re.split(marker, text)
    entries = []
    for index in range(1, len(parts), 2):
        week = parts[index]
        body = parts[index + 1]
        lines = body.strip().splitlines()
        title = clean_text(lines[0].strip())
        blocks = []
        current = []
        for line in lines[1:]:
            if line.startswith("## "):
                if current:
                    blocks.append(("paragraph", clean_text(" ".join(current))))
                    current = []
                blocks.append(("heading", clean_text(line[3:].strip())))
            elif line.strip():
                current.append(line.strip())
            elif current:
                blocks.append(("paragraph", clean_text(" ".join(current))))
                current = []
        if current:
            blocks.append(("paragraph", clean_text(" ".join(current))))
        entries.append((week, title, blocks))
    return entries


class CompactDocTemplate(BaseDocTemplate):
    def __init__(self, *args, header_titles, zh=False, **kwargs):
        self.header_titles = header_titles
        self.zh = zh
        super().__init__(*args, **kwargs)


def make_pdf(source: Path, output: Path, zh: bool):
    entries = parse_entries(source, zh=zh)
    if len(entries) != 5:
        raise RuntimeError(f"Expected 5 entries in {source.name}, found {len(entries)}")

    titles = [f"Week {week} Journal: {title}" for week, title, _ in entries]
    if zh:
        body_font = "Deng"
        bold_font = "Deng-Bold"
        footer_label = "ALA 240 - Journal 中文版"
        heading_color = colors.HexColor("#A23E48")
        word_wrap = "CJK"
        body_size, leading = 10.35, 15.2
        heading_size, heading_leading = 12.0, 15.0
        header_size = 13.2
    else:
        body_font = "Vera"
        bold_font = "Vera-Bold"
        footer_label = "ALA 240 - Journal Collection"
        heading_color = colors.HexColor("#A23E48")
        word_wrap = None
        body_size, leading = 7.8, 9.65
        heading_size, heading_leading = 10.2, 12.3
        header_size = 13.0

    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        name="CompactBody",
        fontName=body_font,
        fontSize=body_size,
        leading=leading,
        textColor=colors.HexColor("#1F2937"),
        alignment=TA_LEFT,
        spaceAfter=5.0,
        wordWrap=word_wrap,
    )
    heading_style = ParagraphStyle(
        name="CompactHeading",
        fontName=bold_font,
        fontSize=heading_size,
        leading=heading_leading,
        textColor=heading_color,
        spaceBefore=3.0,
        spaceAfter=4.0,
        keepWithNext=True,
        wordWrap=word_wrap,
    )

    def on_page(canvas, doc):
        page = canvas.getPageNumber()
        title = titles[page - 1] if 1 <= page <= len(titles) else "ALA 240 Journal"
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#17365D"))
        canvas.setFont(bold_font, header_size)
        canvas.drawString(doc.leftMargin, letter[1] - 0.45 * inch, title)
        canvas.setStrokeColor(colors.HexColor("#17365D"))
        canvas.setLineWidth(1.25)
        canvas.line(doc.leftMargin, letter[1] - 0.56 * inch, letter[0] - doc.rightMargin, letter[1] - 0.56 * inch)
        canvas.setStrokeColor(colors.HexColor("#D9DEE7"))
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, 0.45 * inch, letter[0] - doc.rightMargin, 0.45 * inch)
        canvas.setFillColor(colors.HexColor("#6B7280"))
        canvas.setFont(body_font, 7.2)
        canvas.drawString(doc.leftMargin, 0.27 * inch, footer_label)
        canvas.drawRightString(letter[0] - doc.rightMargin, 0.27 * inch, str(page))
        canvas.restoreState()

    left = 0.52 * inch
    right = 0.52 * inch
    bottom = 0.60 * inch
    top = 0.75 * inch
    gutter = 0.20 * inch
    frame_height = letter[1] - top - bottom
    frame_width = (letter[0] - left - right - gutter) / 2
    if zh:
        frames = [Frame(left, bottom, letter[0] - left - right, frame_height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="full")]
    else:
        frames = [
            Frame(left, bottom, frame_width, frame_height, leftPadding=0, rightPadding=4, topPadding=0, bottomPadding=0, id="left"),
            Frame(left + frame_width + gutter, bottom, frame_width, frame_height, leftPadding=4, rightPadding=0, topPadding=0, bottomPadding=0, id="right"),
        ]
    doc = CompactDocTemplate(
        str(output),
        pagesize=letter,
        leftMargin=left,
        rightMargin=right,
        topMargin=top,
        bottomMargin=bottom,
        header_titles=titles,
        zh=zh,
        title=("ALA 240 Journal Collection Chinese Version: Weeks 1-5" if zh else "ALA 240 Journal Collection: Weeks 1-5"),
        author="ALA 240 Student",
        subject=("Week 1-5 Chinese journal entries" if zh else "Week 1-5 journal entries"),
    )
    doc.addPageTemplates([PageTemplate(id="two-column", frames=frames, onPage=on_page)])

    story = []
    for index, (_, _, blocks) in enumerate(entries):
        if index:
            story.append(PageBreak())
        for kind, value in blocks:
            story.append(Paragraph(escape(value), heading_style if kind == "heading" else body_style))
    doc.build(story)


make_pdf(ROOT / "Week1-5_Journal_Drafts.md", OUT_DIR / "ALA240_Week1-5_Journals.pdf", zh=False)
make_pdf(ROOT / "Week1-5_Journal_Drafts_ZH.md", OUT_DIR / "ALA240_Week1-5_Journals_ZH.pdf", zh=True)
print(OUT_DIR / "ALA240_Week1-5_Journals.pdf")
print(OUT_DIR / "ALA240_Week1-5_Journals_ZH.pdf")

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

FONT_DIR = Path(
    r"C:\Users\cyuhe\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\reportlab\fonts"
)
pdfmetrics.registerFont(TTFont("Vera", str(FONT_DIR / "Vera.ttf")))
pdfmetrics.registerFont(TTFont("Vera-Bold", str(FONT_DIR / "VeraBd.ttf")))
pdfmetrics.registerFont(TTFont("SimHei", r"C:\Windows\Fonts\simhei.ttf"))
pdfmetrics.registerFont(TTFont("Deng-Bold", r"C:\Windows\Fonts\Dengb.ttf"))


def parse_entries(path: Path, zh: bool):
    text = path.read_text(encoding="utf-8")
    marker = r"(?m)^# Week (\d+) Journal[:：]\s*"
    parts = re.split(marker, text)
    entries = []
    for index in range(1, len(parts), 2):
        week = parts[index]
        body = parts[index + 1]
        lines = body.strip().splitlines()
        title = lines[0].strip()
        blocks = []
        current = []
        for line in lines[1:]:
            if line.startswith("*Draft assumption:"):
                continue
            if line.startswith("## "):
                if current:
                    joiner = "" if zh else " "
                    blocks.append(("paragraph", joiner.join(current)))
                    current = []
                blocks.append(("heading", line[3:].strip()))
            elif line.strip():
                current.append(line.strip())
            elif current:
                joiner = "" if zh else " "
                blocks.append(("paragraph", joiner.join(current)))
                current = []
        if current:
            joiner = "" if zh else " "
            blocks.append(("paragraph", joiner.join(current)))
        entries.append((week, title, blocks))
    return entries


def use_full_week2(compact_source: Path, full_source: Path, zh: bool):
    """Use the complete Week 2 response because Canvas labels Part One as two pages."""
    compact_entries = parse_entries(compact_source, zh=zh)
    full_entries = parse_entries(full_source, zh=zh)
    full_week2 = next((entry for entry in full_entries if entry[0] == "2"), None)
    if full_week2 is None:
        raise RuntimeError(f"Week 2 entry not found in {full_source.name}")
    return [full_week2 if entry[0] == "2" else entry for entry in compact_entries]


class JournalDocTemplate(BaseDocTemplate):
    pass


def make_pdf(source: Path, output: Path, zh: bool):
    full_source = ROOT / ("Week1-5_Journal_Drafts_ZH.md" if zh else "Week1-5_Journal_Drafts.md")
    entries = use_full_week2(source, full_source, zh=zh)
    if len(entries) != 5:
        raise RuntimeError(f"Expected five entries in {source.name}, found {len(entries)}")

    if zh:
        body_font = "SimHei"
        bold_font = "Deng-Bold"
        word_wrap = "CJK"
        footer_label = "ALA 240 · Journal 中文版"
        title_sep = "："
    else:
        body_font = "Vera"
        bold_font = "Vera-Bold"
        word_wrap = None
        footer_label = "ALA 240 · Journal Collection"
        title_sep = ": "

    # These sizes match the original journal PDFs. Only the content length is reduced.
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="JournalTitle",
        fontName=bold_font,
        fontSize=19,
        leading=25 if zh else 24,
        textColor=colors.HexColor("#17365D"),
        wordWrap=word_wrap,
        spaceAfter=8,
        keepWithNext=True,
    )
    heading_style = ParagraphStyle(
        name="JournalHeading",
        fontName=bold_font,
        fontSize=13 if zh else 12.5,
        leading=18 if zh else 17,
        textColor=colors.HexColor("#A23E48"),
        wordWrap=word_wrap,
        spaceBefore=4,
        spaceAfter=4,
        keepWithNext=True,
    )
    body_style = ParagraphStyle(
        name="JournalBody",
        fontName=body_font,
        fontSize=10.7 if zh else 10.3,
        leading=17 if zh else 15.4,
        textColor=colors.HexColor("#1F2937"),
        alignment=TA_LEFT,
        wordWrap=word_wrap,
        spaceAfter=5,
    )

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#D9DEE7"))
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, 0.62 * inch, letter[0] - doc.rightMargin, 0.62 * inch)
        canvas.setFont(body_font, 8)
        canvas.setFillColor(colors.HexColor("#6B7280"))
        canvas.drawString(doc.leftMargin, 0.42 * inch, footer_label)
        canvas.drawRightString(letter[0] - doc.rightMargin, 0.42 * inch, f"{doc.page}")
        canvas.restoreState()

    doc = JournalDocTemplate(
        str(output),
        pagesize=letter,
        leftMargin=0.82 * inch,
        rightMargin=0.82 * inch,
        topMargin=0.70 * inch,
        bottomMargin=0.72 * inch,
        title=("ALA 240 Journal Collection Chinese Version: Weeks 1-5" if zh else "ALA 240 Journal Collection: Weeks 1-5"),
        author="ALA 240 Student",
        subject=("Week 1-5 Chinese journal entries" if zh else "Week 1-5 journal entries"),
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="journal", frames=[frame], onPage=footer)])

    story = []
    for index, (week, title, blocks) in enumerate(entries):
        if index:
            story.append(PageBreak())
        story.append(Paragraph(escape(f"Week {week} Journal{title_sep}{title}"), title_style))
        for kind, value in blocks:
            style = heading_style if kind == "heading" else body_style
            story.append(Paragraph(escape(value), style))
    doc.build(story)


make_pdf(ROOT / "Week1-5_Journal_500w.md", OUT_DIR / "ALA240_Week1-5_Journals.pdf", zh=False)
make_pdf(ROOT / "Week1-5_Journal_500w_ZH.md", OUT_DIR / "ALA240_Week1-5_Journals_ZH.pdf", zh=True)
print(OUT_DIR / "ALA240_Week1-5_Journals.pdf")
print(OUT_DIR / "ALA240_Week1-5_Journals_ZH.pdf")

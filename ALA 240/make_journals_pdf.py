from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    PageBreak,
    Paragraph,
    Spacer,
)


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Week1-5_Journal_Drafts.md"
OUTPUT = ROOT / "output" / "pdf" / "ALA240_Week1-5_Journals.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

FONT_DIR = Path(
    r"C:\Users\cyuhe\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages\reportlab\fonts"
)
pdfmetrics.registerFont(TTFont("Vera", str(FONT_DIR / "Vera.ttf")))
pdfmetrics.registerFont(TTFont("Vera-Bold", str(FONT_DIR / "VeraBd.ttf")))


def parse_entries(text: str):
    entries = []
    parts = re.split(r"(?m)^# Week (\d+) Journal:\s*", text)
    for index in range(1, len(parts), 2):
        week_number = parts[index]
        body = parts[index + 1]
        lines = body.strip().splitlines()
        title = lines[0].strip()
        content_lines = lines[1:]
        cleaned = []
        for line in content_lines:
            if line.startswith("*Draft assumption:"):
                continue
            if line.strip() == "*":
                continue
            if line.startswith("## "):
                cleaned.append(("heading", line[3:].strip()))
            elif line.strip():
                cleaned.append(("text", line.strip()))
            else:
                cleaned.append(("blank", ""))
        blocks = []
        current = []
        for kind, value in cleaned:
            if kind == "heading":
                if current:
                    blocks.append(("paragraph", " ".join(current)))
                    current = []
                blocks.append(("heading", value))
            elif kind == "text":
                current.append(value)
            else:
                if current:
                    blocks.append(("paragraph", " ".join(current)))
                    current = []
        if current:
            blocks.append(("paragraph", " ".join(current)))
        entries.append((week_number, title, blocks))
    return entries


class JournalDocTemplate(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style_name = flowable.style.name
            if style_name in ("JournalTitle", "JournalHeading"):
                text = flowable.getPlainText()
                level = 0 if style_name == "JournalTitle" else 1
                key = f"h{level}-{self.page}-{len(text)}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=level, closed=False)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D9DEE7"))
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 0.62 * inch, letter[0] - doc.rightMargin, 0.62 * inch)
    canvas.setFont("Vera", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(doc.leftMargin, 0.42 * inch, "ALA 240 · Journal Collection")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.42 * inch, f"{doc.page}")
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        fontName="Vera-Bold",
        fontSize=25,
        leading=31,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        spaceAfter=14,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSubtitle",
        fontName="Vera",
        fontSize=12,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4B5563"),
    )
)
styles.add(
    ParagraphStyle(
        name="JournalTitle",
        fontName="Vera-Bold",
        fontSize=19,
        leading=24,
        textColor=colors.HexColor("#17365D"),
        spaceAfter=14,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="JournalHeading",
        fontName="Vera-Bold",
        fontSize=12.5,
        leading=17,
        textColor=colors.HexColor("#A23E48"),
        spaceBefore=8,
        spaceAfter=7,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="JournalBody",
        fontName="Vera",
        fontSize=10.3,
        leading=15.4,
        textColor=colors.HexColor("#1F2937"),
        alignment=TA_LEFT,
        spaceAfter=9,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverNote",
        fontName="Vera",
        fontSize=9.5,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#6B7280"),
        spaceBefore=20,
    )
)


entries = parse_entries(SOURCE.read_text(encoding="utf-8"))
if len(entries) != 5:
    raise RuntimeError(f"Expected 5 journal entries, found {len(entries)}")

doc = JournalDocTemplate(
    str(OUTPUT),
    pagesize=letter,
    leftMargin=0.82 * inch,
    rightMargin=0.82 * inch,
    topMargin=0.78 * inch,
    bottomMargin=0.8 * inch,
    title="ALA 240 Journal Collection: Weeks 1–5",
    author="ALA 240 Student",
    subject="Week 1–5 journal entries",
)
frame = Frame(
    doc.leftMargin,
    doc.bottomMargin,
    doc.width,
    doc.height,
    id="normal",
)
doc.addPageTemplates([PageTemplate(id="journal", frames=[frame], onPage=footer)])

story = []
story.append(Spacer(1, 1.55 * inch))
story.append(Paragraph("ALA 240 Journal Collection", styles["CoverTitle"]))
story.append(Paragraph("Weeks 1–5 · Fall 2026", styles["CoverSubtitle"]))
story.append(Spacer(1, 0.35 * inch))
story.append(Paragraph("Five reflective journal entries on wellbeing, mindfulness, identity, community, and success and failure.", styles["CoverSubtitle"]))
story.append(Paragraph("Each entry follows the corresponding Canvas prompt and is approximately 800 words.", styles["CoverNote"]))
story.append(PageBreak())

for index, (week_number, title, blocks) in enumerate(entries):
    if index:
        story.append(PageBreak())
    story.append(Paragraph(f"Week {week_number} Journal: {escape(title)}", styles["JournalTitle"]))
    for kind, value in blocks:
        if kind == "heading":
            story.append(Paragraph(escape(value), styles["JournalHeading"]))
        else:
            story.append(Paragraph(escape(value), styles["JournalBody"]))

doc.build(story)
print(OUTPUT)

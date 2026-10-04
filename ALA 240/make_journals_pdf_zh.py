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
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Week1-5_Journal_Drafts_ZH.md"
OUTPUT = ROOT / "output" / "pdf" / "ALA240_Week1-5_Journals_ZH.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont("SimHei", r"C:\Windows\Fonts\simhei.ttf"))
pdfmetrics.registerFont(TTFont("Deng-Bold", r"C:\Windows\Fonts\Dengb.ttf"))


def parse_entries(text: str):
    parts = re.split(r"(?m)^# Week (\d+) Journal[:：]\s*", text)
    entries = []
    for index in range(1, len(parts), 2):
        week_number = parts[index]
        body = parts[index + 1]
        lines = body.strip().splitlines()
        title = lines[0].strip()
        blocks = []
        current = []
        for line in lines[1:]:
            if line.startswith("## "):
                if current:
                    blocks.append(("paragraph", "".join(current)))
                    current = []
                blocks.append(("heading", line[3:].strip()))
            elif line.strip():
                current.append(line.strip())
            elif current:
                blocks.append(("paragraph", "".join(current)))
                current = []
        if current:
            blocks.append(("paragraph", "".join(current)))
        entries.append((week_number, title, blocks))
    return entries


class JournalDocTemplate(BaseDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            if flowable.style.name in ("JournalTitle", "JournalHeading"):
                text = flowable.getPlainText()
                level = 0 if flowable.style.name == "JournalTitle" else 1
                key = f"h{level}-{self.page}-{len(text)}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=level, closed=False)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D9DEE7"))
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 0.62 * inch, letter[0] - doc.rightMargin, 0.62 * inch)
    canvas.setFont("SimHei", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(doc.leftMargin, 0.42 * inch, "ALA 240 · Journal 中文版")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.42 * inch, f"{doc.page}")
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        fontName="Deng-Bold",
        fontSize=25,
        leading=32,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        wordWrap="CJK",
        spaceAfter=14,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSubtitle",
        fontName="SimHei",
        fontSize=12,
        leading=19,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4B5563"),
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="JournalTitle",
        fontName="Deng-Bold",
        fontSize=19,
        leading=25,
        textColor=colors.HexColor("#17365D"),
        wordWrap="CJK",
        spaceAfter=14,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="JournalHeading",
        fontName="Deng-Bold",
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#A23E48"),
        wordWrap="CJK",
        spaceBefore=8,
        spaceAfter=7,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="JournalBody",
        fontName="SimHei",
        fontSize=10.7,
        leading=17,
        textColor=colors.HexColor("#1F2937"),
        alignment=TA_LEFT,
        wordWrap="CJK",
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverNote",
        fontName="SimHei",
        fontSize=9.5,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#6B7280"),
        wordWrap="CJK",
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
    title="ALA 240 Journal Collection Chinese Version: Weeks 1-5",
    author="ALA 240 Student",
    subject="Week 1-5 Chinese journal entries",
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
doc.addPageTemplates([PageTemplate(id="journal", frames=[frame], onPage=footer)])

story = [
    Spacer(1, 1.45 * inch),
    Paragraph("ALA 240 Journal 中文版", styles["CoverTitle"]),
    Paragraph("Week 1-5 · 2026 秋季", styles["CoverSubtitle"]),
    Spacer(1, 0.35 * inch),
    Paragraph("五篇关于幸福感、正念、身份、社区以及成功与失败的反思日志。", styles["CoverSubtitle"]),
    Paragraph("本文件保留原有 Canvas Journal 的章节结构，并提供完整中文翻译。", styles["CoverNote"]),
    PageBreak(),
]

for index, (week_number, title, blocks) in enumerate(entries):
    if index:
        story.append(PageBreak())
    story.append(Paragraph(f"Week {week_number} Journal：{escape(title)}", styles["JournalTitle"]))
    for kind, value in blocks:
        style = styles["JournalHeading"] if kind == "heading" else styles["JournalBody"]
        story.append(Paragraph(escape(value), style))

doc.build(story)
print(OUTPUT)

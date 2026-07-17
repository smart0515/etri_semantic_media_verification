from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


PROJECT_TITLE = "ETRI 시맨틱 미디어 검증시스템"
VERSION = "v0.1.0-report"


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Malgun", r"C:\Windows\Fonts\malgun.ttf"))
    pdfmetrics.registerFont(TTFont("Malgun-Bold", r"C:\Windows\Fonts\malgunbd.ttf"))
    consolas = Path(r"C:\Windows\Fonts\consola.ttf")
    if consolas.exists():
        pdfmetrics.registerFont(TTFont("Consolas", str(consolas)))
    else:
        pdfmetrics.registerFont(TTFont("Consolas", r"C:\Windows\Fonts\malgun.ttf"))
    pdfmetrics.registerFontFamily(
        "Malgun", normal="Malgun", bold="Malgun-Bold", italic="Malgun", boldItalic="Malgun-Bold"
    )


class ReportDocument(BaseDocTemplate):
    def __init__(self, filename: str) -> None:
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=19 * mm,
            bottomMargin=18 * mm,
            title="의미 기반 미디어 전송 검증시스템 용역결과보고서",
            author="ETRI 용역 수행 결과물",
            subject="보고 단계 설계 및 사전검증 결과",
        )
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="body",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates([PageTemplate(id="report", frames=[frame], onPage=draw_page)])


def draw_page(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    if doc.page > 1:
        canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, height - 13 * mm, width - doc.rightMargin, height - 13 * mm)
        canvas.setFont("Malgun", 7.5)
        canvas.setFillColor(colors.HexColor("#64748B"))
        canvas.drawString(doc.leftMargin, height - 10.5 * mm, PROJECT_TITLE)
        canvas.drawRightString(width - doc.rightMargin, height - 10.5 * mm, VERSION)
    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.line(doc.leftMargin, 12 * mm, width - doc.rightMargin, 12 * mm)
    canvas.setFont("Malgun", 7.5)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(doc.leftMargin, 8.7 * mm, "보고용 납품본 | PRELIMINARY_MOCK 수치는 실제 ETRI 성능이 아님")
    canvas.drawRightString(width - doc.rightMargin, 8.7 * mm, str(doc.page))
    canvas.restoreState()


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    navy = colors.HexColor("#17365D")
    blue = colors.HexColor("#1D4ED8")
    slate = colors.HexColor("#334155")
    styles = {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=base["Title"],
            fontName="Malgun-Bold",
            fontSize=24,
            leading=34,
            textColor=navy,
            alignment=TA_CENTER,
            spaceBefore=42 * mm,
            spaceAfter=8 * mm,
            wordWrap="CJK",
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle",
            parent=base["Normal"],
            fontName="Malgun",
            fontSize=13,
            leading=20,
            textColor=slate,
            alignment=TA_CENTER,
            spaceAfter=14 * mm,
            wordWrap="CJK",
        ),
        "h1": ParagraphStyle(
            "Heading1Ko",
            parent=base["Heading1"],
            fontName="Malgun-Bold",
            fontSize=17,
            leading=24,
            textColor=navy,
            spaceBefore=7 * mm,
            spaceAfter=3 * mm,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "h2": ParagraphStyle(
            "Heading2Ko",
            parent=base["Heading2"],
            fontName="Malgun-Bold",
            fontSize=12.5,
            leading=18,
            textColor=blue,
            spaceBefore=5 * mm,
            spaceAfter=2 * mm,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "h3": ParagraphStyle(
            "Heading3Ko",
            parent=base["Heading3"],
            fontName="Malgun-Bold",
            fontSize=10.5,
            leading=16,
            textColor=slate,
            spaceBefore=3.5 * mm,
            spaceAfter=1.5 * mm,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "body": ParagraphStyle(
            "BodyKo",
            parent=base["BodyText"],
            fontName="Malgun",
            fontSize=9.2,
            leading=15.2,
            textColor=colors.HexColor("#1F2937"),
            alignment=TA_JUSTIFY,
            spaceAfter=2.2 * mm,
            wordWrap="CJK",
            splitLongWords=True,
        ),
        "bullet": ParagraphStyle(
            "BulletKo",
            parent=base["BodyText"],
            fontName="Malgun",
            fontSize=9,
            leading=14.5,
            leftIndent=6 * mm,
            firstLineIndent=-3.5 * mm,
            bulletIndent=1.5 * mm,
            spaceAfter=1.2 * mm,
            wordWrap="CJK",
        ),
        "number": ParagraphStyle(
            "NumberKo",
            parent=base["BodyText"],
            fontName="Malgun",
            fontSize=9,
            leading=14.5,
            leftIndent=7 * mm,
            firstLineIndent=-5 * mm,
            bulletIndent=1 * mm,
            spaceAfter=1.2 * mm,
            wordWrap="CJK",
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=base["BodyText"],
            fontName="Malgun-Bold",
            fontSize=7.5,
            leading=10.5,
            textColor=colors.white,
            alignment=TA_CENTER,
            wordWrap="CJK",
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            parent=base["BodyText"],
            fontName="Malgun",
            fontSize=7.25,
            leading=10.3,
            textColor=colors.HexColor("#1F2937"),
            alignment=TA_LEFT,
            wordWrap="CJK",
            splitLongWords=True,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Consolas",
            fontSize=6.8,
            leading=9.5,
            leftIndent=4 * mm,
            rightIndent=4 * mm,
            spaceBefore=2 * mm,
            spaceAfter=3 * mm,
            backColor=colors.HexColor("#F1F5F9"),
            borderColor=colors.HexColor("#CBD5E1"),
            borderWidth=0.5,
            borderPadding=4,
        ),
    }
    return styles


def inline_markup(text: str) -> str:
    escaped = html.escape(text.strip())
    escaped = re.sub(r"`([^`]+)`", r'<font name="Consolas" color="#0F4C81">\1</font>', escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", escaped)
    return escaped


def visual_len(value: str) -> int:
    return sum(2 if ord(char) > 127 else 1 for char in re.sub(r"[`*]", "", value))


def table_widths(rows: list[list[str]], available: float) -> list[float]:
    column_count = max(len(row) for row in rows)
    weights: list[float] = []
    for column in range(column_count):
        maximum = max(visual_len(row[column]) if column < len(row) else 0 for row in rows)
        weights.append(float(max(5, min(maximum, 42))))
    total = sum(weights)
    minimum = 18 * mm
    widths = [max(minimum, available * weight / total) for weight in weights]
    scale = available / sum(widths)
    return [width * scale for width in widths]


def build_table(raw_rows: list[list[str]], styles: dict[str, ParagraphStyle], available: float) -> Table:
    normalized: list[list[str]] = []
    column_count = max(len(row) for row in raw_rows)
    for row in raw_rows:
        normalized.append(row + [""] * (column_count - len(row)))
    data = []
    for row_index, row in enumerate(normalized):
        style = styles["table_header"] if row_index == 0 else styles["table_cell"]
        data.append([Paragraph(inline_markup(cell), style) for cell in row])
    table = Table(
        data,
        colWidths=table_widths(normalized, available),
        repeatRows=1,
        hAlign="LEFT",
        splitByRow=1,
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3.2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ]
        )
    )
    return table


def parse_markdown(source: Path, styles: dict[str, ParagraphStyle], available: float):
    lines = source.read_text(encoding="utf-8").splitlines()
    story = []
    index = 0
    first_heading = True
    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if stripped == "<!-- PAGEBREAK -->":
            story.append(PageBreak())
            index += 1
            continue
        if stripped.startswith("<!--"):
            index += 1
            continue
        if stripped.startswith("```"):
            code_lines = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index].rstrip())
                index += 1
            index += 1
            story.append(Preformatted("\n".join(code_lines), styles["code"], maxLineLength=96))
            continue
        if stripped.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1
            raw_rows = []
            for table_line in table_lines:
                cells = [cell.strip() for cell in table_line.strip("|").split("|")]
                if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                    continue
                raw_rows.append(cells)
            if raw_rows:
                story.append(build_table(raw_rows, styles, available))
                story.append(Spacer(1, 3 * mm))
            continue
        if stripped.startswith("### "):
            story.append(Paragraph(inline_markup(stripped[4:]), styles["h3"]))
            index += 1
            continue
        if stripped.startswith("## "):
            style = styles["subtitle"] if first_heading else styles["h2"]
            story.append(Paragraph(inline_markup(stripped[3:]), style))
            index += 1
            continue
        if stripped.startswith("# "):
            if first_heading:
                story.append(Paragraph(inline_markup(stripped[2:]), styles["title"]))
                first_heading = False
            else:
                story.append(Paragraph(inline_markup(stripped[2:]), styles["h1"]))
                story.append(HRFlowable(width="100%", thickness=0.7, color=colors.HexColor("#93C5FD")))
                story.append(Spacer(1, 1.5 * mm))
            index += 1
            continue
        if stripped.startswith("- [x] ") or stripped.startswith("- [ ] "):
            checked = stripped.startswith("- [x] ")
            text = stripped[6:]
            story.append(
                Paragraph(inline_markup(text), styles["bullet"], bulletText="☑" if checked else "☐")
            )
            index += 1
            continue
        if stripped.startswith("- "):
            story.append(Paragraph(inline_markup(stripped[2:]), styles["bullet"], bulletText="•"))
            index += 1
            continue
        numbered = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if numbered:
            story.append(
                Paragraph(inline_markup(numbered.group(2)), styles["number"], bulletText=f"{numbered.group(1)}.")
            )
            index += 1
            continue
        if stripped.startswith("> "):
            story.append(
                Paragraph(
                    inline_markup(stripped[2:]),
                    ParagraphStyle(
                        "Callout",
                        parent=styles["body"],
                        backColor=colors.HexColor("#EFF6FF"),
                        borderColor=colors.HexColor("#60A5FA"),
                        borderWidth=0.8,
                        borderPadding=7,
                        leftIndent=3 * mm,
                        rightIndent=3 * mm,
                        spaceBefore=2 * mm,
                        spaceAfter=3 * mm,
                    ),
                )
            )
            index += 1
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index].strip()
            if not candidate:
                break
            if (
                candidate.startswith("#")
                or candidate.startswith("|")
                or candidate.startswith("```")
                or candidate.startswith("- ")
                or candidate.startswith("> ")
                or candidate == "<!-- PAGEBREAK -->"
                or re.match(r"^\d+\.\s+", candidate)
            ):
                break
            paragraph_lines.append(candidate)
            index += 1
        story.append(Paragraph(inline_markup(" ".join(paragraph_lines)), styles["body"]))
    return story


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    register_fonts()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    document = ReportDocument(str(args.output))
    styles = make_styles()
    story = parse_markdown(args.source, styles, document.width)
    document.build(story)
    print(f"created {args.output}")


if __name__ == "__main__":
    main()

"""Generate Argus-Project-Proposal.docx from proposal/argus-proposal.md.
Formal black-on-white layout; the .md stays the single source of truth."""

import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, RGBColor, Cm

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "proposal" / "argus-proposal.md"
OUT = ROOT / "proposal" / "Argus-Project-Proposal.docx"

BLACK = RGBColor(0, 0, 0)
BODY_FONT = "Calibri"
BODY_SIZE = Pt(11)


def set_border_bottom(paragraph, size=8, space=4):
    p_pr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), str(space))
    bottom.set(qn("w:color"), "000000")
    borders.append(bottom)
    p_pr.append(borders)


def add_page_number_footer(section, label):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(label)
    run.font.size = Pt(9)
    run.font.color.rgb = BLACK
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    p._p.append(fld)


def add_md_runs(paragraph, text):
    """Minimal inline markdown: **bold** and `code`, all black."""
    for tok in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text):
        if not tok:
            continue
        if tok.startswith("**"):
            run = paragraph.add_run(tok[2:-2])
            run.bold = True
        elif tok.startswith("`"):
            run = paragraph.add_run(tok[1:-1])
            run.font.name = "Consolas"
            run.font.size = Pt(10)
        else:
            paragraph.add_run(tok)
        for run in paragraph.runs:
            run.font.color.rgb = BLACK


def meta_table(doc, rows):
    table = doc.add_table(rows=len(rows), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False
    widths = (Cm(3.4), Cm(12.6))
    for i, (label, value) in enumerate(rows):
        for j, width in enumerate(widths):
            cell = table.cell(i, j)
            cell.width = width
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            run = p.add_run(label if j == 0 else value)
            run.bold = j == 0
            run.font.size = Pt(10.5)
            run.font.color.rgb = BLACK
    return table


def section_heading(doc, text, size=13):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.bold = True
    run.font.size = Pt(size)
    run.font.color.rgb = BLACK
    set_border_bottom(h)
    return h


def body_paragraph(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    add_md_runs(p, text)
    return p


def main():
    md = SRC.read_text(encoding="utf-8")
    parts = re.split(r"\n## ", "\n" + md)
    annex_idx = next(i for i, p in enumerate(parts) if p.lstrip().startswith("Annex"))
    answers = [p for p in parts[1:annex_idx]]
    annex = parts[annex_idx]

    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = BODY_SIZE
    normal.font.color.rgb = BLACK
    for section in doc.sections:
        section.page_height = Cm(29.7)
        section.page_width = Cm(21.0)
        section.top_margin = section.bottom_margin = Cm(2.4)
        section.left_margin = section.right_margin = Cm(2.6)
        add_page_number_footer(section, "Argus — Project Proposal · UGREEN Hackathon 2026 · ")

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t.paragraph_format.space_after = Pt(2)
    run = t.add_run("PROJECT PROPOSAL")
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = BLACK

    t2 = doc.add_paragraph()
    t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t2.paragraph_format.space_after = Pt(2)
    run = t2.add_run("Argus — AI Steward for UGREEN AI NAS")
    run.bold = True
    run.font.size = Pt(22)
    run.font.color.rgb = BLACK

    t3 = doc.add_paragraph()
    t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t3.paragraph_format.space_after = Pt(12)
    run = t3.add_run("UGREEN Hackathon 2026 on AI NAS · Round 1 Submission")
    run.font.size = Pt(11)
    run.font.color.rgb = BLACK
    set_border_bottom(t3, size=12, space=8)

    doc.add_paragraph()
    meta_table(doc, [
        ("Track", "Open Innovation"),
        ("Entrant", "Helmut Chaparro Sandoval — individual entry"),
        ("Residence", "Bogotá D.C., Colombia"),
        ("Deliverable", "AI Skill package per the Uliya Skill Development Standard (Markdown-only)"),
    ])
    doc.add_paragraph()

    for part in answers:
        heading, _, body = part.partition("\n")
        heading = heading.strip()
        section_heading(doc, heading, size=12)
        for line in body.splitlines():
            line = line.strip()
            if not line or line.startswith(">"):
                continue
            body_paragraph(doc, line)

    doc.add_page_break()
    section_heading(doc, "Annex — Declarations (outside the 500-word limit)", size=13)
    for line in annex.splitlines()[1:]:
        line = line.strip()
        if not line or line.startswith("---"):
            continue
        if line.startswith("### "):
            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after = Pt(2)
            run = h.add_run(line[4:])
            run.bold = True
            run.font.size = Pt(11.5)
            run.font.color.rgb = BLACK
        elif line.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(3)
            add_md_runs(p, line[2:])
            for run in p.runs:
                run.font.color.rgb = BLACK
        else:
            body_paragraph(doc, line)

    doc.save(OUT)
    print(f"written: {OUT}")


if __name__ == "__main__":
    sys.exit(main())

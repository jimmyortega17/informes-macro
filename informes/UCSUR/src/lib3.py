import os, sys, json
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

S = os.path.dirname(os.path.abspath(__file__)); FIG = os.path.join(S, "fig2")
OUT = sys.argv[1] if len(sys.argv) > 1 else None
PAGES = json.load(open(sys.argv[2])) if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else {}
def pg2():
    a = PAGES.get("razint", ["?"])[0]; b = PAGES.get("razperu", ["?"])[0]
    return f"(págs. {a} y {b})"
NOMARK = "--final" in sys.argv
def pg(key):
    a, b = PAGES.get(key, ["?", "?"])
    return f"(pág. {a})" if a == b else f"(págs. {a}-{b})"

ROJO = RGBColor(0xC0, 0x00, 0x00); NEGRO = RGBColor(0, 0, 0); FONT = "Calibri"; SZ = 11
doc = Document()
sec = doc.sections[0]; sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"): setattr(sec, m, Cm(2.54))

def set_font_style(s, bold=None):
    s.font.name = FONT; s.font.size = Pt(SZ); s.font.color.rgb = NEGRO
    if bold is not None: s.font.bold = bold
    rpr = s.element.get_or_add_rPr(); rf = rpr.find(qn("w:rFonts"))
    if rf is None: rf = OxmlElement("w:rFonts"); rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"): rf.set(qn(a), FONT)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]
set_font_style(doc.styles["Normal"])
doc.styles["Normal"].paragraph_format.space_after = Pt(6); doc.styles["Normal"].paragraph_format.line_spacing = 1.15
for h in ("Heading 1", "Heading 2"):
    st = doc.styles[h]; set_font_style(st, True); st.font.italic = False
    st.paragraph_format.space_before = Pt(12); st.paragraph_format.space_after = Pt(6); st.paragraph_format.keep_with_next = True
# rPrDefault también en Calibri 11
rd = doc.styles.element.find(qn("w:docDefaults")).find(qn("w:rPrDefault")).find(qn("w:rPr"))
rf = rd.find(qn("w:rFonts"))
for a in list(rf.attrib): del rf.attrib[a]
for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"): rf.set(qn(a), FONT)
for t in ("w:sz", "w:szCs"):
    e = rd.find(qn(t))
    if e is None: e = OxmlElement(t); rd.append(e)
    e.set(qn("w:val"), str(SZ * 2))

def run(p, text, bold=False, italic=False, color=None):
    r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.name = FONT; r.font.size = Pt(SZ)
    if color: r.font.color.rgb = color
    return r
def P(text="", bold=False, color=None, align=None, italic=False, after=None, keep=False):
    p = doc.add_paragraph()
    if text: run(p, text, bold, italic, color)
    if align is not None: p.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    if keep: p.paragraph_format.keep_with_next = True
    return p
T = lambda t: P(t)
def EQ(t): return P(t, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, after=4)
def CAP(t): return P(t, bold=True, keep=True, after=3)
def SRC(t): return P("Fuente: " + t, after=8)
def INT(t): return P(t, bold=True)
def SUB(t): return P(t, bold=True, keep=True)
def H1(t): return doc.add_heading(t, level=1)
def H2(t): return doc.add_heading(t, level=2)
def CRIT(t):
    p = doc.add_paragraph(); run(p, "RAZONAMIENTO CRÍTICO: ", True); run(p, t, True)
def ESTR(t):
    p = doc.add_paragraph(); run(p, "RAZONAMIENTO ESTRATÉGICO: ", True, color=ROJO); run(p, t, True, color=ROJO)
def IMG(name, w=6.2):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(os.path.join(FIG, name), width=Inches(w))

def borders(cell, **kw):
    tcPr = cell._tc.get_or_add_tcPr(); b = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{side}"); v = kw.get(side)
        if v: e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(v)); e.set(qn("w:color"), "000000")
        else: e.set(qn("w:val"), "nil")
        b.append(e)
    tcPr.append(b)
def fix_widths(t, widths):
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); t._tbl.tblPr.append(lay)
    for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), widths): gc.set(qn("w:w"), str(int(int(w) / 635)))
    for row in t.rows:
        for c, w in zip(row.cells, widths): c.width = Emu(int(w))
def cell_lines(cell, lines, align=WD_ALIGN_PARAGRAPH.CENTER):
    cell.text = ""
    for k, (txt, b) in enumerate(lines):
        p = cell.paragraphs[0] if k == 0 else cell.add_paragraph()
        p.alignment = align; p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.0
        run(p, txt, b)

def CADENA(titulo, elems, nota=None):
    """elems: lista de (notación, cifra). Caja única con flechas, estilo de la guía del profesor."""
    CAP(titulo)
    n = len(elems) * 2 - 1
    t = doc.add_table(rows=1, cols=n); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    aw = Inches(0.17); ew = Emu(int((Inches(6.5) - aw * (len(elems) - 1)) / len(elems)))
    widths = []
    for i in range(n):
        c = t.rows[0].cells[i]
        top = 12; left = 12 if i == 0 else None; right = 12 if i == n - 1 else None
        if i % 2 == 0:
            no, ci = elems[i // 2]; cell_lines(c, [(no, True), (ci, False)]); widths.append(ew)
        else:
            cell_lines(c, [("→", True)]); widths.append(aw)
        borders(c, top=top, bottom=12, left=left, right=right)
    fix_widths(t, widths)
    mar = OxmlElement("w:tblCellMar")
    for side in ("left", "right"):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:w"), "30"); e.set(qn("w:type"), "dxa"); mar.append(e)
    t._tbl.tblPr.append(mar)
    trPr = t.rows[0]._tr.get_or_add_trPr(); cs = OxmlElement("w:cantSplit"); trPr.append(cs)
    for c in t.rows[0].cells:
        for p in c.paragraphs: p.paragraph_format.keep_with_next = True
    if nota: P(nota, after=8)

def APA(header, rows, widths):
    t = doc.add_table(rows=len(rows) + 1, cols=len(header)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for j, h in enumerate(header):
        c = t.rows[0].cells[j]; cell_lines(c, [(h, False)], WD_ALIGN_PARAGRAPH.CENTER if j else WD_ALIGN_PARAGRAPH.LEFT); borders(c, top=12, bottom=6)
    for i, row in enumerate(rows, 1):
        for j, v in enumerate(row):
            c = t.rows[i].cells[j]; cell_lines(c, [(v, False)], WD_ALIGN_PARAGRAPH.CENTER if j else WD_ALIGN_PARAGRAPH.LEFT)
            borders(c, bottom=12 if i == len(rows) else None)
    fix_widths(t, [Inches(w) for w in widths])

def MARK(key):  # marcador invisible para localizar páginas en el PDF
    if NOMARK: return
    p = doc.paragraphs[-1]; r = p.add_run(f"⟦{key}⟧"); r.font.size = Pt(1); r.font.color.rgb = RGBColor(255, 255, 255)


import os, sys, json
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

S = os.path.dirname(os.path.abspath(__file__)); FIG = os.path.join(S, "fig2")
OUT = sys.argv[1]
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

# ================= CARÁTULA =================
for txt in ("PONTIFICIA UNIVERSIDAD CATÓLICA DEL PERÚ", "ESCUELA DE POSGRADO"): P(txt, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = Pt(18)
p.add_run().add_picture(os.path.join(S, "logo", "word", "media", "image1.png"), width=Inches(3.0))
P("", after=40)
P("ANÁLISIS MACROECONÓMICO", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
P("UNIVERSIDAD CIENTÍFICA DEL SUR S.A.C.", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
P("RUC 20421239275", align=WD_ALIGN_PARAGRAPH.CENTER, after=60)
P("PRESENTADO POR", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
P("[NOMBRE]", align=WD_ALIGN_PARAGRAPH.CENTER, after=30)
P("PROFESOR", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
P("Sergio Julio Chión Chacón", align=WD_ALIGN_PARAGRAPH.CENTER, after=90)
P("LIMA, NOVIEMBRE DE 2026", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

# ================= RESUMEN =================
H1("Resumen")
T("La economía mundial crecerá 3,1% en 2026 y 3,1% en 2027, frente a 3,4% en 2025, con China en 4,5% y Estados Unidos en 2,2% (BCRP, RI setiembre 2026). El conflicto en Medio Oriente elevó el petróleo WTI de US$64,4 por barril en febrero a US$98,9 en octubre, y la Reserva Federal subió su tasa 25 pb el 17 de setiembre, a 3,75%–4,00%, porque la inflación PCE de 2026 subiría a 3,7%. El cobre promedia US$6,14 por libra en 2026, 36% más que en 2025, y empuja los términos de intercambio peruanos 18,1%. La cuenta corriente registraría un superávit de 4,0% del PBI y el saldo comercial, US$48.865 millones. Para UCSUR el mundo actúa por dos canales: el ingreso nacional que sostiene el empleo de las familias de Lima Sur y el costo en dólares de su equipamiento académico, que ya subió 5,1% en soles " + pg("int") + ".")
T("El PBI peruano crecería 3,2% en 2026 y 3,0% en 2027, tras un recorte de 0,2 pp por un Fenómeno El Niño extraordinario; en agosto creció 3,23% y acumula 3,14% en el año (BCRPData). El consumo privado aportaría 2,36 pp y la inversión privada, 2,87 pp. La inflación de Lima llegó a 5,25% en octubre, por encima del rango meta y de la proyección de 4,2% del RI, mientras la liquidez en soles crece 16,7%. El BCRP mantiene su tasa en 4,25%, lo que deja una tasa real ex ante de 1,20% y ex post de −1,00%. El sol cotiza S/3,412 por dólar, respaldado por reservas de US$96.668 millones. El desempleo de Lima bajó a 4,4%, pero el ingreso promedio real cayó 4,0%, y el crédito de consumo crece 13,2%. Es una economía con empleo, crédito y más inflación, pero con menos poder adquisitivo " + pg("peru") + ".")
T("Universidad Científica del Sur S.A.C. (RUC 20421239275) es una universidad privada societaria cuyo mercado núcleo son estudiantes de clase media de Lima Sur y sus familias, que pagan pensiones en soles con su salario, su crédito o becas. No tiene un cliente grande: su riesgo está repartido entre miles de hogares cuya capacidad de pago depende del empleo, los salarios y el crédito. Sus ingresos por derechos de enseñanza pasaron de S/264,1 millones en 2022 a S/594,8 millones en 2025; la utilidad de operación llegó a S/219,5 millones (margen de 36,9%) y la utilidad neta a S/141,6 millones. Para crecer elevó sus obligaciones financieras a S/172,8 millones e invirtió S/82,5 millones en activos fijos en 2025. Otorga crédito a sus estudiantes vía fraccionamiento de pensiones y recibe crédito de proveedores (S/40,0 millones) y de bancos " + pg("cruces") + ".")
T("Los cruces de tres años muestran que UCSUR crece por encima de la economía. Sus ingresos reales subieron 14,7%, 27,7% y 39,4% en 2023-2025, frente a un PBI de −0,35%, 3,52% y 3,43%; la elasticidad aparente frente al consumo privado fue 9,99 en 2024 y 10,85 en 2025. Con la inflación de 2023 (6,3% promedio) el margen operativo cayó a 15,8%; con inflación de 1,5% en 2025 subió a 36,9%. Las cuentas por cobrar crecieron 139% en 2025, hasta S/48,8 millones, y el plazo de cobro pasó de 18 a 30 días, mientras las cuentas por pagar comerciales subieron 60,4%. Con inflación de 5,25%, el valor real de esas cuentas por cobrar pierde S/2,6 millones al año y las cuentas por pagar alivian S/2,1 millones. Cada 25 pb de alza de tasa cuestan S/0,43 millones en intereses sobre la deuda actual " + pg("cxc") + ".")
T("La conclusión central es que el entorno de 2026-2027 sostiene el volumen de UCSUR por el empleo y el crédito, pero erosiona el poder adquisitivo de sus familias por la inflación de oferta. Se recomienda: (R1) reajustar pensiones con la inflación esperada (3,05%) y no con la observada (5,25%), porque con una elasticidad de 10,4 cada punto de consumo perdido cuesta S/62 millones de ingresos; (R2) fijar a tasa fija la deuda de S/172,8 millones antes de un alza del BCRP, dado que la tasa real ex post es −1,00%; (R3) trasladar el fraccionamiento de pensiones a convenios de crédito educativo con bancos y cajas, aprovechando la liquidez (+16,7%) y el crédito de consumo (+13,2%), para reducir la cobranza a 20 días; y (R4) cubrir con forwards el capex en dólares mientras el diferencial con la Fed sea solo 0,375 pp " + pg2() + ".")

# ================= SECCIÓN 1 (numeración desde 1) =================
new = doc.add_section(WD_SECTION.NEW_PAGE)
new.header.is_linked_to_previous = False
hp = new.header.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = hp.add_run(); r.font.name = FONT; r.font.size = Pt(SZ)
for t_, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    e = OxmlElement("w:fldChar" if t_ else "w:instrText")
    if t_: e.set(qn("w:fldCharType"), t_)
    else: e.set(qn("xml:space"), "preserve"); e.text = txt
    r._r.append(e)
pgn = OxmlElement("w:pgNumType"); pgn.set(qn("w:start"), "1"); new._sectPr.append(pgn)

H1("SECCIÓN 1"); MARK("int_ini")
H2("Análisis de la economía internacional y sus incidencias sobre la economía del país en que la empresa desarrolla sus principales actividades")

SUB("1. Crecimiento mundial (Y*) y PBI peruano (Y): empleo y demanda de educación superior")
T("El BCRP mantuvo en 3,1% el crecimiento mundial para 2026 y 2027, debajo del 3,4% de 2025 (RI setiembre 2026). El conflicto en Medio Oriente resta actividad, pero la inversión en inteligencia artificial y la transición energética la compensan: Estados Unidos crecería 2,2%, China 4,5% y América Latina 2,2%. El Perú (3,2%) crece por encima del promedio porque exporta los metales que esa inversión demanda: el cobre promedió US$6,14 por libra entre enero y octubre de 2026, 36% más que en 2025 (BCRPData). Ese ingreso externo se convierte en empleo: el sector privado formal sumó alrededor de 242 mil puestos en lo que va de 2026 (BCRP, RI setiembre 2026). UCSUR no exporta, pero su demanda depende del empleo de las familias de Lima Sur; por eso Y* le llega a través de Y, del empleo y del consumo, con rezago.")
CAP("Gráfico 1. Crecimiento del PBI por Economía, 2025–2027 (var. % real)")
IMG("g1.png")
SRC("BCRP, Reporte de Inflación setiembre 2026, con base en FMI y Consensus Forecast.")
INT("El gráfico 1 muestra que el Perú crece 0,1 pp por encima del mundo y 1,0 pp por encima de América Latina en 2026. Esa diferencia financia empleo formal y, con una elasticidad aparente de 10,4, cada décima adicional de consumo privado se asocia a cerca de S/6 millones de ingresos para UCSUR.")
CADENA("Cadena 1. Crecimiento Mundial (Y*) → PBI Peruano (Y) → Ingresos de UCSUR",
       [("↑Y*", "Mundo 3,1%; China 4,5%"), ("↑Px", "Cobre +36%"), ("↑TI", "+18,1% (2026)"), ("↑Y", "Perú 3,2%"), ("↑Empleo", "+242 mil formales"), ("↑Ventas UCSUR", "ε = 10,4")],
       "Si crece la economía mundial → suben los precios de los metales y los términos de intercambio → crece el PBI peruano y el empleo formal → las familias de Lima Sur matriculan y pagan pensiones → suben los ingresos de UCSUR (S/594,8 millones en 2025, +41,5%).")
CADENA("Cadena 2. Crecimiento Mundial (Y*) → Inflación (P) y Tasa de Interés (i): Ajuste hasta Y = Yn",
       [("↑Y*", "Aceleración mundial; WTI US$98,9"), ("Y > Yn", "DA +6,2% (2026P)"), ("↑P", "π 5,25% (oct-26)"), ("↓M/P", "Liquidez +16,7% < saldo real"), ("↑i", "Presión sobre 4,25%"), ("↓Y", "3,0% (2027P), hasta Y = Yn")],
       "Si la demanda externa y la inversión empujan la demanda interna (+6,2%) por encima del producto potencial → suben los precios (5,25%) → caen los saldos reales → sube la tasa de interés → se modera el PBI a 3,0% en 2027 hasta que Y = Yn. Para UCSUR, la fase de ajuste significa crédito educativo más caro y matrícula 2027 más lenta.")

SUB("2. Precio del petróleo e inflación (P): costo de la energía y poder adquisitivo de las familias")
T("El petróleo WTI promedió US$98,9 por barril en octubre de 2026, frente a US$64,4 en febrero, antes del conflicto en Medio Oriente, y a US$65,5 de promedio en 2025 (BCRPData). El RI de setiembre supuso US$82 para 2026, de modo que el precio de octubre lo supera en 21%. El alza se trasladó a combustibles, tarifas eléctricas y pasajes, y explica que la inflación de Lima llegue a 5,25% mientras la inflación sin alimentos, energía y transporte es solo 1,8% (BCRP, RI setiembre 2026). Para UCSUR el petróleo pesa por dos lados: encarece la energía de laboratorios, clínicas y campus, dentro de gastos generales de S/128,2 millones en 2025, y reduce el ingreso disponible de un estudiante que gasta más en transporte para llegar a clases.")
CAP("Gráfico 2. Petróleo WTI y Cobre LME, enero 2025 – octubre 2026 (promedio mensual)")
IMG("g2.png")
SRC("BCRPData, series PN01660XM y PN01652XM (consulta del 11 de noviembre de 2026); BCRP, RI setiembre 2026.")
INT("El gráfico 2 muestra dos choques opuestos: el cobre sube de forma sostenida y el petróleo salta en marzo y otra vez desde agosto. Para el Perú el saldo es positivo; para UCSUR es negativo en el corto plazo, porque la energía se traslada en semanas a sus costos, mientras el ingreso minero llega a sus familias con rezago.")
CAP("Modelo 1. Mercado Internacional del Petróleo: Contracción de la Oferta, 2026")
IMG("m1.png", 5.6)
SRC("BCRPData (WTI de febrero y octubre de 2026). Curvas ilustrativas con precios observados; diagrama conceptual.")
INT("El modelo 1 muestra que la oferta se contrajo de S₀ a S₁ por el conflicto y, con una demanda poco sensible al precio, el equilibrio pasó de E₀ (US$64,4) a E₁ (US$98,9), +53,5%. Para UCSUR es un choque de costos, no de demanda: no cambia el número de postulantes, pero sí lo que cuesta operar sus sedes.")
CADENA("Cadena 3. Petróleo → Inflación (P) → Salario Real y Costos de UCSUR",
       [("↑WTI", "US$64,4 → US$98,9"), ("↑P energía", "Tarifas y pasajes"), ("↑π", "5,25% (oct-26)"), ("↓w/P", "Ingreso real −4,0%"), ("↑Costos UCSUR", "Gastos generales S/128,2 MM"), ("↓Margen", "36,9% en riesgo")],
       "Si sube el petróleo → sube la inflación → cae el salario real de las familias y suben los costos operativos de UCSUR → se reduce su margen y la capacidad de pago de sus estudiantes al mismo tiempo.")

SUB("3. Tasa de la Reserva Federal (i*) y tipo de cambio (E): paridad de tasas")
T("La Reserva Federal subió su tasa 25 pb el 17 de setiembre de 2026, a 3,75%–4,00%, después de haberla recortado a 3,50%–3,75% en diciembre de 2025 (Federal Reserve, 2026). Con el BCRP en 4,25%, el diferencial frente al punto medio de la Fed se redujo a 0,375 pp. El sol, sin embargo, se mantiene estable: S/3,442 de promedio en octubre y S/3,412 el 9 de noviembre, frente a S/3,367 en diciembre de 2025 (BCRPData), porque el superávit comercial y las compras del BCRP compensan el menor atractivo de las tasas en soles.")
EQ("Paridad descubierta de tasas: i = i* + Δe esperada + ρ")
EQ("4,25% = 3,875% + (Δe + ρ)   →   Δe + ρ = 0,375 pp")
T("Para el BCRP, ese 0,375 pp es el margen que compensa al inversionista por depreciación esperada y riesgo: si la Fed sube de nuevo y el BCRP no responde, la paridad presiona al sol. Para UCSUR, que cobra en soles, el efecto llega por el costo de lo que importa (equipos, licencias de software) y no por sus ventas.")
CAP("Gráfico 3. Tipo de Cambio Sol/Dólar, enero 2025 – noviembre 2026")
IMG("g3.png")
SRC("BCRPData, series PN01210PM (promedio mensual bancario) y PD04638PD (interbancario venta, 9 de noviembre de 2026).")
INT("El gráfico 3 muestra que el sol se apreció 10,2% en 2025 (de S/3,748 a S/3,367) y que en 2026 oscila entre S/3,36 y S/3,45. Para UCSUR, esa estabilidad permite presupuestar el capex en dólares dentro de un rango estrecho de S/3,40–3,50.")
CAP("Modelo 2. Mercado Cambiario: Oferta y Demanda de Dólares, diciembre 2025 – noviembre 2026")
IMG("m2.png", 5.6)
SRC("BCRPData; BCRP, RI setiembre 2026. Diagrama conceptual con valores observados.")
INT("El modelo 2 muestra que la Fed y el petróleo desplazan la demanda de dólares de D$₀ a D$₁, pero la oferta abundante limita el alza: el equilibrio pasa de E₀ (S/3,367) a E₁ (S/3,412), apenas +1,3%. Mientras se mantenga esa oferta, el traslado cambiario a los costos de UCSUR será acotado.")
CADENA("Cadena 4. Tasa de la Fed (i*) → Tipo de Cambio (E) → Costo Importado de UCSUR",
       [("↑i*", "Fed 3,75%–4,00%"), ("↓(i − i*)", "0,375 pp"), ("↑Salida de capital", "No residentes 45%"), ("↑E", "S/3,367 → S/3,412"), ("↑Costo importado", "Equipos y licencias"), ("↑Capex UCSUR", "S/82,5 MM (2025)")],
       "Si sube la tasa de la Fed → se reduce el diferencial de tasas → salen capitales → sube el tipo de cambio → sube el costo en soles del equipamiento → sube el capex de UCSUR.")

SUB("4. Términos de intercambio (TI) y balanza de pagos (BP): reservas y estabilidad cambiaria")
T("Los términos de intercambio crecerían 18,1% en 2026 y alcanzarían en 2027 su nivel más alto desde que hay registro, por el cobre (615 centavos por libra en 2026) y el oro (BCRP, RI setiembre 2026). Las exportaciones sumarían US$119.876 millones y las importaciones US$71.011 millones, con un saldo comercial de US$48.865 millones (12,1% del PBI). La cuenta corriente tendría un superávit de 4,0% del PBI, su quinto año seguido, y el BCRP compró US$15.715 millones en 2026; las reservas llegaron a US$96.668 millones el 9 de noviembre (BCRPData).")
EQ("Balanza de pagos: BP = CA + KA + ER")
EQ("CA = +4,0% del PBI (superávit)   →   KA + ER = −4,0% del PBI   →   ↑RIN (compras BCRP US$15.715 MM)")
T("Para el BCRP, la ecuación dice que el superávit corriente se compensa con salida de capitales y acumulación de reservas: el banco central compra dólares para que el exceso de oferta no aprecie en exceso al sol. Para UCSUR, esas reservas son un seguro: reducen la probabilidad de un salto cambiario que encarezca su equipamiento o su deuda.")
CAP("Gráfico 4. Balanza Comercial del Perú, 2025–2027 (US$ miles de millones)")
IMG("g4.png")
SRC("BCRP, Reporte de Inflación setiembre 2026, cuadro de balanza comercial.")
INT("El gráfico 4 muestra que el saldo comercial sube de US$35.433 millones en 2025 a US$48.865 millones en 2026, aunque las importaciones crecen más rápido por bienes de capital y de consumo duradero. Para UCSUR, el exceso de dólares es lo que mantiene barato su equipamiento importado.")
CADENA("Cadena 5. Términos de Intercambio (TI) → Balanza de Pagos (BP) → Tipo de Cambio (E) → UCSUR",
       [("↑TI", "+18,1% (2026)"), ("↑CA", "+4,0% del PBI"), ("↑Oferta de US$", "Saldo US$48.865 MM"), ("↑RIN", "US$96.668 MM"), ("E estable", "S/3,40–3,50"), ("↓Riesgo cambiario", "Capex de UCSUR")],
       "Si mejoran los términos de intercambio → sube el superávit en cuenta corriente → entran más dólares y el BCRP acumula reservas → el tipo de cambio se mantiene estable → baja el riesgo cambiario del capex de UCSUR.")

SUB("5. Inflación de Estados Unidos (π*) y tipo de cambio (E): costo del equipamiento académico importado")
T("UCSUR ofrece carreras de ciencias de la salud, ambientales y veterinaria que requieren laboratorios, simuladores clínicos, equipos de diagnóstico y licencias de software facturados en dólares. Su costo en soles depende del precio en origen y del tipo de cambio. La inflación PCE de Estados Unidos proyectada para 2026 es 3,7% (Fed, citada en BCRP, RI setiembre 2026), y el sol pasó de S/3,367 en diciembre de 2025 a S/3,412. Con compras de activos fijos de S/82,5 millones en 2025 (+78,7%), la universidad tiene una exposición relevante a ambas variables.")
EQ("Costo en soles = P* × (1 + π*) × E")
EQ("US$1 MM:  1,00 × 3,367 = S/3,367 MM   →   1,037 × 3,412 = S/3,538 MM   (+5,1%)")
T("Para el BCRP, el cálculo muestra el traslado de precios externos con un sol estable: casi todo el encarecimiento proviene de π*, no de la depreciación. Para UCSUR, si el tipo de cambio sube a S/3,60, el mismo equipo costaría S/3,733 millones, 10,9% más que en diciembre de 2025.")
CAP("Gráfico 5. Costo en Soles de un Equipo Académico de US$1 MM: Efectos de Precio y Tipo de Cambio")
IMG("g5.png")
SRC("Cálculo con tipo de cambio de BCRPData (diciembre de 2025 y 9 de noviembre de 2026) e inflación PCE 2026 de 3,7% (Fed, citada en BCRP, RI setiembre 2026).")
INT("El gráfico 5 muestra que cada 10 céntimos de alza del tipo de cambio añaden cerca de 3 pp al costo del equipamiento. Con un capex del orden de S/80 millones al año, comprar a S/3,60 en lugar de S/3,41 costaría unos S/4,5 millones más.")
CADENA("Cadena 6. Inflación de EE.UU. (π*) → Tipo de Cambio (E) → Capex de UCSUR",
       [("↑π*", "PCE 3,7% (2026P)"), ("↑i*", "Fed 3,75%–4,00%"), ("↑E", "S/3,412 (9-nov)"), ("↑P* × E", "Equipo +5,1% en S/"), ("↑Capex", "S/82,5 MM (2025)"), ("↓Flujo libre UCSUR", "Tras capex y deuda")],
       "Si sube la inflación de EE.UU. → la Fed mantiene tasas altas → sube el tipo de cambio → sube el precio en soles del equipamiento → sube el capex → se reduce el flujo libre de UCSUR.")
T("El diagrama de Ishikawa agrupa los seis factores internacionales. Las espinas verdes (crecimiento mundial y términos de intercambio) empujan el ingreso de las familias; las rojas (petróleo, Fed, inflación de EE.UU.) empujan los costos de UCSUR; la gris resume la estabilidad financiera externa.")
CAP("Diagrama 1. Ishikawa de Factores Internacionales que Afectan a UCSUR, 2026–2027")
IMG("i1.png")
SRC("BCRP, RI setiembre 2026; BCRPData; Federal Reserve (2026). Diagrama conceptual.")
INT("El diagrama 1 muestra que las espinas favorables actúan sobre la demanda con rezago y las desfavorables sobre los costos de inmediato. El riesgo internacional relevante para UCSUR no es una caída de matrícula, sino un costo operativo y de inversión más alto en 2026.")
MARK("razint"); CRIT("el entorno internacional de 2026 favorece a UCSUR por el ingreso nacional y la perjudica por los costos, y ambos efectos llegan a destiempo. Los términos de intercambio crecen 18,1% y el superávit comercial llega a US$48.865 millones, pero esa riqueza se concentra en minería y en el fisco y llega a las familias de Lima Sur con rezago, a través del empleo formal (242 mil puestos). El petróleo, en cambio, pasó de US$64,4 a US$98,9 en ocho meses y se trasladó en semanas a pasajes y tarifas: la inflación de 5,25% de octubre lo confirma, con un ingreso real que cae 4,0%. La Fed agrega una tercera presión: con un diferencial de solo 0,375 pp, el sol depende de las compras del BCRP y no de las tasas. El crecimiento de 41,5% de los ingresos de UCSUR en 2025 no se explica por el entorno externo, que fue similar en 2024 y 2025; por eso la universidad no debe leer el buen momento minero como una garantía de demanda, sino como un viento de cola que puede revertirse si el cobre cae o si la Fed vuelve a subir.")
ESTR("UCSUR debe usar la estabilidad cambiaria que hoy le dan el superávit externo y las reservas de US$96.668 millones para blindar su estructura de costos antes de que el ciclo cambie. Con un capex del orden de S/80 millones al año y un diferencial de tasas de 0,375 pp, conviene comprar forwards para la mitad de sus compras de equipamiento de 2027 mientras el tipo de cambio esté por debajo de S/3,45; si el sol llegara a S/3,60, esa cobertura evitaría hasta S/2,3 millones de sobrecosto. Frente al petróleo a US$98,9, debe negociar contratos de energía con precio fijo o tope por 24 meses, porque la inflación de energía se traslada a sus costos antes que a sus pensiones. Y debe programar las compras de equipos en tramos trimestrales y priorizar proveedores con precios fijados en soles, no en un solo pedido, para promediar el tipo de cambio en un año en que la Fed puede volver a subir. Estas medidas no dependen de la matrícula: protegen el margen de 36,9% justo cuando el entorno internacional deja de ser un viento de cola y pasa a ser una fuente de costos.")
MARK("int_fin")

H2("Situación macroeconómica del Perú y perspectivas 2025–2027: dependencia de Universidad Científica del Sur S.A.C. del entorno nacional"); MARK("peru_ini")

SUB("1. PBI (Y) y consumo privado (C): ventas de UCSUR y elasticidad de la demanda")
T("El PBI peruano creció 3,4% en 2025 y crecería 3,2% en 2026 y 3,0% en 2027 (BCRP, RI setiembre 2026). El dato más reciente es agosto: +3,23% interanual y 3,14% acumulado en el año (INEI, vía BCRPData). La demanda interna crecería 6,2%, impulsada por la inversión privada (+14,0%) y el consumo privado (+3,6%), mientras las exportaciones apenas suben 0,1% por El Niño. Con las ponderaciones reales de 2025, la identidad del gasto cuadra con la proyección oficial:")
EQ("PBI = C + I + G + (X − M)")
EQ("3,20% = 2,36 (C: 65,6% × 3,6%) + 2,87 (Ipriv: 20,5% × 14,0%) + 0,06 (Ipub) + 0,70 (inventarios) + 0,45 (G: 14,2% × 3,2%) + 0,03 (X) − 3,27 (M: 30,3% × 10,8%)")
T("Para el BCRP, el resultado dice que el crecimiento de 2026 es de demanda interna: consumo e inversión aportan 5,23 pp, y las importaciones restan 3,27 pp. Para UCSUR, el consumo privado es su mercado: la pensión universitaria es un gasto de las familias que compite con vivienda, transporte y alimentación, y su desaceleración a 3,0% en 2027 estrechará el espacio para subir precios.")
CAP("Gráfico 6. PBI Mensual del Perú, enero 2025 – agosto 2026 (var. % interanual)")
IMG("g6.png")
SRC("BCRPData, serie PN01728AM, con datos del INEI; BCRP, RI setiembre 2026.")
INT("El gráfico 6 muestra un crecimiento estable alrededor de 3%, con baches en mayo y junio de 2026 por la producción primaria. Es compatible con la proyección de 3,2%, pero no con el crecimiento de dos dígitos de UCSUR: la universidad crece por encima de su mercado."); MARK("cruces_ini")
T("La elasticidad ingreso de la demanda mide cuánto cambian las ventas cuando cambia el ingreso de los consumidores. Para UCSUR se calculó con sus ingresos reales (deflactados por la inflación promedio de Lima) frente al consumo privado real:")
EQ("ε = %Δ Ingresos reales de UCSUR / %Δ Consumo privado real")
EQ("2024: ε = 27,66% / 2,77% = 9,99        2025: ε = 39,39% / 3,63% = 10,85        Promedio = 10,42")
CAP("Tabla 1. Cruces de Tres Años: PBI, Consumo, Inflación y Estados Financieros de UCSUR, 2023–2025")
APA(["Indicador", "2023", "2024", "2025"], [
    ["PBI real (var. %)", "−0,35", "3,52", "3,43"],
    ["Consumo privado real (var. %)", "0,06", "2,77", "3,63"],
    ["Inflación promedio de Lima (%)", "6,26", "2,35", "1,50"],
    ["Ingresos por derechos de enseñanza (S/ MM)", "321,8", "420,4", "594,8"],
    ["Ingresos nominales (var. %)", "21,84", "30,66", "41,48"],
    ["Ingresos reales (var. %)", "14,66", "27,66", "39,39"],
    ["Elasticidad frente al consumo privado", "n. s.", "9,99", "10,85"],
    ["Elasticidad frente al PBI", "n. s.", "7,87", "11,48"],
    ["Margen operativo (%)", "15,8", "28,8", "36,9"],
    ["Derechos de enseñanza por cobrar (S/ MM)", "17,7", "20,4", "48,8"],
    ["Días de cobranza", "20", "18", "30"],
    ["Cuentas por pagar comerciales (S/ MM)", "25,9", "24,9", "40,0"],
    ["Obligaciones financieras (S/ MM)", "113,1", "131,3", "172,8"],
], [3.3, 1.0, 1.0, 1.0])
SRC("UCSUR, Estados financieros auditados 2023, 2024 y 2025 (los dos últimos por Tanaka, Valdivia, Arribas & Asociados); BCRPData, PBI por tipo de gasto trimestral (PN02528AQ, PN02529AQ, PN02536AQ y PN02537AQ) e IPC de Lima (PN38705PM). n. s.: no significativa, porque el PBI y el consumo casi no variaron. Margen operativo de 2024 según el comparativo reexpresado del informe 2025.")
CAP("Gráfico 7. PBI, Consumo Privado e Ingresos Reales de UCSUR, 2023–2025 (var. % real)")
IMG("g7.png")
SRC("UCSUR, EEFF auditados 2023-2025; BCRPData.")
INT("El gráfico 7 muestra que una elasticidad de 10,4 no describe la respuesta de las familias a su ingreso. En 2023 los ingresos reales de UCSUR subieron 14,7% con un PBI que cayó 0,35%: la mayor parte del crecimiento proviene de captar estudiantes y abrir carreras. La sensibilidad sí es útil para planificar: cada punto menos de consumo se asocia a 10,4 puntos menos de crecimiento real, unos S/62 millones sobre la base de 2025.")
CAP("Modelo 3. Oferta Agregada y Demanda Agregada: Perú 2025–2026")
IMG("m3.png", 5.6)
SRC("BCRP, RI setiembre 2026; BCRPData. Diagrama conceptual con cifras observadas y proyectadas.")
INT("El modelo 3 muestra que la demanda agregada se desplazó a la derecha (DA₁) por la inversión privada y el consumo, y la oferta agregada a la izquierda (OA₁) por el petróleo y El Niño. El equilibrio pasa de E₀ (π 1,5%; PBI 3,4%) a E₁ (π 5,25%; PBI 3,2%): más precios con casi el mismo producto. Para UCSUR, OA₁ es la curva que importa, porque sube los precios sin subir el ingreso de sus familias.")
CADENA("Cadena 7. Consumo Privado (C) → PBI (Y) → Ventas de UCSUR",
       [("↑C", "+3,6% (2026P)"), ("↑Y", "+3,2% (2026P)"), ("↑Gasto en educación", "ε = 10,4"), ("↑Ventas UCSUR", "S/594,8 MM (+41,5%)"), ("↓C en 2027", "+3,0%"), ("↓Ventas", "−6 pp de crecimiento real")],
       "Si crece el consumo privado → crece el PBI → sube el gasto de las familias en educación superior → suben los ingresos de UCSUR; si el consumo se desacelera de 3,6% a 3,0% en 2027 → el crecimiento real de los ingresos de UCSUR caería unos 6 pp."); MARK("cruces_fin")

SUB("2. Inflación (P) y costos de UCSUR: salarios, servicios, CxC y CxP")
T("La inflación de Lima llegó a 5,25% en octubre de 2026, con 0,57% mensual y 4,88% acumulado en el año (INEI, vía BCRPData). El RI proyectó 4,2% para diciembre; para cumplirlo, noviembre y diciembre deberían sumar −0,65%, lo que es improbable, de modo que 2026 cerraría por encima de 5%. El RI prevé que la inflación de servicios llegue a 5,3% en 2026 y las expectativas a 12 meses están en 3,05%. Para UCSUR, la inflación entra por los costos: la planilla docente y administrativa (S/214,7 millones, 36,1% de los ingresos) se reajusta con rezago, y los servicios de terceros suben con la energía. Los proveedores trasladan esa inflación: las cuentas por pagar comerciales subieron 60,4% en 2025, a S/40,0 millones. La inflación también cambia el valor real de los saldos: con 5,25%, las cuentas por cobrar de S/48,8 millones pierden S/2,6 millones de poder de compra al año, mientras las cuentas por pagar alivian S/2,1 millones.")
CAP("Gráfico 8. Inflación en Lima Metropolitana y Expectativas, enero 2025 – octubre 2026 (%)")
IMG("g8.png")
SRC("BCRPData, series PN01273PM y PD12912AM; BCRP, RI setiembre 2026.")
INT("El gráfico 8 muestra que la inflación salió del rango meta en marzo de 2026 y no volvió, mientras las expectativas suben de 2,8% a 3,05%. Para UCSUR, la planilla de 2027 se reajustará con esa inflación, y una pensión indexada a 5,25% chocaría con un ingreso real de sus familias que cae.")
CAP("Modelo 4. Isocuanta del Servicio Educativo: Docentes y Capital Académico ante la Inflación")
IMG("m4.png", 5.6)
SRC("UCSUR, EEFF auditados 2025 (gastos de personal y capex); BCRPData. Diagrama conceptual.")
INT("El modelo 4 muestra la isocuanta Q₀ del servicio educativo con dos insumos: horas docentes (L) y capital académico (K). La inflación de 5,25% eleva el costo de L más que el de K (+5,1% por equipo importado), la recta de isocosto se hace más empinada y el punto óptimo pasa de A a B: más laboratorios, simulación y plataformas digitales por alumno, y menos horas docentes por estudiante. Para UCSUR, es la lógica del capex de S/82,5 millones de 2025.")
CADENA("Cadena 8. Inflación (P) → Salarios (w) → Costos y CxC/CxP de UCSUR",
       [("↑P", "π 5,25% (oct-26)"), ("↑w", "Reajustes 2027"), ("↑Costos UCSUR", "Planilla S/214,7 MM"), ("↓Valor real CxC", "−S/2,6 MM/año"), ("↓Valor real CxP", "+S/2,1 MM/año"), ("↓Margen", "36,9% en riesgo")],
       "Si sube la inflación → suben los salarios y los servicios → suben los costos de UCSUR → pierde valor real lo que le deben sus estudiantes y gana algo con lo que debe a proveedores; el efecto neto es negativo porque las cuentas por cobrar superan a las por pagar.")

SUB("3. Dinero (M) e inflación (P): teoría cuantitativa y liquidez del sistema")
T("La liquidez en soles de las sociedades de depósito creció 16,7% interanual en setiembre de 2026 (BCRPData), muy por encima del crecimiento nominal de la economía. La teoría cuantitativa permite leer ese dato:")
EQ("M × V = P × Y   →   %ΔM + %ΔV = %ΔP + %ΔY")
EQ("16,7% + %ΔV = 4,5% + 3,2%   →   %ΔV = −9,0%")
T("Para el BCRP, una caída de 9,0% en la velocidad significa que el público retiene más dinero del que gasta: hay liquidez acumulada que puede convertirse en demanda y en precios si las expectativas suben, lo que justifica vigilar la tasa. Para UCSUR, esa liquidez es hoy una fuente de pago de pensiones y de crédito a sus estudiantes; si el BCRP la retira con alzas de tasa, la cobranza se volverá más difícil.")
CAP("Gráfico 9. Liquidez en Soles e Inflación, enero 2025 – octubre 2026 (var. % 12 meses)")
IMG("g9.png")
SRC("BCRPData, series PN00189MM (liquidez en soles de las sociedades de depósito) y PN01273PM; BCRP, RI setiembre 2026.")
INT("El gráfico 9 muestra que la liquidez pasó de crecer 4,2% a fines de 2025 a 16,7%–17,7% en 2026, mientras la inflación subió de 1,5% a 5,25%. Para UCSUR, el exceso de liquidez es un colchón de demanda en 2026 y un riesgo de ajuste monetario en 2027.")
CADENA("Cadena 9. Dinero (M) → Inflación (P) → Tasa de Interés (i) → UCSUR",
       [("↑M", "Liquidez +16,7%"), ("↓V", "−9,0%"), ("↑P", "π 5,25%"), ("↑Eπ", "3,05% > 3%"), ("↑i", "Presión sobre 4,25%"), ("↑Costo del crédito", "↑CxC UCSUR")],
       "Si la liquidez crece más que la economía → se acumulan saldos que presionan precios → suben las expectativas → el BCRP enfrenta presión para subir la tasa → se encarece el crédito con que las familias pagan pensiones.")

SUB("4. Tasa de interés (i) y política monetaria: CxC, CxP y gastos financieros de UCSUR")
T("El BCRP mantiene su tasa de referencia en 4,25% desde setiembre de 2025 (BCRPData). Con expectativas de inflación de 3,05% (octubre) y una inflación observada de 5,25%:")
EQ("Fisher: i = r + πᵉ   →   r = i − πᵉ")
EQ("r ex ante = 4,25% − 3,05% = 1,20%        r ex post = 4,25% − 5,25% = −1,00%")
T("Para el BCRP, una tasa real ex ante de 1,20%, debajo del nivel neutral, y una ex post negativa indican una política expansiva justo cuando la inflación supera el rango meta; un alza de 25 pb sería coherente con anclar las expectativas. Para UCSUR, la tasa afecta tres partidas. Sus obligaciones financieras (S/172,8 millones) generaron gastos financieros de S/27,5 millones en 2025, de los cuales S/12,0 millones son intereses de arrendamientos; cada 25 pb sobre toda la deuda cuestan S/0,43 millones al año. Sus cuentas por cobrar (S/48,8 millones) se financian con caja propia: con tasas más altas, el costo de oportunidad de prestar a los estudiantes sube. Y sus cuentas por pagar comerciales (S/40,0 millones) se vuelven más valiosas como financiamiento sin costo.")
CAP("Gráfico 10. Gastos Financieros, Diferencia de Cambio y Deuda Financiera de UCSUR, 2022–2025 (S/ millones)")
IMG("g10.png")
SRC("UCSUR, Estados financieros auditados 2023, 2024 y 2025.")
INT("El gráfico 10 muestra que la deuda casi se duplicó entre 2022 y 2025 (de S/89,0 a S/172,8 millones), mientras los gastos financieros se estabilizaron en S/27,5 millones. La sensibilidad de UCSUR a la tasa es moderada en intereses, pero alta en la cobranza, porque sus estudiantes pagan con crédito de consumo.")
CAP("Modelo 5. IS-MP: Crédito, Tasa Real y Producto, 2026")
IMG("m5.png", 5.6)
SRC("BCRPData (tasa de referencia y expectativas, octubre de 2026); BCRP, RI setiembre 2026. Diagrama conceptual.")
INT("El modelo 5 muestra la curva IS desplazada a la derecha (IS₁) por el crédito de consumo (+13,2%) y la inversión privada (+14,0%), con la regla monetaria MP₀ en r = 1,20% (E₁). Si el BCRP sube 25 pb, la MP pasa a MP₁ y el producto se modera en E₂. Para UCSUR, E₂ significa menos crédito para pensiones y más morosidad.")
CADENA("Cadena 10. Inflación (P) → Tasa de Interés (i) → CxC, CxP y Gastos Financieros de UCSUR",
       [("↑P", "π 5,25%"), ("↓r", "Ex post −1,00%"), ("↑i BCRP", "4,25% → 4,50% (escenario)"), ("↑Tasas de crédito", "Consumo y empresas"), ("↑Gastos financieros", "+S/0,43 MM por 25 pb"), ("↑CxC y morosidad", "S/48,8 MM; 30 días")],
       "Si la inflación supera el rango meta → la tasa real cae → el BCRP sube la tasa → suben las tasas de crédito → suben los gastos financieros de UCSUR y se encarece el crédito de sus estudiantes → aumentan las cuentas por cobrar y la morosidad.")

SUB("5. Tipo de cambio (E): operaciones y balance de UCSUR")
T("UCSUR factura en soles y su exposición cambiaria en resultados es pequeña, pero creciente: la pérdida por diferencia de cambio pasó de S/0,1 millones en 2023 a S/0,4 millones en 2024 y S/1,7 millones en 2025 (EEFF auditados), en un año en que el sol se apreció 10,2%, lo que indica pasivos o compromisos en dólares. El riesgo mayor está en el balance futuro, porque el capex y algunos arrendamientos se pagan en dólares. Con el sol en S/3,412 y un rango esperado de S/3,40–3,50, el riesgo es moderado mientras se mantengan el superávit comercial y las reservas.")
CADENA("Cadena 11. Tipo de Cambio (E) → Costo Importado (P*×E) → Resultado de UCSUR",
       [("↑i*", "Fed 3,75%–4,00%"), ("↑E", "S/3,412 → S/3,50"), ("↑P* × E", "Equipos +7,8%"), ("↑Capex en US$", "S/82,5 MM"), ("↑Pérdida cambiaria", "−S/1,7 MM (2025)"), ("↓Utilidad UCSUR", "S/141,6 MM (2025)")],
       "Si sube el tipo de cambio → sube el costo en soles del equipamiento y de los pasivos en dólares → aumenta la pérdida cambiaria → se reduce la utilidad de UCSUR.")

SUB("6. Empleo, remuneraciones (w) y poder adquisitivo: efecto indirecto sobre la matrícula")
T("La tasa de desempleo de Lima Metropolitana bajó de 5,7% a 4,4% entre los trimestres móviles terminados en setiembre de 2025 y 2026, y la de los jóvenes de 14 a 24 años, de 13,9% a 11,3% (INEI, vía BCRPData). El empleo mejora, pero el ingreso no: el ingreso promedio mensual en Lima fue S/2.302, apenas 0,35% más que un año antes, lo que equivale a una caída real de 4,0% con la inflación de setiembre (4,5%). Para UCSUR, el desempleo juvenil importa dos veces: muchos de sus estudiantes trabajan para pagar sus estudios, y la empleabilidad de sus egresados es su principal argumento de venta. La caída del ingreso real ya se refleja en su balance: los castigos de pensiones incobrables subieron 84%, de S/2,0 a S/3,7 millones.")
CAP("Gráfico 11. Desempleo e Ingreso Promedio en Lima Metropolitana, enero 2025 – setiembre 2026")
IMG("g11.png")
SRC("BCRPData, series PN38063GM, PN38066GM y PN38070GM (promedio móvil de tres meses), con datos del INEI.")
INT("El gráfico 11 muestra la divergencia de 2026: más empleo y menos poder de compra. Para la familia de clase media de Lima Sur, una pensión que sube 5% pesa más que el año anterior, aunque haya más miembros trabajando.")
CADENA("Cadena 12. Empleo (N) y Remuneraciones (w) → Poder Adquisitivo (w/P) → Ventas y Cobranza de UCSUR",
       [("↓u", "Lima 4,4%; jóvenes 11,3%"), ("↑N", "+242 mil formales"), ("w nominal", "S/2.302 (+0,35%)"), ("↓w/P", "−4,0% real"), ("↓Capacidad de pago", "Castigos +84%"), ("↑Riesgo de deserción", "CxC S/48,8 MM")],
       "Si baja el desempleo → sube el número de familias con ingreso; pero si la inflación supera al salario → cae el poder adquisitivo → se reduce la capacidad de pago de pensiones → aumentan castigos, cuentas por cobrar y riesgo de deserción en UCSUR.")

SUB("7. Liquidez del sistema financiero, crédito educativo y morosidad")
T("El crédito de consumo de las sociedades de depósito creció 13,2% en setiembre de 2026, frente a 7,3% un año antes, y el crédito total al sector privado 10,3% (BCRPData), sostenidos por la liquidez en soles (+16,7%). El crédito barato permite a las familias financiar estudios, pero UCSUR no lo está aprovechando: sus derechos de enseñanza por cobrar crecieron 139% en 2025, hasta S/48,8 millones, y el plazo de cobro subió de 18 a 30 días. La universidad financia a sus estudiantes con su propio capital de trabajo, y ese crédito ya tiene un costo: la estimación para pérdidas crediticias subió 23,3%, de S/5,3 a S/6,5 millones, y las provisiones totales llegaron a S/7,3 millones.")
CAP("Gráfico 12. Crédito de Consumo y Cobranza de UCSUR")
IMG("g12.png")
SRC("BCRPData, serie PN00537MM; UCSUR, EEFF auditados 2023-2025.")
INT("El gráfico 12 muestra dos ciclos paralelos: el crédito de consumo se acelera desde mediados de 2025 y las cuentas por cobrar de UCSUR saltan en 2025. Si el BCRP sube la tasa, ambos ciclos se revierten a la vez: menos crédito bancario para las familias y más morosidad en las pensiones.")
CADENA("Cadena 13. Liquidez (M) → Crédito → Morosidad → CxC de UCSUR",
       [("↑M", "Liquidez +16,7%"), ("↑Crédito de consumo", "+13,2% (set-26)"), ("↑Matrícula", "Ingresos +41,5%"), ("↑i (escenario)", "Alza de 25 pb"), ("↑Morosidad", "Provisiones S/7,3 MM"), ("↑CxC UCSUR", "S/48,8 MM; 30 días")],
       "Si sube la liquidez → crece el crédito de consumo → más familias financian la matrícula; pero si sube la tasa → se encarece ese crédito → sube la morosidad → crecen las cuentas por cobrar y las provisiones de UCSUR.")
MARK("cxc_fin")

SUB("8. Política fiscal (G): consumo público, déficit y becas")
T("El RI de setiembre proyecta un consumo público de 3,2% en 2026 y 2,3% en 2027, un déficit fiscal de 1,5% del PBI en ambos años y una deuda pública que bajaría de 30,1% a 28,2% del PBI entre 2025 y 2027 (BCRP, RI setiembre 2026). La política fiscal es prudente: aporta 0,45 pp al crecimiento de 2026 y no presiona la inflación. Para UCSUR, el canal fiscal es indirecto pero relevante: parte de sus estudiantes accede a becas y créditos públicos (Pronabec), cuyo presupuesto depende del gasto corriente. Un consumo público que se desacelera de 3,2% a 2,3% limita la expansión de esos programas justo cuando el ingreso real de las familias cae.")
CADENA("Cadena 14. Política Fiscal (G) → Consumo Público → Demanda Financiada de UCSUR",
       [("↓Déficit", "1,5% del PBI"), ("↓G", "3,2% → 2,3%"), ("↓Becas", "Pronabec"), ("↓Demanda becada", "Familias de Lima Sur"), ("↑Uso de crédito", "Consumo +13,2%"), ("↑CxC UCSUR", "S/48,8 MM")],
       "Si el fisco consolida y el consumo público se desacelera → crecen menos los programas de becas → más estudiantes dependen de crédito o fraccionamiento → aumentan las cuentas por cobrar de UCSUR.")
T("El diagrama de Ishikawa doméstico reúne los seis factores de la economía peruana. Las espinas verdes (PBI y consumo, empleo) sostienen la demanda; las rojas (inflación y dinero, crédito y morosidad) presionan la capacidad de pago; las grises (tasa y política fiscal) definen el costo del financiamiento.")
CAP("Diagrama 2. Ishikawa de Factores Domésticos que Afectan a UCSUR, 2026–2027")
IMG("i2.png")
SRC("BCRP, RI setiembre 2026; BCRPData; UCSUR, EEFF auditados 2025. Diagrama conceptual.")
INT("El diagrama 2 muestra que la espina decisiva para 2026-2027 es la inflación: actúa sobre los ingresos (menor capacidad de pago), los costos (salarios y servicios) y la política monetaria (posible alza que encarece el crédito educativo).")
MARK("razperu"); CRIT("la economía peruana de 2026 le ofrece a UCSUR más empleo, más liquidez y más crédito, pero menos ingreso real. El desempleo de Lima bajó a 4,4%, la liquidez en soles crece 16,7% y el crédito de consumo 13,2%, mientras el ingreso promedio real cae 4,0% y la inflación llega a 5,25%. La teoría cuantitativa lo explica: con una velocidad que cae 9,0%, hay saldos acumulados que hoy pagan pensiones pero que mañana pueden traducirse en inflación y en un alza de tasas, porque la tasa real ex post ya es −1,00%. La elasticidad aparente de 10,4 no debe leerse como garantía: refleja la ganancia de participación de 2023-2025 y, aplicada al revés, significa que una desaceleración del consumo de 3,6% a 3,0% restaría unos 6 pp de crecimiento real. La señal de alerta ya está en el balance: las cuentas por cobrar crecieron 139% frente a ingresos que crecieron 41,5%, y los castigos subieron 84%. Parte del crecimiento de 2025 se financió con plazo a las familias, y un alza de tasas convertiría ese plazo en morosidad, justo cuando el consumo público, que financia becas, se desacelera de 3,2% a 2,3%.")
ESTR("UCSUR debe pasar de financiar a sus estudiantes a facilitarles financiamiento, y hacerlo antes de que el ciclo monetario se endurezca. Con la liquidez creciendo 16,7% y el crédito de consumo 13,2%, los bancos y cajas tienen fondos para convenios de crédito educativo a tasa fija; trasladar a ellos el fraccionamiento permitiría bajar la cobranza de 30 a 20 días y liberar unos S/16 millones de capital de trabajo. Al mismo tiempo, conviene fijar la tasa de su deuda de S/172,8 millones mientras la tasa real ex post sea negativa: cada 25 pb de alza cuestan S/0,43 millones al año. En precios, el reajuste de pensiones de 2027 debería atarse a la inflación esperada (3,05%) y aplicarse sobre todo a ingresantes, porque con una elasticidad de 10,4 y un ingreso real que cae 4,0%, un alza de 5,25% arriesgaría más matrícula de la que gana en precio. Por último, debe planificar 2027 con un PBI de 3,0% y un consumo de 3,0%, no con el ritmo de 2025, y reservar parte de la caja operativa de S/230,6 millones como colchón frente a un alza de la morosidad.")
MARK("peru_fin")

doc.save(OUT)
print("saved", OUT)

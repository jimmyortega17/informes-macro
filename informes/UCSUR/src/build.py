import os, sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

S = os.path.dirname(os.path.abspath(__file__)); FIG = os.path.join(S, "fig")
OUT = sys.argv[1]
ROJO = RGBColor(0xC0, 0x00, 0x00); NEGRO = RGBColor(0, 0, 0)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"): setattr(sec, m, Cm(2.54))
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12); st.font.color.rgb = NEGRO
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 1.15
for h, sz in (("Heading 1", 14), ("Heading 2", 12)):
    s = doc.styles[h]; s.font.name = "Times New Roman"; s.font.size = Pt(sz); s.font.bold = True; s.font.color.rgb = NEGRO
    s.element.rPr.rFonts.set(qn("w:asciiTheme"), "") if False else None
    rf = s.element.rPr.find(qn("w:rFonts"))
    if rf is None: rf = OxmlElement("w:rFonts"); s.element.rPr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"): rf.set(qn(a), "Times New Roman")
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]
    s.paragraph_format.space_before = Pt(12); s.paragraph_format.space_after = Pt(6); s.paragraph_format.keep_with_next = True

# número de página arriba a la derecha
hp = sec.header.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = hp.add_run()
for t, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    if t: e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), t)
    else: e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt
    r._r.append(e)
sec.different_first_page_header_footer = True

def P(text="", bold=False, color=None, size=None, align=None, italic=False, after=None, keep=False):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text); r.bold = bold; r.italic = italic
        if color: r.font.color.rgb = color
        if size: r.font.size = Pt(size)
    if align is not None: p.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    if keep: p.paragraph_format.keep_with_next = True
    return p

def T(text): return P(text)
def EQ(text): return P(text, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)
def CAP(text): return P(text, bold=True, keep=True, after=3)
def SRC(text): return P("Fuente: " + text, size=9, after=8)
def INT(text): return P(text, bold=True)
def CADENA_LINEA(text): return P(text, bold=True, size=16)
def CRIT(text):
    p = doc.add_paragraph(); r = p.add_run("RAZONAMIENTO CRÍTICO: "); r.bold = True; r2 = p.add_run(text); r2.bold = True
def ESTR(text):
    p = doc.add_paragraph(); r = p.add_run("RAZONAMIENTO ESTRATÉGICO: "); r.bold = True; r.font.color.rgb = ROJO
    r2 = p.add_run(text); r2.bold = True; r2.font.color.rgb = ROJO
def SUB(text): return P(text, bold=True, keep=True)

def IMG(name, w=6.3):
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

def cell_text(cell, txt, size=9, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""; p = cell.paragraphs[0]; p.alignment = align; p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.0
    r = p.add_run(txt); r.font.size = Pt(size); r.bold = bold

def fix_widths(t, widths):
    tblPr = t._tbl.tblPr
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    grid = t._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths): gc.set(qn("w:w"), str(int(int(w) / 635)))
    for row in t.rows:
        for c, w in zip(row.cells, widths): c.width = Emu(int(w))

def CHAIN(boxes):
    n = len(boxes) * 2 - 1
    t = doc.add_table(rows=1, cols=n); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    wbox = Emu(int(Inches(6.5 - 0.25 * (len(boxes) - 1)) / len(boxes)))
    for i in range(n):
        c = t.rows[0].cells[i]
        if i % 2 == 0:
            c.width = wbox; cell_text(c, boxes[i // 2], 9, align=WD_ALIGN_PARAGRAPH.CENTER); borders(c, top=6, left=6, bottom=6, right=6)
        else:
            c.width = Inches(0.25); cell_text(c, "→", 11, True, WD_ALIGN_PARAGRAPH.CENTER); borders(c)
    fix_widths(t, [wbox if i % 2 == 0 else Inches(0.25) for i in range(n)])
    return t

def APA(header, rows, widths):
    t = doc.add_table(rows=len(rows) + 1, cols=len(header)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for j, h in enumerate(header):
        c = t.rows[0].cells[j]; c.width = Inches(widths[j]); cell_text(c, h, 9, align=WD_ALIGN_PARAGRAPH.CENTER if j else WD_ALIGN_PARAGRAPH.LEFT)
        borders(c, top=12, bottom=6)
    for i, row in enumerate(rows, 1):
        for j, v in enumerate(row):
            c = t.rows[i].cells[j]; c.width = Inches(widths[j]); cell_text(c, v, 9, align=WD_ALIGN_PARAGRAPH.CENTER if j else WD_ALIGN_PARAGRAPH.LEFT)
            borders(c, bottom=12 if i == len(rows) else None)
    fix_widths(t, [Inches(w) for w in widths])
    return t

# ---------------- CARÁTULA ----------------
for txt in ("PONTIFICIA UNIVERSIDAD CATÓLICA DEL PERÚ", "ESCUELA DE POSGRADO"):
    P(txt, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = Pt(18)
p.add_run().add_picture(os.path.join(S, "logo", "word", "media", "image1.png"), width=Inches(3.0))
P("", after=30)
P("ANÁLISIS MACROECONÓMICO", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16)
P("UNIVERSIDAD CIENTÍFICA DEL SUR S.A.C.", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
P("RUC 20421239275", align=WD_ALIGN_PARAGRAPH.CENTER)
P("Curso: Macroeconomía", align=WD_ALIGN_PARAGRAPH.CENTER, after=40)
P("PRESENTADO POR", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
P("[NOMBRE]", align=WD_ALIGN_PARAGRAPH.CENTER, after=24)
P("PROFESOR", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
P("Sergio Julio Chión Chacón", align=WD_ALIGN_PARAGRAPH.CENTER, after=60)
P("LIMA, NOVIEMBRE DE 2026", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

# ---------------- RESUMEN ----------------
doc.add_heading("Resumen", level=1)
T("La economía mundial crecerá 3,1% en 2026 y 3,1% en 2027, frente a 3,4% en 2025, según el Reporte de Inflación (RI) de setiembre de 2026 del BCRP, que recoge proyecciones del FMI y de Consensus Forecast. El conflicto en Medio Oriente llevó el petróleo WTI de US$64,4 por barril en febrero a US$98,9 en octubre de 2026 (BCRPData), 21% por encima del promedio de US$82 que el RI asume para el año. La Reserva Federal subió su tasa 25 pb el 17 de setiembre de 2026, a un rango de 3,75%–4,00% (Federal Reserve, 2026), y el cobre promedió US$6,59 por libra en octubre. Para Universidad Científica del Sur S.A.C. (UCSUR) el canal externo es indirecto: los términos de intercambio (+18,1% en 2026) sostienen el empleo y el ingreso de las familias que pagan pensiones, mientras la energía y el dólar encarecen la operación de sus campus y el equipamiento académico importado.")
T("El Perú crecerá 3,2% en 2026 y 3,0% en 2027, tras un recorte de 0,2 pp en cada año por un Fenómeno El Niño de magnitud extraordinaria (BCRP, RI setiembre 2026). El PBI de agosto creció 3,23% interanual y 3,14% entre enero y agosto (INEI, vía BCRPData). La inflación de Lima subió de 1,5% en diciembre de 2025 a 5,25% en octubre de 2026, por encima de la proyección de 4,2% del RI para diciembre, mientras las expectativas a 12 meses se ubican en 3,05%. El BCRP mantiene su tasa de referencia en 4,25% desde setiembre de 2025, lo que deja una tasa real ex ante de 1,20% y ex post de −1,00%. El sol cotizó S/3,412 por dólar el 9 de noviembre, apenas 1,3% por encima del promedio de diciembre de 2025, respaldado por reservas internacionales de US$96.668 millones (BCRPData).")
T("UCSUR es una universidad privada societaria cuyo mercado núcleo son estudiantes de clase media de Lima Sur y sus familias. Sus ingresos por derechos de enseñanza pasaron de S/264,1 millones en 2022 a S/594,8 millones en 2025, con alzas de 21,8%, 30,7% y 41,5% en los últimos tres años. La utilidad de operación llegó a S/219,5 millones en 2025 (margen de 36,9%) y la utilidad neta a S/141,6 millones, frente a S/76,5 millones en 2024. La expansión se financió con deuda: las obligaciones financieras subieron a S/172,8 millones y los derechos de enseñanza por cobrar se multiplicaron por 2,4 hasta S/48,8 millones, con un plazo de cobranza que pasó de 18 a 30 días (UCSUR, EEFF auditados 2023-2025).")
T("La elasticidad ingreso aparente de la demanda de UCSUR, medida como la variación real de sus ingresos frente a la del consumo privado, fue 10,0 en 2024 y 10,9 en 2025 (promedio 10,4); frente al PBI fue 7,9 y 11,5. Una cifra tan alta no describe la respuesta de las familias a su ingreso: revela que UCSUR ganó participación de mercado, como lo confirma 2023, cuando sus ingresos reales crecieron 14,7% con un PBI que cayó 0,35%. La sensibilidad sí es útil para planificar: cada punto porcentual menos de consumo privado se asocia a unos 10 puntos menos de crecimiento real de ingresos, cerca de S/62 millones sobre la base de 2025. El riesgo de 2026 está en el bolsillo de las familias: el ingreso promedio en Lima Metropolitana cayó 4,0% en términos reales a setiembre y el desempleo juvenil (14-24 años) es 11,3%, aunque el crédito de consumo crece 13,2%.")
T("Se recomienda: (R1) congelar en soles las pensiones de los estudiantes vigentes y aplicar reajustes solo a ingresantes, para proteger la retención mientras la inflación supere 3%; (R2) ampliar el fraccionamiento de pensiones con convenios de crédito educativo con bancos y cajas, aprovechando que el crédito de consumo crece 13,2%, en lugar de financiar a las familias con cuentas por cobrar propias; (R3) contratar energía y servicios con tarifas fijas o indexadas a un tope, dado el WTI cercano a US$99; y (R4) programar en tramos y con cobertura cambiaria las compras de equipamiento importado de laboratorios y simulación clínica, cuyo costo en soles ya subió 5,1% desde diciembre de 2025. El entorno 2026-2027 sigue siendo favorable en volumen, pero exige cuidar la cobranza y el poder adquisitivo de la familia de Lima Sur.")
doc.add_page_break()

# ---------------- SECCIÓN 1 ----------------
doc.add_heading("SECCIÓN 1", level=1)
doc.add_heading("Análisis de la economía internacional y sus incidencias sobre la economía del país en que la empresa desarrolla sus principales actividades", level=2)

SUB("1. Crecimiento económico mundial, empleo en el Perú y demanda de educación superior")
T("El BCRP mantuvo en 3,1% su proyección de crecimiento mundial para 2026 y 2027, por debajo del 3,4% de 2025 (RI setiembre 2026). El conflicto en Medio Oriente resta actividad, pero el dinamismo de las industrias de inteligencia artificial y de la transición energética lo compensa: Estados Unidos crecería 2,2%, China 4,5% y América Latina 2,2%. Para el Perú el vínculo pasa por los metales: si China y la inversión en centros de datos sostienen la demanda de cobre → suben los precios de exportación → mejoran los términos de intercambio, que crecerían 18,1% en 2026 → sube el ingreso nacional y el empleo formal. UCSUR no exporta ni importa a gran escala; su exposición al mundo llega por el empleo y el ingreso de las familias de Lima Sur, que financian 100% de sus ingresos por derechos de enseñanza.")
CAP("Gráfico 1. Crecimiento del PBI por Economía, 2025–2027 (var. % real)")
IMG("g1.png")
SRC("BCRP, Reporte de Inflación setiembre 2026, con base en FMI y Consensus Forecast.")
INT("El gráfico 1 muestra que el Perú (3,2%) crece por encima del promedio mundial (3,1%) y de América Latina (2,2%) en 2026, gracias a China (4,5%) y a los precios de los metales. Para UCSUR esa diferencia importa porque el empleo formal privado sumó alrededor de 242 mil puestos en lo que va de 2026 (BCRP, RI setiembre 2026), y cada nuevo empleo formal en una familia de clase media eleva la probabilidad de que un hijo curse una carrera universitaria privada.")
CAP("Cadena 1. Crecimiento Mundial → Precios de Metales → Empleo en el Perú → Matrícula en UCSUR")
CHAIN(["↑ PBI China 4,5% y mundial 3,1% (2026P)", "↑ Demanda de cobre e IA; TI +18,1%", "↑ Ingreso nacional y 242 mil empleos formales", "↑ Capacidad de pago de familias de Lima Sur", "▲ Riesgo: guerra en Medio Oriente resta actividad"])
SRC("BCRP, RI setiembre 2026; UCSUR, EEFF auditados 2025.")
CADENA_LINEA("↑ PBI China → ↑ precio del cobre → ↑ términos de intercambio (+18,1%) → ↑ empleo formal → ↑ matrícula UCSUR (ε aparente = 10,4)")

SUB("2. Precios internacionales de commodities: energía y equipamiento importado")
T("El petróleo WTI promedió US$98,9 por barril en octubre de 2026, frente a US$64,4 en febrero, antes del conflicto en Medio Oriente, y a US$65,5 de promedio en 2025 (BCRPData). El RI de setiembre supuso US$82 para todo 2026, de modo que el precio de octubre lo supera en 21%. El cobre, en cambio, promedió US$6,59 por libra en octubre y US$6,14 entre enero y octubre, 36% más que en 2025, en línea con los 615 centavos que el RI proyecta para el año. Para la economía peruana el saldo es positivo, porque los metales pesan mucho más en las exportaciones que el petróleo en las importaciones → Para UCSUR el saldo es mixto: el cobre sostiene el ingreso de las familias, pero la energía encarece la operación de sus campus y el transporte de sus estudiantes.")
CAP("Gráfico 2. Petróleo WTI y Cobre LME, enero 2025 – octubre 2026 (promedio mensual)")
IMG("g2.png")
SRC("BCRPData, series PN01660XM y PN01652XM (consultadas el 11 de noviembre de 2026); BCRP, RI setiembre 2026.")
INT("El gráfico 2 muestra dos choques de signo opuesto. El cobre sube de forma sostenida y explica el superávit externo; el petróleo salta en marzo de 2026 y vuelve a subir desde agosto. Para una universidad, la energía es un costo directo (electricidad de laboratorios, aulas y servidores) e indirecto, porque el alza de pasajes reduce el ingreso disponible del estudiante que viaja diariamente a Villa El Salvador.")
CAP("Cadena 2. Petróleo → Tarifas Eléctricas y Pasajes → Costos de Campus y Gasto de las Familias")
CHAIN(["↑ WTI US$98,9 (oct-26), +53,5% desde feb-26", "↑ Tarifas eléctricas y combustibles", "↑ Gastos generales de UCSUR (S/128,2 MM en 2025)", "↑ Costo de transporte del estudiante", "▲ Riesgo: menor margen y más deserción"])
SRC("BCRPData; BCRP, RI setiembre 2026; UCSUR, EEFF auditados 2025, estado de resultados integrales.")
CADENA_LINEA("↑ Petróleo (+53,5%) → ↑ energía y pasajes → ↑ gastos de operación → ↓ ingreso disponible de las familias → ↓ margen UCSUR")
CAP("Modelo 1. Mercado Internacional del Petróleo: Contracción de la Oferta, 2026")
IMG("m1.png", 5.2)
SRC("BCRPData (WTI febrero y octubre de 2026). Curvas ilustrativas con precios observados; diagrama conceptual.")
INT("El modelo 1 explica el salto del WTI como un desplazamiento de la oferta de S₀ a S₁: con una demanda de corto plazo poco sensible al precio, la menor oferta por el conflicto eleva el precio de US$64 a US$99. Para UCSUR, el choque es de costos y no de demanda: no cambia el número de postulantes, pero sí el costo de mantener operativos laboratorios, clínicas veterinarias y campus.")

SUB("3. Desempeño financiero de Universidad Científica del Sur S.A.C., 2022–2025")
T("Los ingresos por derechos de enseñanza de UCSUR crecieron 41,5% en 2025, hasta S/594,8 millones, después de subir 30,7% en 2024 y 21,8% en 2023 (EEFF auditados). El costo de personal docente y administrativo, su principal gasto, creció 26,7% en 2025, por debajo de los ingresos, y bajó de 40,3% a 36,1% de las ventas; ese apalancamiento operativo elevó el margen operativo de 28,8% a 36,9%. La utilidad neta casi se duplicó, de S/76,5 a S/141,6 millones. El crecimiento exigió inversión: la compra de activos fijos sumó S/82,5 millones en 2025 (+78,7%), se pagaron por adelantado S/77,3 millones de arrendamientos y las obligaciones financieras subieron 31,6%, hasta S/172,8 millones → El negocio genera caja (S/230,6 millones de flujo operativo), pero su balance depende de que la matrícula siga creciendo.")
CAP("Tabla 1. Indicadores Financieros de UCSUR, 2022–2025 (S/ millones)")
APA(["Indicador", "2022", "2023", "2024", "2025"], [
    ["Ingresos por derechos de enseñanza", "264,1", "321,8", "420,4", "594,8"],
    ["Variación anual (%)", "—", "21,8", "30,7", "41,5"],
    ["Gastos de personal docente y administrativo", "116,8", "152,5", "169,5", "214,7"],
    ["Utilidad de operación", "55,0", "50,8", "121,1", "219,5"],
    ["Margen operativo (%)", "20,8", "15,8", "28,8", "36,9"],
    ["Utilidad neta", "25,0", "22,0", "76,5", "141,6"],
    ["Obligaciones financieras (corriente + no corriente)", "89,0", "113,1", "131,3", "172,8"],
    ["Derechos de enseñanza por cobrar, neto", "13,4", "17,7", "20,4", "48,8"],
    ["Días de cobranza (por cobrar / ingresos × 365)", "19", "20", "18", "30"],
], [2.9, 0.85, 0.85, 0.85, 0.85])
SRC("UCSUR, Estados financieros auditados 2023, 2024 y 2025 (los dos últimos por Tanaka, Valdivia, Arribas & Asociados). Las cifras de 2024 de utilidad de operación corresponden al comparativo reexpresado del informe 2025.")
CAP("Gráfico 3. Resultados de UCSUR, 2022–2025 (S/ millones y margen operativo)")
IMG("g3.png")
SRC("UCSUR, Estados financieros auditados 2023, 2024 y 2025, estados de resultados integrales.")
INT("El gráfico 3 muestra que el margen operativo cayó en 2023 (15,8%), cuando el PBI se contrajo y la inflación promedio fue 6,3%, y luego se disparó hasta 36,9%. La lección macroeconómica es directa: los costos de UCSUR son en gran parte fijos (planilla docente, depreciación de campus y arrendamientos), por lo que una caída de matrícula reduciría la utilidad mucho más que los ingresos.")
CAP("Cadena 3. Matrícula → Ingresos → Apalancamiento Operativo → Utilidad")
CHAIN(["↑ Ingresos +41,5% (2025)", "Personal +26,7%; gastos generales +17,8%", "↑ Margen operativo 28,8% → 36,9%", "↑ Utilidad neta +85,1% (S/141,6 MM)", "▲ Riesgo: costos fijos amplifican una caída de matrícula"])
SRC("UCSUR, EEFF auditados 2025.")
CADENA_LINEA("↑ Matrícula → ↑ ingresos (+41,5%) → costos fijos → ↑↑ utilidad (+85,1%); si ↓ matrícula → ↓↓ utilidad")

SUB("4. Política monetaria de la Reserva Federal y tipo de cambio")
T("La Reserva Federal subió su tasa 25 pb el 17 de setiembre de 2026, a un rango de 3,75%–4,00%, después de haberla bajado a 3,50%–3,75% en diciembre de 2025 (Federal Reserve, 2026). La razón es la inflación: las proyecciones de la Fed recogidas en el RI elevan la inflación PCE de 2026 a 3,7%. El BCRP mantiene 4,25%, de modo que el diferencial frente al punto medio de la Fed se redujo a 0,375 pp. Con un diferencial tan estrecho, el sol depende más del superávit comercial y de las compras del BCRP (US$15.715 millones en 2026, según el RI) que del atractivo de las tasas en soles.")
EQ("Paridad descubierta de tasas: i(PEN) = i(USD) + Δe esperada + prima de riesgo")
EQ("4,25% = 3,875% + (Δe + ρ)   →   Δe + ρ ≈ 0,375 pp")
T("Para el BCRP, ese 0,375 pp significa que el mercado acepta tener soles con una compensación mínima por depreciación y riesgo: si la Fed sube otra vez y el BCRP no responde, la paridad se rompe a favor del dólar. Para UCSUR, que cobra en soles y no reporta deuda en dólares relevante, el efecto pasa por el costo de lo que importa y por la tasa de los créditos que toman sus estudiantes.")
CAP("Gráfico 4. Tipo de Cambio Sol/Dólar, enero 2025 – noviembre 2026")
IMG("g4.png")
SRC("BCRPData, series PN01210PM (promedio mensual bancario) y PD04638PD (interbancario venta, 9 de noviembre de 2026).")
INT("El gráfico 4 muestra que el sol se apreció 10,2% durante 2025, de S/3,748 en enero a S/3,367 en diciembre, y que en 2026 se mantiene entre S/3,36 y S/3,45, pese a la Fed y al petróleo. Para UCSUR esa estabilidad es una ventaja: el presupuesto de equipos y licencias en dólares puede planificarse dentro de un rango estrecho de S/3,40-3,50.")
CAP("Cadena 4. Tasa Fed → Diferencial de Tasas → Tipo de Cambio → Costo Importado de UCSUR")
CHAIN(["↑ Fed 3,75%–4,00% (17-set-26)", "↓ Diferencial con BCRP a 0,375 pp", "↑ Presión al alza del TC (S/3,442 en oct-26)", "↑ Costo en soles de equipos y software", "▲ Mitigante: superávit comercial y compras del BCRP"])
SRC("Federal Reserve (2026); BCRP, RI setiembre 2026; BCRPData.")
CADENA_LINEA("↑ Tasa Fed → ↓ diferencial (0,375 pp) → ↑ tipo de cambio → ↑ costo en soles del equipamiento → ↓ margen UCSUR")
CAP("Modelo 2. Mercado Cambiario: Oferta y Demanda de Dólares, 2025–2026")
IMG("m2.png", 5.2)
SRC("BCRPData (tipo de cambio de diciembre de 2025 y 9 de noviembre de 2026); BCRP, RI setiembre 2026. Diagrama conceptual con valores observados.")
INT("El modelo 2 resume el año: la Fed y el petróleo desplazan la demanda de dólares de D$₀ a D$₁, pero la oferta abundante de dólares por el superávit comercial y la intervención del BCRP limita el alza a S/3,412. Mientras los términos de intercambio sigan en máximos, el traslado del dólar a los costos de UCSUR será acotado.")

SUB("5. Economía de Estados Unidos, dólar y costo del equipamiento académico importado")
T("UCSUR concentra su oferta en carreras de ciencias de la salud, ambientales y veterinaria, que requieren laboratorios, simuladores clínicos, equipos de diagnóstico y licencias de software fabricados o facturados en dólares. Su costo en soles depende del precio en origen y del tipo de cambio. La inflación PCE de Estados Unidos proyectada para 2026 es 3,7% (Fed, citada en BCRP, RI setiembre 2026), y el sol pasó de S/3,367 en diciembre de 2025 a S/3,412 el 9 de noviembre. Las compras de activos fijos de UCSUR sumaron S/82,5 millones en 2025, de modo que una parte relevante de su presupuesto de inversión está expuesta a ambos factores.")
EQ("Costo en soles = P_USD × (1 + π_EE.UU.) × E")
EQ("Equipo de US$1 MM:  1,00 × 3,367 = S/3,367 MM  →  1,037 × 3,412 = S/3,538 MM  (+5,1%)")
T("Para el BCRP, el cálculo ilustra el traslado de precios externos: con un sol estable, el encarecimiento proviene casi todo de la inflación de Estados Unidos y no de la depreciación. Para UCSUR, si el tipo de cambio sube a S/3,60, el mismo equipo costaría S/3,733 millones, 10,9% más que en diciembre de 2025.")
CAP("Gráfico 5. Costo en Soles de un Equipo Académico de US$1 MM: Efectos de Precio y Tipo de Cambio")
IMG("g5.png")
SRC("Cálculo con tipo de cambio de BCRPData (diciembre de 2025 y 9 de noviembre de 2026) e inflación PCE 2026 de 3,7% (Fed, citada en BCRP, RI setiembre 2026). Escenarios de S/3,50 y S/3,60 construidos a partir de ese cálculo.")
INT("El gráfico 5 muestra que cada 10 céntimos de alza del tipo de cambio añade cerca de 3 puntos porcentuales al costo del equipamiento. Para un plan de inversión del orden de S/80 millones al año, la diferencia entre comprar a S/3,41 o a S/3,60 equivale a unos S/4,5 millones, cifra comparable a las provisiones anuales de UCSUR.")
CAP("Cadena 5. Inflación de EE.UU. → Fed y Dólar → Precio del Equipamiento → Inversión de UCSUR")
CHAIN(["↑ Inflación PCE EE.UU. 3,7% (2026P)", "Fed 3,75%–4,00%; ↑ dólar", "↑ Precio en origen de equipos y licencias", "↑ Costo en soles +5,1% (dic-25 a nov-26)", "▲ Capex S/82,5 MM expuesto al dólar"])
SRC("BCRP, RI setiembre 2026; BCRPData; UCSUR, EEFF auditados 2025, estado de flujos de efectivo.")
CADENA_LINEA("↑ Inflación EE.UU. → ↑ dólar → ↑ costo en soles del equipamiento (+5,1%) → ↑ capex → ↓ flujo libre UCSUR")
T("El diagrama de Ishikawa agrupa en seis espinas los factores internacionales y su efecto sobre los ingresos y costos de UCSUR. Las espinas verdes empujan los ingresos (crecimiento mundial y términos de intercambio); las rojas empujan los costos (energía, Fed y dólar, equipamiento importado); la gris reúne los factores financieros que sostienen la estabilidad cambiaria.")
CAP("Diagrama 1. Ishikawa de Factores Internacionales que Afectan a UCSUR, 2026–2027")
IMG("i1.png")
SRC("BCRP, RI setiembre 2026; BCRPData; Federal Reserve (2026). Diagrama conceptual.")
INT("El diagrama 1 muestra que las espinas favorables actúan sobre la demanda y las desfavorables sobre los costos. Como la demanda de UCSUR depende del ingreso de las familias y no del comercio exterior, el entorno internacional le llega con rezago y atenuado, salvo en la energía, cuyo efecto es inmediato.")
CRIT("el entorno internacional de 2026 favorece a UCSUR por el lado del ingreso nacional y la perjudica por el lado de los costos. Los términos de intercambio crecen 18,1% y sostienen el empleo formal, pero esa riqueza se concentra en minería y en el fisco, y llega a las familias de Lima Sur con rezago. El petróleo, en cambio, se traslada en semanas a pasajes y tarifas: la inflación de 5,25% de octubre lo confirma. El crecimiento de 41,5% de los ingresos de UCSUR en 2025 no se explica por el entorno externo, que fue similar en 2024 y 2025; por eso el riesgo internacional relevante para la universidad no es una menor demanda, sino un costo operativo más alto en un año en que las familias pierden poder adquisitivo.")
ESTR("UCSUR debe blindar su estructura de costos frente a la energía y el dólar mientras el entorno externo siga siendo favorable para el ingreso nacional. Conviene negociar contratos de suministro eléctrico con precio fijo o con tope por 24 meses, programar las compras de equipamiento de laboratorio y simulación en tramos trimestrales con forwards de compra cuando el tipo de cambio esté por debajo de S/3,42, y fijar en soles los contratos de licencias de software que lo permitan. Con un capex anual cercano a S/80 millones, cubrir la mitad de la exposición evitaría hasta S/2,3 millones de sobrecosto si el sol llegara a S/3,60.")

doc.add_heading("Situación macroeconómica del Perú y perspectivas 2025–2027: dependencia de Universidad Científica del Sur S.A.C. del entorno nacional", level=2)

SUB("1. PBI, consumo privado y demanda de educación universitaria privada")
T("El PBI peruano creció 3,4% en 2025 y crecería 3,2% en 2026 y 3,0% en 2027, tras el recorte de 0,2 pp en cada año por El Niño extraordinario (BCRP, RI setiembre 2026). El último dato es agosto: +3,23% interanual, con 3,14% acumulado entre enero y agosto (INEI, vía BCRPData). El motor es la demanda interna, que crecería 6,2% en 2026: la inversión privada subiría 14,0% y el consumo privado 3,6%, mientras las exportaciones apenas crecerían 0,1%. Para UCSUR la variable relevante es el consumo privado, porque la pensión universitaria es un gasto de las familias que compite con vivienda, transporte y alimentación.")
EQ("PBI = C + I + G + (X − M)")
T("Para el BCRP, la identidad muestra que el crecimiento de 2026 es de demanda interna: el consumo privado aporta alrededor de dos tercios del PBI y crece 3,6%, mientras las importaciones (+10,8%) restan parte de ese impulso. Para UCSUR, ese mismo consumo privado es el ingreso de su mercado: si el consumo se desacelera a 3,0% en 2027, como prevé el RI, el espacio para subir pensiones se estrecha.")
CAP("Gráfico 6. PBI Mensual del Perú, enero 2025 – agosto 2026 (var. % interanual)")
IMG("g6.png")
SRC("BCRPData, serie PN01728AM, con datos del INEI; BCRP, RI setiembre 2026.")
INT("El gráfico 6 muestra un crecimiento estable alrededor de 3%, con baches en mayo y junio de 2026 por la menor producción primaria y una recuperación a 3,56% en julio y 3,23% en agosto. Es un ritmo compatible con la proyección de 3,2%, pero no con el crecimiento de dos dígitos de los ingresos de UCSUR: la universidad crece por encima de su mercado.")
T("La elasticidad ingreso de la demanda mide cuánto cambia la demanda de un bien cuando cambia el ingreso de los consumidores. Para UCSUR se calculó con la variación real de sus ingresos por derechos de enseñanza (deflactados por la inflación promedio de Lima) frente a la variación real del consumo privado y del PBI.")
EQ("ε = %Δ Ingresos reales de UCSUR / %Δ Consumo privado real")
EQ("2025:  ε = 39,39% / 3,63% = 10,85        2024:  ε = 27,66% / 2,77% = 9,99")
CAP("Tabla 2. Elasticidad Ingreso Aparente de la Demanda de UCSUR, 2023–2025")
APA(["Año", "Ingresos UCSUR (var. % nominal)", "Inflación promedio (%)", "Ingresos UCSUR (var. % real)", "PBI (var. % real)", "Consumo privado (var. % real)", "ε frente al PBI", "ε frente al consumo"], [
    ["2023", "21,84", "6,26", "14,66", "−0,35", "0,06", "n. s.", "n. s."],
    ["2024", "30,66", "2,35", "27,66", "3,52", "2,77", "7,87", "9,99"],
    ["2025", "41,48", "1,50", "39,39", "3,43", "3,63", "11,48", "10,85"],
    ["Promedio 2024–2025", "", "", "", "", "", "9,68", "10,42"],
], [1.05, 0.85, 0.75, 0.8, 0.7, 0.8, 0.7, 0.75])
SRC("UCSUR, EEFF auditados 2023-2025; BCRPData, PBI por tipo de gasto trimestral (series PN02528AQ, PN02529AQ, PN02536AQ y PN02537AQ, sumadas por año) e IPC de Lima Metropolitana (PN38705PM, promedio anual). n. s.: no significativa, porque el PBI y el consumo casi no variaron.")
T("Una elasticidad de 10,4 indica un bien de lujo en sentido estricto, pero esa lectura sería engañosa. En 2023 los ingresos reales de UCSUR subieron 14,7% con un PBI que cayó 0,35% y un consumo estancado (+0,06%), lo que prueba que la mayor parte del crecimiento proviene de captar estudiantes de otras instituciones y de abrir carreras, no del ingreso de las familias. Para el BCRP el dato confirma que la educación superior privada responde más que proporcionalmente al ciclo. Para UCSUR, la sensibilidad es la cifra útil: con ε = 10,4, cada punto porcentual menos de consumo privado se asocia a 10,4 puntos menos de crecimiento real de ingresos, unos S/62 millones sobre la base de 2025.")
CAP("Cadena 6. Consumo Privado → Gasto en Educación → Ingresos de UCSUR")
CHAIN(["↑ Consumo privado 3,6% (2026P) y 3,0% (2027P)", "↑ Gasto de familias en educación superior", "ε aparente = 10,4 (2024–2025)", "↑ Ingresos +41,5% (2025)", "▲ −1 pp de consumo ≈ −S/62 MM de ingresos"])
SRC("BCRP, RI setiembre 2026; BCRPData; UCSUR, EEFF auditados 2025.")
CADENA_LINEA("↓ Consumo privado (3,6% → 3,0%) → ↓ gasto en educación (ε = 10,4) → ↓ crecimiento de ingresos UCSUR (≈ −6 pp)")
CAP("Modelo 3. Oferta Agregada y Demanda Agregada: Perú 2025–2026")
IMG("m3.png", 5.2)
SRC("BCRP, RI setiembre 2026; BCRPData. Curvas ilustrativas con cifras observadas y proyectadas; diagrama conceptual.")
INT("El modelo 3 explica la combinación de 2026: la demanda agregada se desplaza a la derecha por la inversión privada (+14,0%) y la oferta agregada a la izquierda por el petróleo y El Niño. El resultado es un producto que crece 3,2%, cerca de su potencial, con una inflación que sube de 1,5% a entre 4,2% y 5,3%. Para UCSUR, el desplazamiento de la oferta es el que importa: eleva precios sin elevar los ingresos de las familias.")

SUB("2. Inflación y poder adquisitivo de las familias")
T("La inflación de Lima Metropolitana llegó a 5,25% interanual en octubre de 2026, con 0,57% mensual y 4,88% acumulado en el año (INEI, vía BCRPData). El origen es de oferta: combustibles, tarifas eléctricas y pasajes de transporte local, más el efecto de El Niño sobre alimentos. La inflación sin alimentos, energía y transporte era 1,8% en setiembre (BCRP, RI setiembre 2026) → El problema no es exceso de demanda, sino costos. El RI proyectó 4,2% para diciembre; para cumplirlo, noviembre y diciembre deberían sumar una variación de −0,65%, lo que es improbable, de modo que el cierre de 2026 se ubicaría por encima de 5%.")
EQ("Cierre 2026:  (1 + π dic) = (1 + 4,88%) × (1 + π nov-dic)   →   π nov-dic = 1,042 / 1,0488 − 1 = −0,65%")
T("Para el BCRP, el número dice que su proyección de setiembre quedó corta y que las expectativas (3,05%) ya están por encima del techo del rango meta. Para UCSUR, el dato más relevante es que el RI proyecta 5,3% de inflación de servicios en 2026: las familias perciben que todo lo que pagan de forma recurrente, incluida la pensión, sube más que su ingreso.")
CAP("Gráfico 7. Inflación en Lima Metropolitana y Expectativas, enero 2025 – octubre 2026 (%)")
IMG("g7.png")
SRC("BCRPData, series PN01273PM (IPC Lima, var. % 12 meses) y PD12912AM (expectativa de inflación a 12 meses); BCRP, RI setiembre 2026.")
INT("El gráfico 7 muestra que la inflación salió del rango meta en marzo de 2026 y no ha vuelto, mientras las expectativas suben de 2,8% a 3,05%. Para UCSUR esto significa que sus costos de personal y servicios subirán en 2027 por reajustes salariales, y que un alza de pensiones en línea con la inflación puede chocar con el ingreso real de sus estudiantes, que cae.")
CAP("Cadena 7. Petróleo y El Niño → Inflación → Ingreso Real → Pago de Pensiones")
CHAIN(["↑ Combustibles, tarifas y alimentos", "↑ Inflación Lima 5,25% (oct-26)", "↓ Ingreso real de Lima −4,0% (set-26)", "↓ Capacidad de pago de pensiones", "▲ ↑ Morosidad y deserción"])
SRC("BCRPData; BCRP, RI setiembre 2026.")
CADENA_LINEA("↑ Choque de oferta → ↑ inflación (5,25%) → ↓ ingreso real (−4,0%) → ↓ pago de pensiones → ↑ derechos por cobrar UCSUR (+139%)")

SUB("3. Tipo de cambio y su efecto sobre el costo importado")
T("UCSUR factura en soles y su exposición cambiaria es pequeña en el resultado, pero crece. La pérdida neta por diferencia de cambio pasó de S/0,1 millones en 2023 a S/0,4 millones en 2024 y S/1,7 millones en 2025 (EEFF auditados), en un año en que el sol se apreció, lo que sugiere pasivos o compromisos en dólares, posiblemente arrendamientos o proveedores del exterior. El riesgo mayor no está en el estado de resultados, sino en el capex: el equipamiento de laboratorios y la infraestructura tecnológica se pagan en dólares. Con un tipo de cambio de S/3,412 el 9 de noviembre y un rango esperado de S/3,40-3,50, el riesgo es moderado.")
CAP("Gráfico 8. Gastos Financieros, Diferencia de Cambio y Deuda Financiera de UCSUR, 2022–2025 (S/ millones)")
IMG("g8.png")
SRC("UCSUR, Estados financieros auditados 2023, 2024 y 2025, estado de resultados y estado de situación financiera.")
INT("El gráfico 8 muestra que la deuda financiera casi se duplicó entre 2022 y 2025 (de S/89,0 a S/172,8 millones), mientras los gastos financieros se estabilizaron en S/27,5 millones. Esos gastos incluyen S/12,0 millones de intereses por arrendamientos, de modo que la sensibilidad de UCSUR a la tasa de interés es mayor que su sensibilidad al tipo de cambio.")
CAP("Cadena 8. Tipo de Cambio → Costo Importado → Inversión → Resultado de UCSUR")
CHAIN(["TC S/3,412 (9-nov-26); rango S/3,40-3,50", "↑ Costo en soles de equipos y licencias", "↑ Capex (S/82,5 MM en 2025)", "↓ Diferencia de cambio −S/1,7 MM (2025)", "▲ Riesgo moderado; mayor en el capex que en resultados"])
SRC("BCRPData; UCSUR, EEFF auditados 2025.")
CADENA_LINEA("↑ Tipo de cambio → ↑ costo importado → ↑ capex y ↑ pérdida cambiaria (−S/1,7 MM) → ↓ utilidad UCSUR")

SUB("4. Empleo, salarios e ingresos de las familias de Lima")
T("La tasa de desempleo de Lima Metropolitana bajó de 5,7% a 4,4% entre los trimestres móviles terminados en setiembre de 2025 y de 2026, y la de los jóvenes de 14 a 24 años, de 13,9% a 11,3% (INEI, vía BCRPData). El empleo mejora, pero el ingreso no: el ingreso promedio mensual en Lima fue S/2.302 en el trimestre julio-setiembre de 2026, apenas 0,35% más que un año antes, lo que equivale a una caída real de 4,0% con la inflación de 4,5% de setiembre. Para UCSUR, el desempleo juvenil importa dos veces: muchos de sus estudiantes trabajan para pagar sus estudios, y la empleabilidad de sus egresados es su principal argumento de venta.")
CAP("Gráfico 9. Desempleo e Ingreso Promedio en Lima Metropolitana, enero 2025 – setiembre 2026")
IMG("g9.png")
SRC("BCRPData, series PN38063GM, PN38066GM y PN38070GM (promedio móvil de tres meses), con datos del INEI.")
INT("El gráfico 9 muestra la divergencia de 2026: más empleo y menos poder de compra. El ingreso nominal se estancó desde mayo alrededor de S/2.300 mientras la inflación subió a 5,25%. Para la familia de clase media de Lima Sur, una pensión que sube 5% pesa más que el año anterior, aunque haya más miembros trabajando.")
CAP("Cadena 9. Empleo → Ingreso Real → Capacidad de Pago → Retención de Estudiantes")
CHAIN(["↓ Desempleo Lima 4,4%; jóvenes 11,3%", "Ingreso nominal +0,35% (S/2.302)", "↓ Ingreso real −4,0%", "↓ Capacidad de pago de pensiones", "▲ ↑ Fraccionamiento y riesgo de deserción"])
SRC("BCRPData, con datos del INEI.")
CADENA_LINEA("↓ Desempleo → ↑ empleo; pero ↑ inflación → ↓ ingreso real (−4,0%) → ↓ capacidad de pago → ↑ cuentas por cobrar UCSUR")

SUB("5. Crédito educativo y financiamiento de las familias")
T("El crédito de consumo de las sociedades de depósito creció 13,2% interanual en setiembre de 2026, frente a 7,3% un año antes, y el crédito total al sector privado 10,3% (BCRPData). El BCRP mantiene su tasa de referencia en 4,25% desde setiembre de 2025, de modo que con expectativas de inflación de 3,05% (octubre) la tasa real ex ante es 1,20%, por debajo del rango neutral, y con la inflación de octubre la tasa real ex post es −1,00%. El crédito barato permite a las familias financiar estudios, pero UCSUR no lo está aprovechando: sus derechos de enseñanza por cobrar crecieron 139% en 2025, hasta S/48,8 millones, y el plazo de cobranza subió de 18 a 30 días. La universidad financia a sus estudiantes con su propio capital de trabajo, además de las becas públicas del Pronabec y de sus propios descuentos.")
EQ("Ecuación de Fisher: i = r + πᵉ   →   r ex ante = 4,25% − 3,05% = 1,20%;   r ex post = 4,25% − 5,25% = −1,00%")
T("Para el BCRP, una tasa real ex post negativa significa que su política es expansiva justo cuando la inflación supera el rango meta, lo que abre la puerta a un alza de 25 pb. Para UCSUR, un alza encarecería el crédito educativo de las familias y su propia deuda financiera de S/172,8 millones; por eso la ventana para firmar convenios de crédito educativo a tasa fija está en los próximos meses.")
CAP("Gráfico 10. Crédito de Consumo y Cobranza de UCSUR")
IMG("g10.png")
SRC("BCRPData, serie PN00537MM (crédito de consumo de las sociedades de depósito, var. % 12 meses); UCSUR, EEFF auditados 2023-2025, estado de situación financiera.")
INT("El gráfico 10 muestra dos ciclos que avanzan en paralelo: el crédito de consumo se acelera desde mediados de 2025 y las cuentas por cobrar de UCSUR saltan en 2025. La estimación para pérdidas crediticias de UCSUR subió de S/5,3 a S/6,5 millones (+23,3%) y los castigos de pensiones incobrables de S/2,0 a S/3,7 millones: el financiamiento directo a las familias ya tiene un costo.")
CAP("Cadena 10. Tasa de Referencia → Tasa Real → Crédito de Consumo → Pago de Pensiones")
CHAIN(["BCRP 4,25% (14 meses sin cambio)", "↓ Tasa real ex ante 1,20%; ex post −1,00%", "↑ Crédito de consumo +13,2% (set-26)", "↑ Financiamiento de estudios; ↑ cobranza propia 30 días", "▲ Alza a 4,50% encarece el crédito educativo"])
SRC("BCRPData; UCSUR, EEFF auditados 2025.")
CADENA_LINEA("↓ Tasa real (1,20%) → ↑ crédito de consumo (+13,2%) → ↑ financiamiento de pensiones → ↑ matrícula; si ↑ tasa → ↓ crédito → ↑ morosidad UCSUR")
CAP("Modelo 4. Modelo IS-MP: Crédito, Tasa Real y Producto, 2026")
IMG("m4.png", 5.2)
SRC("BCRPData (tasa de referencia y expectativas de inflación, octubre de 2026); BCRP, RI setiembre 2026. Diagrama conceptual.")
INT("El modelo 4 muestra la curva IS desplazada a la derecha por el crédito de consumo y la inversión privada, con una regla monetaria (MP) que fija la tasa real en 1,20%. Si el BCRP sube 25 pb para anclar las expectativas, la MP se desplaza hacia arriba y el producto se modera. Para UCSUR, un alza de tasas reduce la demanda financiada con crédito justo cuando más estudiantes dependen del fraccionamiento.")
T("El diagrama de Ishikawa doméstico reúne los factores de la economía peruana que determinan la matrícula, la cobranza y el margen de UCSUR. Las espinas verdes (PBI y consumo, empleo) sostienen la demanda; las rojas (inflación y crédito educativo) presionan la capacidad de pago; las grises (tasa y tipo de cambio) afectan el costo financiero e importado.")
CAP("Diagrama 2. Ishikawa de Factores Domésticos que Afectan a UCSUR, 2026–2027")
IMG("i2.png")
SRC("BCRP, RI setiembre 2026; BCRPData; UCSUR, EEFF auditados 2025. Diagrama conceptual.")
INT("El diagrama 2 muestra que la espina decisiva para 2026-2027 es la inflación: es la única que actúa a la vez sobre los ingresos (menor capacidad de pago), los costos (reajustes salariales y servicios) y la política monetaria (posible alza de tasas que encarece el crédito educativo).")
CRIT("la economía peruana de 2026 ofrece a UCSUR más empleo y más crédito, pero menos ingreso real. El desempleo de Lima bajó a 4,4% y el crédito de consumo crece 13,2%, mientras el ingreso promedio real cae 4,0% y la inflación llega a 5,25%. La elasticidad aparente de 10,4 no debe leerse como una garantía de crecimiento: refleja la ganancia de participación de 2023-2025, que no se repite indefinidamente. La señal de alerta ya está en el balance: las cuentas por cobrar crecieron 139% frente a ingresos que crecieron 41,5%. Parte del crecimiento de 2025 se financió con plazo a las familias, y una subida de tasas o una inflación persistente convertiría ese plazo en morosidad.")
ESTR("UCSUR debe pasar de financiar a sus estudiantes a facilitarles financiamiento. Conviene firmar convenios de crédito educativo con bancos y cajas a tasa fija antes de un posible alza del BCRP a 4,50%, con el objetivo de devolver los días de cobranza de 30 a 20, lo que liberaría unos S/16 millones de capital de trabajo sobre la base de 2025. Al mismo tiempo, el reajuste de pensiones de 2027 debería limitarse a ingresantes y a la inflación esperada (3%), no a la observada (5,25%), para proteger la retención de una base estudiantil cuyo ingreso real cae. El costo de esa moderación, unos 2 puntos de crecimiento de ingresos, es menor que el de perder estudiantes de los ciclos avanzados, que ya cubrieron el costo de captación.")

doc.save(OUT)
print("saved", OUT)

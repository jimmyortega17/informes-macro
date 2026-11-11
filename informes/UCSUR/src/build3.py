import os, sys
S = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(S, "lib3.py"), encoding="utf-8").read())

def pgN(key):
    return f"Página {PAGES.get(key, ['?'])[0]}."

def APA(header, rows, widths, bold_first_col=False):
    t = doc.add_table(rows=len(rows) + 1, cols=len(header)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for j, h in enumerate(header):
        c = t.rows[0].cells[j]; cell_lines(c, [(h, False)], WD_ALIGN_PARAGRAPH.CENTER if j else WD_ALIGN_PARAGRAPH.LEFT); borders(c, top=12, bottom=6)
    for i, row in enumerate(rows, 1):
        for j, v in enumerate(row):
            c = t.rows[i].cells[j]; cell_lines(c, [(v, False)], WD_ALIGN_PARAGRAPH.CENTER if j and len(header) > 2 else WD_ALIGN_PARAGRAPH.LEFT)
            borders(c, bottom=12 if i == len(rows) else None)
    fix_widths(t, [Inches(w) for w in widths])
    for k, r in enumerate(t.rows):
        trPr = r._tr.get_or_add_trPr(); trPr.append(OxmlElement("w:cantSplit"))
        if k < len(t.rows) - 1:
            for c in r.cells:
                for p in c.paragraphs: p.paragraph_format.keep_with_next = True

def H3(t): return SUB(t)

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
T("La economía mundial crecería 3,1% en 2026 y en 2027, debajo del 3,4% de 2025 (BCRP, RI setiembre 2026), y llega al Perú por dos variables. La primera son los términos de intercambio: China crece 4,5%, el cobre sube 36% hasta US$6,14 por libra y los términos de intercambio mejoran 18,1%, lo que eleva el ingreso nacional y el empleo formal, base de la demanda de UCSUR. La segunda es la inflación importada: el conflicto en Medio Oriente llevó el petróleo WTI de US$64,4 a US$98,9 por barril entre febrero y octubre, y la Reserva Federal subió su tasa a 3,75%–4,00% ante una inflación PCE de 3,7%. Para UCSUR, el mundo eleva con rezago el ingreso de las familias, pero encarece de inmediato su energía y su equipamiento importado, cuyo costo en soles ya subió 5,1%. " + pgN("s1int"))
T("El PBI peruano crecería 3,2% en 2026 y 3,0% en 2027, impulsado por la inversión privada (+14,0%) y el consumo privado (+3,6%); en agosto creció 3,23%. La inflación de Lima llegó a 5,25% en octubre, por encima del rango meta, por combustibles, tarifas y El Niño, mientras la liquidez en soles crece 16,7%. Con la tasa del BCRP en 4,25%, la tasa real ex post es −1,00%, lo que alienta el crédito de consumo (+13,2%) y anticipa un posible alza. El desempleo de Lima bajó a 4,4%, pero el ingreso real promedio cae 4,0%, y el sol se mantiene en S/3,412 por dólar con reservas de US$96.668 millones. Para UCSUR hay más familias con empleo y crédito para pagar pensiones, pero cada sol de pensión pesa más en un presupuesto con menor poder adquisitivo. " + pgN("s1peru"))
T("Universidad Científica del Sur S.A.C. (RUC 20421239275) opera en la educación superior universitaria privada y atiende a estudiantes de clase media de Lima Sur y a sus familias, que pagan pensiones en soles con su salario, con crédito o con becas. No depende de un cliente grande: su riesgo se reparte entre miles de hogares. Sus ingresos pasaron de S/264,1 millones en 2022 a S/594,8 millones en 2025, con un margen operativo de 36,9% y una utilidad neta de S/141,6 millones. Otorga crédito a sus estudiantes mediante el fraccionamiento de pensiones (S/48,8 millones por cobrar), recibe crédito de proveedores (S/40,0 millones) y de bancos (S/172,8 millones) y compra en dólares equipamiento de laboratorio. Así queda expuesta a las cuatro variables clave: PBI, inflación, tasa de interés y tipo de cambio. " + pgN("s2desc"))
T("La elasticidad aparente de las ventas reales frente al consumo privado fue 10,4 en 2024-2025, porque UCSUR ganó participación; con una elasticidad base de 5,2, las ventas llegarían a S/743 millones en 2026 y S/876 millones en 2027, y cada punto menos de consumo restaría S/31 millones. La inflación de 5,25% eleva en S/18,0 millones su planilla y gastos generales, resta S/2,6 millones al valor real de las cuentas por cobrar y alivia S/2,1 millones de las cuentas por pagar. Cada alza de 25 pb del BCRP cuesta S/0,43 millones sobre una deuda con costo implícito de 10,2%. Un tipo de cambio de S/3,60 encarecería 10,9% el equipamiento importado frente a diciembre de 2025. " + pgN("s2imp"))
T("Se recomienda: (R1) reajustar las pensiones con la inflación esperada (3,05%) y no con la observada (5,25%), aplicado sobre todo a ingresantes, para proteger la retención mientras el ingreso real cae 4,0%; (R2) fijar la tasa de la deuda de S/172,8 millones antes de que el BCRP corrija una tasa real negativa; (R3) trasladar el fraccionamiento a convenios de crédito educativo con bancos y cajas, aprovechando el crédito de consumo (+13,2%), para bajar la cobranza de 30 a 20 días; y (R4) cubrir con forwards la mitad del capex en dólares mientras el diferencial con la Fed sea 0,375 pp. El análisis costo-beneficio estima beneficios de S/35,6 millones frente a costos de S/16,8 millones en 2026-2027. " + pgN("s3"))

# ================= SECCIÓN 1 =================
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

H1("SECCIÓN 1"); MARK("s1int")
H2("Análisis de la economía internacional y sus incidencias sobre la economía del país en que la empresa desarrolla sus principales actividades")

SUB("1. Crecimiento económico mundial (Y*) y PBI peruano (Y): empleo y demanda de educación superior")
T("El BCRP mantuvo en 3,1% el crecimiento mundial para 2026 y 2027, debajo del 3,4% de 2025 (RI setiembre 2026). El conflicto en Medio Oriente resta actividad, pero la inversión en inteligencia artificial y la transición energética la compensan: Estados Unidos crecería 2,2%, China 4,5% y América Latina 2,2%. El Perú (3,2%) crece por encima del promedio porque exporta los metales que esa inversión demanda: el cobre promedió US$6,14 por libra entre enero y octubre de 2026, 36% más que en 2025 (BCRPData). Ese ingreso externo se convierte en empleo: el sector privado formal sumó alrededor de 242 mil puestos en lo que va de 2026 (BCRP, RI setiembre 2026). UCSUR no exporta, pero su demanda depende del empleo de las familias de Lima Sur; por eso Y* le llega a través de Y, del empleo y del consumo, con rezago.")
CAP("Gráfico 1. Crecimiento del PBI por Economía, 2025–2027 (var. % real)")
IMG("g1.png")
SRC("BCRP, Reporte de Inflación setiembre 2026, con base en FMI y Consensus Forecast.")
INT("El gráfico 1 muestra que el Perú crece 0,1 pp por encima del mundo y 1,0 pp por encima de América Latina en 2026. Esa diferencia financia empleo formal, que es la base de la matrícula universitaria privada de clase media.")
CADENA("Cadena 1. Crecimiento Mundial (Y*) → PBI Peruano (Y) → Ingresos de UCSUR",
       [("↑Y*", "Mundo 3,1%; China 4,5%"), ("↑Px", "Cobre +36%"), ("↑TI", "+18,1% (2026)"), ("↑Y", "Perú 3,2%"), ("↑Empleo", "+242 mil formales"), ("↑Ventas UCSUR", "S/594,8 MM (2025)")],
       "Si crece la economía mundial → suben los precios de los metales y los términos de intercambio → crece el PBI peruano y el empleo formal → las familias de Lima Sur matriculan y pagan pensiones → suben los ingresos de UCSUR.")
CADENA("Cadena 2. Crecimiento Mundial (Y*) → Inflación (P) y Tasa de Interés (i): Ajuste hasta Y = Yn",
       [("↑Y*", "Aceleración mundial; WTI US$98,9"), ("Y > Yn", "DA +6,2% (2026P)"), ("↑P", "π 5,25% (oct-26)"), ("↓M/P", "Saldos reales a la baja"), ("↑i", "Presión sobre 4,25%"), ("↓Y", "3,0% (2027P), hasta Y = Yn")],
       "Si la demanda externa y la inversión empujan la demanda interna (+6,2%) por encima del producto potencial → suben los precios (5,25%) → caen los saldos reales → sube la tasa de interés → se modera el PBI a 3,0% en 2027 hasta que Y = Yn. Para UCSUR, la fase de ajuste significa crédito educativo más caro y matrícula 2027 más lenta.")

SUB("2. Precios internacionales de commodities: energía y equipamiento importado")
T("El petróleo WTI promedió US$98,9 por barril en octubre de 2026, frente a US$64,4 en febrero, antes del conflicto en Medio Oriente, y a US$65,5 de promedio en 2025 (BCRPData). El RI de setiembre supuso US$82 para 2026, de modo que el precio de octubre lo supera en 21%. El cobre, en cambio, promedió US$6,59 por libra en octubre, en línea con los 615 centavos que el RI proyecta para el año. El alza de la energía se trasladó a combustibles, tarifas eléctricas y pasajes, y explica que la inflación de Lima llegue a 5,25% mientras la inflación sin alimentos, energía y transporte es solo 1,8%. Para UCSUR la energía pesa por dos lados: encarece la operación de laboratorios, clínicas y campus, dentro de gastos generales de S/128,2 millones en 2025, y reduce el ingreso disponible del estudiante que gasta más en transporte.")
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

SUB("3. Política monetaria global (i*) y tipo de cambio (E)")
T("La Reserva Federal subió su tasa 25 pb el 17 de setiembre de 2026, a 3,75%–4,00%, después de haberla recortado a 3,50%–3,75% en diciembre de 2025 (Federal Reserve, 2026). Con el BCRP en 4,25%, el diferencial frente al punto medio de la Fed se redujo a 0,375 pp. El sol, sin embargo, se mantiene estable: S/3,442 de promedio en octubre y S/3,412 el 9 de noviembre, frente a S/3,367 en diciembre de 2025 (BCRPData), porque el superávit comercial y las compras del BCRP compensan el menor atractivo de las tasas en soles.")
EQ("Paridad descubierta de tasas: i = i* + Δe esperada + ρ")
EQ("4,25% = 3,875% + (Δe + ρ)   →   Δe + ρ = 0,375 pp")
T("Para el BCRP, ese 0,375 pp es el margen que compensa al inversionista por depreciación esperada y riesgo: si la Fed sube de nuevo y el BCRP no responde, la paridad presiona al sol. Para UCSUR, que cobra en soles, el efecto llega por el costo de lo que importa (equipos y licencias de software), no por sus ventas.")
CAP("Gráfico 3. Tipo de Cambio Sol/Dólar, enero 2025 – noviembre 2026")
IMG("g3.png")
SRC("BCRPData, series PN01210PM (promedio mensual bancario) y PD04638PD (interbancario venta, 9 de noviembre de 2026).")
INT("El gráfico 3 muestra que el sol se apreció 10,2% en 2025 (de S/3,748 a S/3,367) y que en 2026 oscila entre S/3,36 y S/3,45. Para UCSUR, esa estabilidad permite presupuestar el capex en dólares dentro de un rango de S/3,40–3,50.")
CAP("Modelo 2. Mercado Cambiario: Oferta y Demanda de Dólares, diciembre 2025 – noviembre 2026")
IMG("m2.png", 5.6)
SRC("BCRPData; BCRP, RI setiembre 2026. Diagrama conceptual con valores observados.")
INT("El modelo 2 muestra que la Fed y el petróleo desplazan la demanda de dólares de D$₀ a D$₁, pero la oferta abundante limita el alza: el equilibrio pasa de E₀ (S/3,367) a E₁ (S/3,412), apenas +1,3%. Mientras se mantenga esa oferta, el traslado cambiario a los costos de UCSUR será acotado.")
CADENA("Cadena 4. Tasa de la Fed (i*) → Tipo de Cambio (E) → Costo Importado de UCSUR",
       [("↑i*", "Fed 3,75%–4,00%"), ("↓(i − i*)", "0,375 pp"), ("↑Salida de capital", "No residentes 45%"), ("↑E", "S/3,367 → S/3,412"), ("↑Costo importado", "Equipos y licencias"), ("↑Capex UCSUR", "S/82,5 MM (2025)")],
       "Si sube la tasa de la Fed → se reduce el diferencial de tasas → salen capitales → sube el tipo de cambio → sube el costo en soles del equipamiento → sube el capex de UCSUR.")

SUB("4. Términos de intercambio (TI) y balanza de pagos (BP)")
T("Los términos de intercambio crecerían 18,1% en 2026 y alcanzarían en 2027 su nivel más alto desde que hay registro, por el cobre y el oro (BCRP, RI setiembre 2026). Las exportaciones sumarían US$119.876 millones y las importaciones US$71.011 millones, con un saldo comercial de US$48.865 millones (12,1% del PBI). La cuenta corriente tendría un superávit de 4,0% del PBI, su quinto año seguido, y el BCRP compró US$15.715 millones en 2026; las reservas llegaron a US$96.668 millones el 9 de noviembre (BCRPData).")
EQ("Balanza de pagos: BP = CA + KA + ER")
EQ("CA = +4,0% del PBI   →   KA + ER = −4,0% del PBI   →   ↑RIN (compras BCRP US$15.715 MM)")
T("Para el BCRP, la ecuación dice que el superávit corriente se compensa con salida de capitales y acumulación de reservas: el banco central compra dólares para que el exceso de oferta no aprecie en exceso al sol. Para UCSUR, esas reservas son un seguro que reduce la probabilidad de un salto cambiario que encarezca su equipamiento.")
CAP("Gráfico 4. Balanza Comercial del Perú, 2025–2027 (US$ miles de millones)")
IMG("g4.png")
SRC("BCRP, Reporte de Inflación setiembre 2026, cuadro de balanza comercial.")
INT("El gráfico 4 muestra que el saldo comercial sube de US$35.433 millones en 2025 a US$48.865 millones en 2026, aunque las importaciones crecen más rápido. Para UCSUR, ese exceso de dólares mantiene acotado el costo de su equipamiento importado.")
CADENA("Cadena 5. Términos de Intercambio (TI) → Balanza de Pagos (BP) → Tipo de Cambio (E) → UCSUR",
       [("↑TI", "+18,1% (2026)"), ("↑CA", "+4,0% del PBI"), ("↑Oferta de US$", "Saldo US$48.865 MM"), ("↑RIN", "US$96.668 MM"), ("E estable", "S/3,40–3,50"), ("↓Riesgo cambiario", "Capex de UCSUR")],
       "Si mejoran los términos de intercambio → sube el superávit en cuenta corriente → entran más dólares y el BCRP acumula reservas → el tipo de cambio se mantiene estable → baja el riesgo cambiario del capex de UCSUR.")

SUB("5. Inflación de Estados Unidos (π*) y dólar: costo del equipamiento académico importado")
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

SUB("Herramientas de análisis macroeconómico aplicadas al entorno internacional")
SUB("1.1 Cadenas de razonamiento")
T("Las seis cadenas del entorno internacional enlazan dos variables macroeconómicas y llegan a UCSUR por el ingreso de las familias o por sus costos. La tabla 1 las resume en notación macroeconómica.")
CAP("Tabla 1. Cadenas de Razonamiento del Entorno Internacional y su Efecto en UCSUR")
APA(["Cadena", "Variables", "Notación con cifras", "Efecto en UCSUR"], [
    ["1", "Y* → Y", "↑Y* 3,1% → ↑TI 18,1% → ↑Y 3,2% → ↑empleo", "↑Matrícula y pensiones"],
    ["2", "Y* → P → i", "↑Y* → Y > Yn → ↑P 5,25% → ↓M/P → ↑i → ↓Y 3,0%", "Crédito educativo más caro en 2027"],
    ["3", "WTI → P", "↑WTI +53,5% → ↑π 5,25% → ↓w/P −4,0%", "↑Costos y ↓capacidad de pago"],
    ["4", "i* → E", "↑i* 3,875% → ↓(i − i*) 0,375 pp → ↑E S/3,412", "↑Costo del equipamiento"],
    ["5", "TI → BP → E", "↑TI → ↑CA 4,0% PBI → ↑RIN US$96.668 MM → E estable", "↓Riesgo cambiario"],
    ["6", "π* → E", "↑π* 3,7% → ↑E → ↑P*×E +5,1%", "↑Capex en soles"],
], [0.55, 1.0, 3.0, 1.9])
SRC("Elaborado a partir de las cadenas 1 a 6 de esta sección; BCRP, RI setiembre 2026; BCRPData; Federal Reserve (2026).")
SUB("1.2 Fórmulas macroeconómicas explícitas")
CAP("Tabla 2. Fórmulas Macroeconómicas Aplicadas al Entorno Internacional")
APA(["Fórmula", "Cálculo con cifras", "Lectura para UCSUR"], [
    ["Paridad de tasas: i = i* + Δe + ρ", "4,25% = 3,875% + 0,375 pp", "Sol sostenido por reservas, no por tasas"],
    ["Balanza de pagos: BP = CA + KA + ER", "CA +4,0% PBI; compras BCRP US$15.715 MM", "Menor riesgo de salto cambiario"],
    ["Costo importado: P* × (1 + π*) × E", "1,037 × 3,412 = S/3,538 MM por US$1 MM", "Equipamiento +5,1% en soles"],
    ["Términos de intercambio: TI = Px / Pm", "Px +28,1%; Pm +8,5% → TI +18,1%", "Más ingreso nacional y empleo"],
], [2.2, 2.3, 1.95])
SRC("BCRP, RI setiembre 2026; BCRPData; Federal Reserve (2026).")
SUB("1.3 Análisis causa-efecto: diagrama de Ishikawa")
T("El diagrama de Ishikawa agrupa los seis factores internacionales. Las espinas verdes (crecimiento mundial y términos de intercambio) empujan el ingreso de las familias; las rojas (petróleo, Fed, inflación de EE.UU.) empujan los costos de UCSUR; la gris resume la estabilidad financiera externa.")
CAP("Diagrama 1. Ishikawa de Factores Internacionales que Afectan a UCSUR, 2026–2027")
IMG("i1.png")
SRC("BCRP, RI setiembre 2026; BCRPData; Federal Reserve (2026). Diagrama conceptual.")
INT("El diagrama 1 muestra que las espinas favorables actúan sobre la demanda con rezago y las desfavorables sobre los costos de inmediato. El riesgo internacional relevante para UCSUR no es una caída de matrícula, sino un costo operativo y de inversión más alto en 2026.")
CRIT("el entorno internacional de 2026 favorece a UCSUR por el ingreso nacional y la perjudica por los costos, y ambos efectos llegan a destiempo. Los términos de intercambio crecen 18,1% y el superávit comercial llega a US$48.865 millones, pero esa riqueza se concentra en minería y en el fisco y llega a las familias de Lima Sur con rezago, a través del empleo formal (242 mil puestos). El petróleo, en cambio, pasó de US$64,4 a US$98,9 en ocho meses y se trasladó en semanas a pasajes y tarifas: la inflación de 5,25% de octubre lo confirma, con un ingreso real que cae 4,0%. La Fed agrega una tercera presión: con un diferencial de solo 0,375 pp, el sol depende de las compras del BCRP y no de las tasas. El crecimiento de 41,5% de los ingresos de UCSUR en 2025 no se explica por el entorno externo, que fue similar en 2024 y 2025; por eso la universidad no debe leer el buen momento minero como una garantía de demanda, sino como un viento de cola que puede revertirse si el cobre cae o si la Fed vuelve a subir.")
ESTR("UCSUR debe usar la estabilidad cambiaria que hoy le dan el superávit externo y las reservas de US$96.668 millones para blindar su estructura de costos antes de que el ciclo cambie. Con un capex del orden de S/80 millones al año y un diferencial de tasas de 0,375 pp, conviene comprar forwards para la mitad de sus compras de equipamiento de 2027 mientras el tipo de cambio esté por debajo de S/3,45; si el sol llegara a S/3,60, esa cobertura evitaría hasta S/2,3 millones de sobrecosto. Frente al petróleo a US$98,9, debe negociar contratos de energía con precio fijo o tope por 24 meses, porque la inflación de energía se traslada a sus costos antes que a sus pensiones. Y debe programar las compras de equipos en tramos trimestrales y priorizar proveedores con precios fijados en soles, para promediar el tipo de cambio en un año en que la Fed puede volver a subir. Estas medidas no dependen de la matrícula: protegen el margen de 36,9% justo cuando el entorno internacional deja de ser un viento de cola y pasa a ser una fuente de costos.")

H2("Situación macroeconómica del Perú y perspectivas 2025–2027: Dependencia de Universidad Científica del Sur S.A.C. del entorno nacional"); MARK("s1peru")

SUB("1. PBI sectorial y por tipo de gasto: el consumo privado como mercado de UCSUR")
T("El PBI peruano creció 3,4% en 2025 y crecería 3,2% en 2026 y 3,0% en 2027 (BCRP, RI setiembre 2026). El dato más reciente es agosto: +3,23% interanual y 3,14% acumulado en el año (INEI, vía BCRPData). Por sectores, el RI prevé que los no primarios crezcan (construcción 9,5%, comercio 5,9%, servicios 4,3%) y los primarios retrocedan por El Niño (pesca −30,7%). Por tipo de gasto, la demanda interna crecería 6,2%, impulsada por la inversión privada (+14,0%) y el consumo privado (+3,6%), mientras las exportaciones apenas suben 0,1%. Con las ponderaciones reales de 2025, la identidad del gasto cuadra con la proyección oficial:")
EQ("PBI = C + I + G + (X − M)")
EQ("3,20% = 2,36 (C: 65,6% × 3,6%) + 2,87 (Ipriv: 20,5% × 14,0%) + 0,06 (Ipub) + 0,70 (inventarios) + 0,45 (G: 14,2% × 3,2%) + 0,03 (X) − 3,27 (M: 30,3% × 10,8%)")
T("Para el BCRP, el resultado dice que el crecimiento de 2026 es de demanda interna: consumo e inversión aportan 5,23 pp y las importaciones restan 3,27 pp. Para UCSUR, el consumo privado es su mercado: la pensión universitaria compite con vivienda, transporte y alimentación, y su desaceleración a 3,0% en 2027 estrechará el espacio para subir precios. Los servicios, sector al que pertenece la educación, crecerían 4,3%.")
CAP("Gráfico 6. PBI Mensual del Perú, enero 2025 – agosto 2026 (var. % interanual)")
IMG("g6.png")
SRC("BCRPData, serie PN01728AM, con datos del INEI; BCRP, RI setiembre 2026.")
INT("El gráfico 6 muestra un crecimiento estable alrededor de 3%, con baches en mayo y junio de 2026 por la producción primaria, y una recuperación a 3,56% en julio y 3,23% en agosto, compatible con la proyección de 3,2%.")
CAP("Modelo 3. Oferta Agregada y Demanda Agregada: Perú 2025–2026")
IMG("m3.png", 5.6)
SRC("BCRP, RI setiembre 2026; BCRPData. Diagrama conceptual con cifras observadas y proyectadas.")
INT("El modelo 3 muestra que la demanda agregada se desplazó a la derecha (DA₁) por la inversión privada y el consumo, y la oferta agregada a la izquierda (OA₁) por el petróleo y El Niño. El equilibrio pasa de E₀ (π 1,5%; PBI 3,4%) a E₁ (π 5,25%; PBI 3,2%): más precios con casi el mismo producto. Para UCSUR, OA₁ es la curva que importa, porque sube los precios sin subir el ingreso de sus familias.")
CADENA("Cadena 7. Consumo Privado (C) → PBI (Y) → Demanda de UCSUR",
       [("↑C", "+3,6% (2026P)"), ("↑Y", "+3,2% (2026P)"), ("↑Servicios", "+4,3% (2026P)"), ("↑Gasto en educación", "Familias de Lima Sur"), ("↓C en 2027", "+3,0%"), ("↓Demanda UCSUR", "Menor espacio de precios")],
       "Si crece el consumo privado → crece el PBI y el sector servicios → sube el gasto de las familias en educación superior; si el consumo se desacelera a 3,0% en 2027 → se reduce el espacio para subir pensiones.")

SUB("2. Inflación (P) y poder adquisitivo del consumidor")
T("La inflación de Lima llegó a 5,25% en octubre de 2026, con 0,57% mensual y 4,88% acumulado en el año (INEI, vía BCRPData). El origen es de oferta: combustibles, tarifas eléctricas, pasajes y El Niño; la inflación sin alimentos, energía y transporte era 1,8% en setiembre (BCRP, RI setiembre 2026). El RI proyectó 4,2% para diciembre; para cumplirlo, noviembre y diciembre deberían sumar −0,65%, lo que es improbable, de modo que 2026 cerraría por encima de 5%. Las expectativas a 12 meses están en 3,05%, sobre el techo del rango meta, y el RI prevé una inflación de servicios de 5,3% en 2026.")
EQ("Cierre 2026:  (1 + π dic) = (1 + 4,88%) × (1 + π nov-dic)   →   π nov-dic = 1,042 / 1,0488 − 1 = −0,65%")
CAP("Gráfico 7. Inflación en Lima Metropolitana y Expectativas, enero 2025 – octubre 2026 (%)")
IMG("g8.png")
SRC("BCRPData, series PN01273PM y PD12912AM; BCRP, RI setiembre 2026.")
INT("El gráfico 7 muestra que la inflación salió del rango meta en marzo de 2026 y no volvió, mientras las expectativas suben de 2,8% a 3,05%. Para las familias que pagan pensiones, todo gasto recurrente sube más que su ingreso.")
CADENA("Cadena 8. Inflación (P) → Salario Real (w/P) → Poder Adquisitivo de las Familias",
       [("↑P", "π 5,25% (oct-26)"), ("w nominal", "+0,35%"), ("↓w/P", "−4,0% real"), ("↓Poder de compra", "Familias de Lima Sur"), ("↑Peso de la pensión", "Servicios +5,3%"), ("↑Riesgo de deserción", "Matrícula UCSUR")],
       "Si sube la inflación más que los salarios → cae el salario real → baja el poder de compra de las familias → la pensión pesa más en su presupuesto → aumenta el riesgo de deserción en UCSUR.")

SUB("3. Tipo de cambio (E) y su efecto sobre el costo importado")
T("El sol cotizó S/3,412 por dólar el 9 de noviembre de 2026, apenas 1,3% por encima del promedio de diciembre de 2025, después de apreciarse 10,2% en 2025 (BCRPData). El BCRP compró US$15.715 millones en 2026 para moderar la apreciación, y el RI destaca al sol como la moneda más estable de la región. Para la economía, un sol estable limita el traslado cambiario a precios; para UCSUR, que importa equipamiento académico y paga licencias en dólares, significa un costo de inversión predecible dentro de un rango de S/3,40–3,50.")
CADENA("Cadena 9. Tipo de Cambio (E) → Precios Importados (P*×E) → Costos de UCSUR",
       [("↑i*", "Fed 3,75%–4,00%"), ("↑E", "S/3,367 → S/3,412"), ("↑P* × E", "+5,1% por equipo"), ("↑Capex", "S/82,5 MM (2025)"), ("↑Pérdida cambiaria", "−S/1,7 MM (2025)"), ("↓Utilidad UCSUR", "S/141,6 MM (2025)")],
       "Si sube el tipo de cambio → sube el precio en soles de lo importado → sube el capex y la pérdida cambiaria → se reduce la utilidad de UCSUR.")

SUB("4. Empleo, salarios y consumo de las familias de Lima")
T("La tasa de desempleo de Lima Metropolitana bajó de 5,7% a 4,4% entre los trimestres móviles terminados en setiembre de 2025 y 2026, y la de los jóvenes de 14 a 24 años, de 13,9% a 11,3% (INEI, vía BCRPData). El empleo formal privado nacional sumó alrededor de 242 mil puestos en el año (BCRP, RI setiembre 2026). El ingreso, en cambio, no acompaña: el ingreso promedio mensual en Lima fue S/2.302, apenas 0,35% más que un año antes, lo que equivale a una caída real de 4,0% con la inflación de setiembre (4,5%). Para UCSUR, el desempleo juvenil importa dos veces: muchos de sus estudiantes trabajan para pagar sus estudios, y la empleabilidad de sus egresados es su principal argumento de venta.")
CAP("Gráfico 8. Desempleo e Ingreso Promedio en Lima Metropolitana, enero 2025 – setiembre 2026")
IMG("g11.png")
SRC("BCRPData, series PN38063GM, PN38066GM y PN38070GM (promedio móvil de tres meses), con datos del INEI.")
INT("El gráfico 8 muestra la divergencia de 2026: más empleo y menos poder de compra. Para la familia de clase media de Lima Sur, una pensión que sube 5% pesa más que el año anterior, aunque haya más miembros trabajando.")
CADENA("Cadena 10. Empleo (N) → Ingreso de los Hogares (w × N) → Consumo (C) → Matrícula",
       [("↓u", "Lima 4,4%; jóvenes 11,3%"), ("↑N", "+242 mil formales"), ("w nominal", "S/2.302 (+0,35%)"), ("↓w/P", "−4,0% real"), ("C moderado", "+3,6% → +3,0%"), ("Matrícula", "Más alumnos, menos capacidad de pago")],
       "Si baja el desempleo → sube el número de hogares con ingreso; pero si la inflación supera al salario → el consumo se modera → más familias acceden a la universidad, pero con menor capacidad de pago.")

SUB("5. Crédito educativo y financiamiento de las familias: liquidez y dinero")
T("La liquidez en soles de las sociedades de depósito creció 16,7% interanual en setiembre de 2026 y el crédito de consumo 13,2%, frente a 7,3% un año antes; el crédito total al sector privado creció 10,3% (BCRPData). Ese crédito es la vía por la que muchas familias financian estudios: préstamos de consumo, tarjetas, créditos educativos de bancos y cajas, además de las becas y créditos públicos del Pronabec. La teoría cuantitativa permite leer el exceso de liquidez:")
EQ("M × V = P × Y   →   %ΔM + %ΔV = %ΔP + %ΔY")
EQ("16,7% + %ΔV = 4,5% + 3,2%   →   %ΔV = −9,0%")
T("Para el BCRP, una caída de 9,0% en la velocidad significa que el público retiene más dinero del que gasta: hay liquidez acumulada que puede convertirse en demanda y en precios si las expectativas suben, lo que justifica vigilar la tasa. Para UCSUR, esa liquidez es hoy una fuente de pago de pensiones y de crédito educativo; si el BCRP la retira con alzas de tasa, la cobranza se volverá más difícil.")
CAP("Gráfico 9. Liquidez en Soles e Inflación, enero 2025 – octubre 2026 (var. % 12 meses)")
IMG("g9.png")
SRC("BCRPData, series PN00189MM (liquidez en soles de las sociedades de depósito) y PN01273PM; BCRP, RI setiembre 2026.")
INT("El gráfico 9 muestra que la liquidez pasó de crecer 4,2% a fines de 2025 a entre 16,7% y 17,7% en 2026, mientras la inflación subió de 1,5% a 5,25%. Para las familias de Lima Sur, el crédito es hoy abundante; para UCSUR, es una oportunidad de financiar matrícula sin usar su propio capital de trabajo.")
CADENA("Cadena 11. Dinero (M) → Crédito de Consumo → Financiamiento Educativo",
       [("↑M", "Liquidez +16,7%"), ("↓V", "−9,0%"), ("↑Crédito de consumo", "+13,2% (set-26)"), ("↑Financiamiento de estudios", "Bancos y cajas"), ("↑P", "π 5,25%"), ("↑i (riesgo)", "Ajuste monetario 2027")],
       "Si la liquidez crece más que la economía → se expande el crédito de consumo → más familias financian estudios; pero el exceso de dinero presiona precios → el BCRP puede subir la tasa → el crédito educativo se encarece en 2027.")

SUB("6. Política monetaria: tasa de referencia y tasa real (i)")
T("El BCRP mantiene su tasa de referencia en 4,25% desde setiembre de 2025 (BCRPData). Con expectativas de inflación de 3,05% (octubre) y una inflación observada de 5,25%:")
EQ("Fisher: i = r + πᵉ   →   r = i − πᵉ")
EQ("r ex ante = 4,25% − 3,05% = 1,20%        r ex post = 4,25% − 5,25% = −1,00%")
T("Para el BCRP, una tasa real ex ante de 1,20%, debajo del nivel neutral, y una ex post negativa indican una política expansiva justo cuando la inflación supera el rango meta; un alza de 25 pb sería coherente con anclar las expectativas. Para UCSUR, la tasa determina el costo del crédito con que sus estudiantes pagan pensiones y el de su propia deuda.")
CAP("Modelo 4. IS-MP: Crédito, Tasa Real y Producto, 2026")
IMG("m5.png", 5.6)
SRC("BCRPData (tasa de referencia y expectativas, octubre de 2026); BCRP, RI setiembre 2026. Diagrama conceptual.")
INT("El modelo 4 muestra la curva IS desplazada a la derecha (IS₁) por el crédito de consumo (+13,2%) y la inversión privada (+14,0%), con la regla monetaria MP₀ en r = 1,20% (E₁). Si el BCRP sube 25 pb, la MP pasa a MP₁ y el producto se modera en E₂. Para UCSUR, E₂ significa menos crédito para pensiones y más morosidad.")
CADENA("Cadena 12. Inflación (P) → Tasa de Interés (i) → Crédito y Demanda",
       [("↑P", "π 5,25%"), ("↓r", "Ex post −1,00%"), ("↑i BCRP", "4,25% → 4,50% (escenario)"), ("↑Tasas de crédito", "Consumo y empresas"), ("↓Crédito", "Menor financiamiento"), ("↓Y", "3,2% → 3,0%")],
       "Si la inflación supera el rango meta → la tasa real cae → el BCRP sube la tasa → suben las tasas de crédito → se desacelera el crédito → se modera el PBI.")

SUB("7. Política fiscal (G): consumo público, déficit y becas")
T("El RI de setiembre proyecta un consumo público de 3,2% en 2026 y 2,3% en 2027, un déficit fiscal de 1,5% del PBI en ambos años y una deuda pública que bajaría de 30,1% a 28,2% del PBI entre 2025 y 2027 (BCRP, RI setiembre 2026). La política fiscal es prudente: aporta 0,45 pp al crecimiento de 2026 y no presiona la inflación. Para UCSUR, el canal fiscal es indirecto pero relevante: parte de sus estudiantes accede a becas y créditos públicos (Pronabec), cuyo presupuesto depende del gasto corriente. Un consumo público que se desacelera de 3,2% a 2,3% limita la expansión de esos programas justo cuando el ingreso real de las familias cae.")
CADENA("Cadena 13. Política Fiscal (G) → Consumo Público → Demanda Financiada de UCSUR",
       [("↓Déficit", "1,5% del PBI"), ("↓G", "3,2% → 2,3%"), ("↓Becas", "Pronabec"), ("↓Demanda becada", "Familias de Lima Sur"), ("↑Uso de crédito", "Consumo +13,2%"), ("↑CxC UCSUR", "S/48,8 MM")],
       "Si el fisco consolida y el consumo público se desacelera → crecen menos los programas de becas → más estudiantes dependen de crédito o fraccionamiento → aumentan las cuentas por cobrar de UCSUR.")

SUB("Herramientas de análisis macroeconómico aplicadas al entorno peruano")
SUB("2.1 Cadenas de razonamiento")
CAP("Tabla 3. Cadenas de Razonamiento del Entorno Peruano y su Efecto en UCSUR")
APA(["Cadena", "Variables", "Notación con cifras", "Efecto en UCSUR"], [
    ["7", "C → Y", "↑C 3,6% → ↑Y 3,2% → ↑servicios 4,3%", "↑Demanda; menor espacio en 2027"],
    ["8", "P → w/P", "↑P 5,25% → w +0,35% → ↓w/P −4,0%", "↑Riesgo de deserción"],
    ["9", "E → P*×E", "↑E S/3,412 → ↑P*×E +5,1%", "↑Capex y pérdida cambiaria"],
    ["10", "N → C", "↓u 4,4% → ↑N 242 mil → ↓w/P → C 3,0%", "Más alumnos, menos capacidad de pago"],
    ["11", "M → crédito", "↑M 16,7% → ↓V −9,0% → ↑crédito 13,2%", "Financiamiento de matrícula"],
    ["12", "P → i", "↑P → ↓r −1,00% → ↑i 4,50% → ↓crédito", "Crédito educativo más caro"],
    ["13", "G → becas", "↓déficit 1,5% → ↓G 2,3% → ↓becas", "↑CxC por fraccionamiento"],
], [0.55, 1.0, 3.0, 1.9])
SRC("Elaborado a partir de las cadenas 7 a 13 de esta sección; BCRP, RI setiembre 2026; BCRPData.")
SUB("2.2 Fórmulas macroeconómicas explícitas – marco peruano")
CAP("Tabla 4. Fórmulas Macroeconómicas Aplicadas al Entorno Peruano")
APA(["Fórmula", "Cálculo con cifras", "Lectura para UCSUR"], [
    ["PBI = C + I + G + (X − M)", "3,20% = 2,36 + 2,87 + 0,06 + 0,70 + 0,45 + 0,03 − 3,27", "El consumo (65,6% del PBI) es su mercado"],
    ["M × V = P × Y", "16,7% + %ΔV = 4,5% + 3,2% → %ΔV = −9,0%", "Liquidez que hoy paga pensiones"],
    ["Fisher: r = i − πᵉ", "1,20% ex ante; −1,00% ex post", "Riesgo de alza de tasas"],
    ["Cierre de inflación", "1,042 / 1,0488 − 1 = −0,65% requerido", "Inflación 2026 sobre 5%"],
    ["Salario real: w/P", "1,0035 / 1,0455 − 1 = −4,0%", "Menor capacidad de pago"],
], [1.8, 2.75, 1.9])
SRC("BCRP, RI setiembre 2026; BCRPData.")
SUB("2.3 Análisis causa-efecto: diagrama de Ishikawa")
T("El diagrama de Ishikawa doméstico reúne los seis factores de la economía peruana. Las espinas verdes (PBI y consumo, empleo) sostienen la demanda; las rojas (inflación y dinero, crédito y morosidad) presionan la capacidad de pago; las grises (tasa y política fiscal) definen el costo del financiamiento.")
CAP("Diagrama 2. Ishikawa de Factores Domésticos que Afectan a UCSUR, 2026–2027")
IMG("i2.png")
SRC("BCRP, RI setiembre 2026; BCRPData; UCSUR, EEFF auditados 2025. Diagrama conceptual.")
INT("El diagrama 2 muestra que la espina decisiva para 2026-2027 es la inflación: actúa sobre los ingresos (menor capacidad de pago), los costos (salarios y servicios) y la política monetaria (posible alza que encarece el crédito educativo).")
CRIT("la economía peruana de 2026 le ofrece a UCSUR más empleo, más liquidez y más crédito, pero menos ingreso real. El desempleo de Lima bajó a 4,4%, la liquidez en soles crece 16,7% y el crédito de consumo 13,2%, mientras el ingreso promedio real cae 4,0% y la inflación llega a 5,25%. La teoría cuantitativa lo explica: con una velocidad que cae 9,0%, hay saldos acumulados que hoy pagan pensiones pero que mañana pueden traducirse en inflación y en un alza de tasas, porque la tasa real ex post ya es −1,00%. El crecimiento es de demanda interna (5,23 pp de consumo e inversión), pero la oferta se contrajo por el petróleo y El Niño, y el modelo OA-DA muestra el resultado: más precios con el mismo producto. Para una universidad que vende a la clase media de Lima Sur, esa combinación es especialmente peligrosa, porque la matrícula se sostiene por el empleo mientras la capacidad de pago se erosiona por la inflación. La política fiscal no compensa: el consumo público se desacelera de 3,2% a 2,3% y limita las becas justo cuando más familias las necesitan.")
ESTR("UCSUR debe aprovechar la ventana de liquidez y crédito barato de 2026 antes de que el ciclo monetario se endurezca. Con la liquidez creciendo 16,7% y el crédito de consumo 13,2%, los bancos y cajas tienen fondos para ofrecer crédito educativo a las familias de Lima Sur; la universidad debe asociarse con ellos para que el financiamiento de la matrícula salga de su balance. Al mismo tiempo, debe preparar su política de precios para un escenario de alza de tasas en 2027: con la tasa real ex post en −1,00% y expectativas de 3,05%, el BCRP tiene razones para subir 25 pb, lo que encarecería el crédito de sus estudiantes. Frente a un ingreso real que cae 4,0%, conviene diferenciar los reajustes: moderados para alumnos de ciclos avanzados, que ya cubrieron el costo de captación, y alineados con la inflación esperada para ingresantes. Y debe planificar 2027 con un consumo privado de 3,0% y un PBI de 3,0%, no con el ritmo de 2025, reservando parte de la caja operativa como colchón frente a una mayor morosidad y vigilando cada mes la inflación de servicios.")

# ================= SECCIÓN 2 =================
doc.add_page_break()
H1("SECCIÓN 2"); MARK("s2desc")
H2("Descripción de la empresa enfatizando los temas relativos a su dependencia del marco macroeconómico en el cual se desenvuelve la empresa")
SUB("Ficha institucional y posición competitiva")
T("Universidad Científica del Sur S.A.C. (UCSUR) es una universidad privada constituida como sociedad anónima cerrada, con fines de lucro, que ofrece carreras de pregrado y programas de posgrado con énfasis en ciencias de la salud, ciencias ambientales y veterinaria. Su mercado núcleo son estudiantes de clase media de Lima Sur y sus familias, que financian las pensiones con su salario, con crédito o con becas. En 2024 absorbió a Pacífico Educad S.A.C. y Rondy S.A.C. (EEFF 2025). No tiene un cliente grande: sus ingresos provienen de miles de pensiones, por lo que su riesgo depende del empleo, los salarios y el crédito de los hogares, más que de un sector o de una empresa.")
CAP("Tabla 5. Ficha Institucional de Universidad Científica del Sur S.A.C.")
APA(["Concepto", "Detalle"], [
    ["Razón social y RUC", "Universidad Científica del Sur S.A.C. — RUC 20421239275"],
    ["Sector", "Educación superior universitaria privada (servicios)"],
    ["Mercado núcleo", "Estudiantes de clase media de Lima Sur y sus familias"],
    ["Ingresos 2025", "S/594,8 millones (+41,5%)"],
    ["Utilidad de operación 2025", "S/219,5 millones (margen 36,9%)"],
    ["Utilidad neta 2025", "S/141,6 millones"],
    ["Activo total / patrimonio 2025", "S/760,2 millones / S/350,6 millones"],
    ["Obligaciones financieras 2025", "S/172,8 millones (corriente S/25,5 MM; no corriente S/147,2 MM)"],
    ["Pasivos por arrendamiento 2025", "S/102,9 millones"],
    ["Inversión en activos fijos 2025", "S/82,5 millones"],
    ["Dividendos pagados 2025", "S/12,5 millones"],
    ["Auditor 2024-2025", "Tanaka, Valdivia, Arribas & Asociados"],
], [2.3, 4.2])
SRC("UCSUR, Estados financieros auditados 2023, 2024 y 2025.")
INT("La tabla 5 muestra una empresa rentable y en expansión, cuya dependencia macroeconómica es directa: vende un servicio de consumo a hogares, financia parte de esa venta con crédito propio y compra en dólares parte de su inversión.")
CAP("Tabla 6. Estados Financieros Resumidos de UCSUR, 2022–2025 (S/ millones)")
APA(["Indicador", "2022", "2023", "2024", "2025"], [
    ["Ingresos por derechos de enseñanza", "264,1", "321,8", "420,4", "594,8"],
    ["Variación anual (%)", "—", "21,8", "30,7", "41,5"],
    ["Gastos de personal docente y administrativo", "116,8", "152,5", "169,5", "214,7"],
    ["Gastos generales de operación y administración", "78,4", "94,7", "108,8", "128,2"],
    ["Utilidad de operación", "55,0", "50,8", "121,1", "219,5"],
    ["Margen operativo (%)", "20,8", "15,8", "28,8", "36,9"],
    ["Gastos financieros", "16,9", "23,0", "27,2", "27,5"],
    ["Utilidad neta", "25,0", "22,0", "76,5", "141,6"],
    ["Derechos de enseñanza por cobrar, neto", "13,4", "17,7", "20,4", "48,8"],
    ["Cuentas por pagar comerciales", "23,1", "25,9", "24,9", "40,0"],
    ["Obligaciones financieras", "89,0", "113,1", "131,3", "172,8"],
    ["Flujo de efectivo de operación", "61,3", "50,2", "141,7", "230,6"],
], [3.1, 0.85, 0.85, 0.85, 0.85])
SRC("UCSUR, Estados financieros auditados 2023, 2024 y 2025. Las cifras de 2024 de gastos generales, utilidad de operación, gastos financieros y flujo operativo corresponden al comparativo reexpresado del informe 2025.")
CAP("Gráfico 10. Resultados de UCSUR, 2022–2025 (S/ millones y margen operativo)")
IMG("g13.png")
SRC("UCSUR, Estados financieros auditados 2023, 2024 y 2025.")
INT("El gráfico 10 muestra que el margen operativo cayó en 2023 (15,8%), cuando el PBI se contrajo y la inflación promedio fue 6,3%, y luego subió hasta 36,9%. Los costos de UCSUR son en gran parte fijos (planilla, depreciación y arrendamientos), por lo que una caída de matrícula reduciría la utilidad más que proporcionalmente.")
SUB("Dependencia de UCSUR respecto a las 4 variables macroeconómicas clave")
T("Las cuatro variables de orientación llegan a UCSUR por canales distintos. El PBI, y dentro de él el consumo privado, determina cuántas familias pueden pagar una universidad privada. La inflación eleva sus costos fijos y reduce el poder de compra de sus clientes. La tasa de interés define el costo del crédito con que las familias pagan y el de la propia deuda de la universidad. El tipo de cambio afecta el costo de su equipamiento importado. La tabla 7 resume su trayectoria.")
CAP("Tabla 7. Variables Macroeconómicas Clave y su Impacto en UCSUR, 2023–2027P")
APA(["Variable", "2023", "2024", "2025", "2026P", "2027P", "Impacto en UCSUR"], [
    ["PBI (var. %)", "−0,4", "3,5", "3,4", "3,2", "3,0", "↑ Matrícula"],
    ["Consumo privado (var. %)", "0,1", "2,8", "3,6", "3,6", "3,0", "↑ Ventas"],
    ["Inflación fin de periodo (%)", "3,2", "2,0", "1,5", "5,25*", "2,0", "↑ Costos; ↓ poder de compra"],
    ["Tasa de referencia (%)", "6,75", "5,00", "4,25", "4,25*", "n. d.", "Costo de deuda y crédito"],
    ["Tipo de cambio dic. (S/ por US$)", "3,734", "3,735", "3,367", "3,412*", "3,40–3,50", "Costo del equipamiento"],
], [1.7, 0.5, 0.5, 0.5, 0.6, 0.75, 1.95])
SRC("BCRPData (PBI y consumo por tipo de gasto, IPC de Lima, tasa de referencia y tipo de cambio promedio de diciembre); BCRP, RI setiembre 2026 (proyecciones). * Último dato observado: inflación de octubre, tasa a noviembre y tipo de cambio del 9 de noviembre de 2026. Rango cambiario 2027P: estimación del grupo.")
INT("La tabla 7 muestra que 2026 combina el mayor crecimiento de la demanda interna del ciclo con la inflación más alta desde 2023, lo que explica el sesgo de tasas al alza y la presión sobre el poder de compra de las familias.")

SUB("Variable 1. PBI y consumo privado: el motor de las ventas de UCSUR")
T("La elasticidad ingreso de la demanda mide cuánto cambian las ventas cuando cambia el ingreso de los consumidores. Para UCSUR se calculó con sus ingresos reales, deflactados por la inflación promedio de Lima, frente al consumo privado real:")
EQ("ε = %Δ Ingresos reales de UCSUR / %Δ Consumo privado real")
EQ("2024: ε = 27,66% / 2,77% = 9,99        2025: ε = 39,39% / 3,63% = 10,85        Promedio = 10,42")
T("Una elasticidad de 10,4 no describe solo la respuesta de las familias a su ingreso: en 2023 los ingresos reales de UCSUR subieron 14,7% con un PBI que cayó 0,35%, lo que prueba que buena parte del crecimiento proviene de ganar participación y abrir carreras. Para proyectar, se usan tres escenarios: un techo con la elasticidad aparente (10,4), una base que supone que la mitad de esa elasticidad se mantiene (5,2) y un escenario prudente sin ganancias de participación (2,0); estas dos últimas son supuestos del grupo. Con el consumo privado del RI (3,6% en 2026 y 3,0% en 2027) y la inflación de 5,25% en 2026 y 2,0% en 2027:")
EQ("Ventas(t) = Ventas(t−1) × (1 + ε × %ΔC) × (1 + π)   →   Base 2026: 594,8 × (1 + 5,2 × 3,6%) × 1,0525 = S/743,3 MM")
CAP("Tabla 8. Proyección de Ingresos de UCSUR según el Consumo Privado, 2026P–2028P (S/ millones)")
APA(["Escenario", "Elasticidad", "2025", "2026P", "2027P", "2028P"], [
    ["Techo (elasticidad aparente)", "10,4", "594,8", "860,5", "1.151,5", "1.541,0"],
    ["Base (supuesto del grupo)", "5,2", "594,8", "743,3", "876,4", "1.033,4"],
    ["Prudente (supuesto del grupo)", "2,0", "594,8", "671,1", "725,6", "784,6"],
    ["Consumo privado (var. %)", "—", "3,6", "3,6", "3,0", "3,0"],
    ["Inflación (%)", "—", "1,5", "5,25", "2,0", "2,0"],
], [2.3, 0.9, 0.8, 0.8, 0.8, 0.9])
SRC("UCSUR, EEFF auditados 2025; BCRP, RI setiembre 2026 (consumo 2026P-2027P, inflación 2027P); BCRPData (inflación 2026). Consumo e inflación de 2028P: supuestos del grupo (consumo igual a 2027 e inflación en el centro del rango meta).")
CAP("Gráfico 11. Ingresos de UCSUR por Escenario y Crecimiento del PBI, 2022–2028P")
IMG("g14.png")
SRC("UCSUR, EEFF auditados 2022-2025; BCRPData; BCRP, RI setiembre 2026. Proyecciones según la tabla 8.")
INT("El gráfico 11 muestra que el escenario base (S/743,3 millones en 2026 y S/876,4 millones en 2027) supone que UCSUR sigue creciendo por encima de su mercado, pero a la mitad del ritmo reciente. La sensibilidad es alta: en el escenario base, cada punto menos de consumo privado resta 5,2 pp de crecimiento real, unos S/31 millones sobre la base de 2025.")

SUB("Variable 2. Inflación: presión sobre costos fijos y poder de compra")
T("La inflación afecta a UCSUR por dos lados. Por el de los costos, su planilla docente y administrativa (S/214,7 millones) y sus gastos generales (S/128,2 millones) suman S/342,8 millones, 57,6% de los ingresos; con una inflación de 5,25%, el solo efecto precio los elevaría en S/18,0 millones, 8,2% de la utilidad de operación de 2025. Por el de los ingresos, una pensión que sube con la inflación choca con un ingreso real que cae 4,0%, de modo que la universidad no puede trasladar toda la inflación a precios sin perder alumnos. La inflación también cambia el valor real de sus saldos: las cuentas por cobrar (S/48,8 millones) pierden S/2,6 millones de poder de compra al año y las cuentas por pagar (S/40,0 millones) alivian S/2,1 millones.")
CAP("Tabla 9. Efecto de la Inflación sobre los Costos de UCSUR, 2025–2027P (S/ millones)")
APA(["Concepto", "2025", "2026P", "2027P"], [
    ["Inflación aplicada (%)", "1,5", "5,25", "2,0"],
    ["Gastos de personal (efecto precio)", "214,7", "225,9", "230,4"],
    ["Gastos generales (efecto precio)", "128,2", "134,9", "137,6"],
    ["Aumento de costos por inflación", "—", "18,0", "7,2"],
    ["Pérdida real de CxC (π × S/48,8 MM)", "0,7", "2,6", "1,0"],
    ["Alivio real de CxP (π × S/40,0 MM)", "0,6", "2,1", "0,8"],
], [3.2, 1.0, 1.0, 1.0])
SRC("UCSUR, EEFF auditados 2025; BCRPData (inflación 2025 y octubre 2026); BCRP, RI setiembre 2026 (inflación 2027P). Proyección: costos de 2025 ajustados solo por inflación, sin cambios de plantilla.")
CAP("Modelo 5. Isocuanta del Servicio Educativo: Docentes y Capital Académico ante la Inflación")
IMG("m4.png", 5.6)
SRC("UCSUR, EEFF auditados 2025 (gastos de personal y capex); BCRPData. Diagrama conceptual.")
INT("El modelo 5 muestra la isocuanta Q₀ del servicio educativo con dos insumos: horas docentes (L) y capital académico (K). La inflación de 5,25% eleva el costo de L más que el de K (+5,1% por equipo importado), la recta de isocosto se hace más empinada y el óptimo pasa de A a B: más laboratorios, simulación y plataformas digitales por alumno, y menos horas docentes por estudiante. Es la lógica del capex de S/82,5 millones de 2025.")

SUB("Variable 3. Tipo de cambio Sol/USD: exposición moderada concentrada en el capex")
T("UCSUR factura en soles y su exposición cambiaria en resultados es pequeña, pero creciente: la pérdida por diferencia de cambio pasó de S/0,1 millones en 2023 a S/0,4 millones en 2024 y S/1,7 millones en 2025, en un año en que el sol se apreció 10,2%, lo que indica pasivos o compromisos en dólares. El riesgo mayor está en la inversión: el equipamiento de laboratorios y simulación y las licencias de software se pagan en dólares. La tabla 10 muestra la sensibilidad del costo de un equipo de US$1 millón y de un capex de S/80 millones a distintos tipos de cambio.")
CAP("Tabla 10. Escenarios de Tipo de Cambio y Costo del Equipamiento Importado de UCSUR")
APA(["Escenario", "Tipo de cambio", "Costo de US$1 MM (S/ MM)", "Variación vs. dic-25", "Sobrecosto en capex de S/80 MM"], [
    ["Diciembre 2025", "3,367", "3,367", "—", "—"],
    ["Base (9-nov-26)", "3,412", "3,538", "+5,1%", "S/4,1 MM"],
    ["Depreciación moderada", "3,50", "3,630", "+7,8%", "S/6,2 MM"],
    ["Depreciación fuerte", "3,60", "3,733", "+10,9%", "S/8,7 MM"],
], [1.6, 1.0, 1.4, 1.1, 1.4])
SRC("BCRPData (tipo de cambio); inflación PCE 2026 de 3,7% (Fed, citada en BCRP, RI setiembre 2026). Capex de S/80 MM: supuesto del grupo, cercano a las compras de activos fijos de 2025.")
INT("La tabla 10 muestra que, aun con un sol estable, el equipamiento ya cuesta 5,1% más que en diciembre de 2025. Un tipo de cambio de S/3,60 elevaría el sobrecosto a S/8,7 millones si todo el capex fuera importado.")

SUB("Variable 4. Tasa de referencia BCRP: costo de la deuda y del crédito de las familias")
T("La tasa de referencia bajó de 7,50% en diciembre de 2022 a 4,25% en 2025 y se mantiene en ese nivel. En ese periodo, UCSUR casi duplicó sus obligaciones financieras, de S/89,0 a S/172,8 millones, mientras sus gastos financieros subieron de S/16,9 a S/27,5 millones; de estos, S/12,0 millones son intereses de arrendamientos. Excluyendo esos intereses, el costo implícito de su deuda financiera fue 10,2% en 2025, muy por encima de la tasa de referencia, por el diferencial que cobran los bancos. Cada 25 pb de alza aplicados a toda la deuda cuestan S/0,43 millones al año.")
CAP("Tabla 11. Tasa de Referencia y Métricas Financieras de UCSUR, 2022–2025")
APA(["Indicador", "2022", "2023", "2024", "2025"], [
    ["Tasa de referencia BCRP, diciembre (%)", "7,50", "6,75", "5,00", "4,25"],
    ["Obligaciones financieras (S/ MM)", "89,0", "113,1", "131,3", "172,8"],
    ["Pasivos por arrendamiento (S/ MM)", "98,4", "90,0", "142,6", "102,9"],
    ["Gastos financieros (S/ MM)", "16,9", "23,0", "27,2", "27,5"],
    ["Ingresos financieros (S/ MM)", "1,3", "8,8", "10,1", "10,1"],
    ["Efectivo y equivalentes (S/ MM)", "6,1", "9,8", "75,4", "139,4"],
], [3.0, 0.85, 0.85, 0.85, 0.85])
SRC("BCRPData (tasa de referencia); UCSUR, EEFF auditados 2023, 2024 y 2025.")
CAP("Gráfico 12. Gastos Financieros, Diferencia de Cambio y Deuda Financiera de UCSUR, 2022–2025 (S/ millones)")
IMG("g10.png")
SRC("UCSUR, Estados financieros auditados 2023, 2024 y 2025.")
INT("El gráfico 12 muestra que la deuda casi se duplicó, pero los gastos financieros se estabilizaron en S/27,5 millones gracias a la baja de tasas y a una caja de S/139,4 millones. La sensibilidad de UCSUR a la tasa es moderada en intereses, pero alta en la cobranza, porque sus estudiantes pagan con crédito.")

SUB("Herramientas de análisis macroeconómico aplicadas a la dependencia institucional de UCSUR")
SUB("3.1 Cadenas de razonamiento")
CAP("Tabla 12. Cadenas de las 4 Variables Clave sobre UCSUR")
APA(["Variable", "Notación con cifras", "Efecto en UCSUR"], [
    ["PBI y consumo", "↑C 3,6% → ↑Y 3,2% → ↑demanda de educación (ε base 5,2) → ↑ventas S/743,3 MM", "Ventas 2026P"],
    ["Inflación", "↑P 5,25% → ↑w → ↑costos S/18,0 MM → ↓margen; ↓w/P −4,0% → ↑CxC", "Margen y cobranza"],
    ["Tipo de cambio", "↑i* → ↑E S/3,412 → ↑P*×E +5,1% → ↑capex S/4,1 MM", "Inversión"],
    ["Tasa de interés", "↑P → ↓r −1,00% → ↑i +25 pb → ↑gastos financieros S/0,43 MM", "Costo de deuda"],
], [1.3, 3.6, 1.55])
SRC("Elaborado a partir de las tablas 7 a 11.")
SUB("3.2 Fórmulas explícitas – marco contable y de sensibilidad macro de UCSUR")
CAP("Tabla 13. Fórmulas de Sensibilidad de UCSUR a las Variables Macroeconómicas")
APA(["Fórmula", "Cálculo", "Resultado"], [
    ["ΔVentas = ε × ΔC × Ventas", "5,2 × (−1 pp) × S/594,8 MM", "−S/31 MM por punto de consumo"],
    ["ΔCostos = π × (Personal + Generales)", "5,25% × S/342,8 MM", "+S/18,0 MM en 2026"],
    ["ΔGastos financieros = Δi × Deuda", "0,25% × S/172,8 MM", "+S/0,43 MM por 25 pb"],
    ["ΔCapex = (ΔE / E) × Capex", "(0,10 / 3,41) × S/80 MM", "+S/2,3 MM por 10 céntimos"],
    ["Pérdida real de CxC = π × CxC", "5,25% × S/48,8 MM", "−S/2,6 MM al año"],
    ["Días de cobro = CxC / Ventas × 365", "48,8 / 594,8 × 365", "30 días (18 en 2024)"],
], [2.3, 2.2, 1.95])
SRC("UCSUR, EEFF auditados 2025; BCRP, RI setiembre 2026; BCRPData.")
SUB("3.3 Análisis causa-efecto: diagrama de Ishikawa")
CAP("Diagrama 3. Ishikawa de la Dependencia de UCSUR de las Variables Macroeconómicas")
IMG("i3.png")
SRC("UCSUR, EEFF auditados 2025; BCRP, RI setiembre 2026; BCRPData. Diagrama conceptual.")
INT("El diagrama 3 muestra que la dependencia de UCSUR se concentra en dos espinas: el consumo privado, que define el volumen, y la inflación, que actúa a la vez sobre costos y cobranza. El tipo de cambio y la tasa de interés tienen efectos acotados en los resultados, pero relevantes en la inversión y el crédito de las familias.")

H2("En base al análisis de la sección anterior, analizar el impacto del entorno macroeconómico sobre la empresa en cuestión, enfatizando el impacto en sus ventas, costos, cuentas por cobrar, cuentas por pagar y financiamiento"); MARK("s2imp")

SUB("1. Variaciones del PBI y su efecto sobre las ventas de UCSUR")
T("En 2023 el PBI cayó 0,35% y los ingresos reales de UCSUR subieron 14,7%; en 2024 y 2025 el PBI creció 3,52% y 3,43%, y los ingresos reales 27,7% y 39,4%. La universidad crece por encima de la economía porque gana participación, pero su crecimiento sigue atado al consumo de las familias. Con el escenario base (ε = 5,2), un PBI de 3,2% y un consumo de 3,6% llevarían los ingresos a S/743,3 millones en 2026 y S/876,4 millones en 2027. Si El Niño redujera el consumo a 3,0% en 2026, el crecimiento real caería de 18,7% a 15,6%.")
CAP("Gráfico 13. PBI, Consumo Privado e Ingresos Reales de UCSUR, 2023–2025 (var. % real)")
IMG("g7.png")
SRC("UCSUR, EEFF auditados 2023-2025; BCRPData.")
CADENA("Cadena 14. PBI (Y) y Consumo (C) → Ventas de UCSUR",
       [("↑Y", "3,2% (2026P)"), ("↑C", "3,6% (2026P)"), ("↑Demanda de educación", "ε base = 5,2"), ("↑Ventas", "S/743,3 MM (2026P)"), ("↓C 2027", "3,0%"), ("↓Crecimiento", "15,6% real (2027P)")],
       "Si crecen el PBI y el consumo → sube la demanda de educación superior → suben las ventas de UCSUR; si el consumo se desacelera en 2027 → el crecimiento real de las ventas baja de 18,7% a 15,6%.")

SUB("2. Tasa de interés y su efecto sobre las cuentas por cobrar (CxC)")
T("Las cuentas por cobrar de UCSUR crecieron 139% en 2025, hasta S/48,8 millones, y el plazo de cobro subió de 18 a 30 días, en un año en que la tasa de referencia bajó a 4,25%. El fraccionamiento de pensiones funciona como un crédito sin interés explícito: cuando las tasas del sistema son bajas, las familias prefieren pagar a plazos a la universidad; cuando suben, el fraccionamiento se vuelve aún más atractivo frente al crédito bancario y las cuentas por cobrar tienden a crecer. Con un costo implícito de deuda de 10,2%, financiar S/48,8 millones de cuentas por cobrar le cuesta a UCSUR unos S/5,0 millones al año en costo de oportunidad.")
CADENA("Cadena 15. Tasa de Interés (i) → Crédito de las Familias → CxC de UCSUR",
       [("↑i BCRP", "4,25% → 4,50% (escenario)"), ("↑Tasa de consumo", "Crédito bancario más caro"), ("↑Fraccionamiento", "Pago a plazos"), ("↑CxC", "S/48,8 MM; 30 días"), ("↑Costo de oportunidad", "10,2% × CxC = S/5,0 MM"), ("↑Provisiones", "S/6,5 MM (2025)")],
       "Si sube la tasa de interés → se encarece el crédito de consumo → más familias fraccionan la pensión → crecen las cuentas por cobrar y su costo de financiamiento → suben las provisiones de UCSUR.")

SUB("3. Tasa de interés: efecto sobre cuentas por pagar y gastos financieros")
T("UCSUR tiene obligaciones financieras por S/172,8 millones (S/147,2 millones a largo plazo) y pasivos por arrendamiento por S/102,9 millones. Sus gastos financieros fueron S/27,5 millones en 2025, casi iguales a los de 2024 pese a una deuda 31,6% mayor, gracias a la baja de la tasa de referencia y a ingresos financieros de S/10,1 millones por su caja de S/139,4 millones. Un alza de 25 pb aplicada a toda la deuda costaría S/0,43 millones al año, y una de 50 pb, S/0,86 millones. Las cuentas por pagar comerciales (S/40,0 millones) son financiamiento sin costo: con tasas más altas, alargar su plazo libera caja.")
CADENA("Cadena 16. Tasa de Interés (i) → Gastos Financieros y CxP de UCSUR",
       [("↑P", "π 5,25%"), ("↓r", "Ex post −1,00%"), ("↑i", "+25 pb (escenario)"), ("↑Gastos financieros", "+S/0,43 MM al año"), ("↑Valor de CxP", "S/40,0 MM sin costo"), ("↓Utilidad neta", "S/141,6 MM (2025)")],
       "Si la inflación lleva al BCRP a subir la tasa → suben los gastos financieros de la deuda de S/172,8 millones → gana valor el crédito de proveedores → se reduce levemente la utilidad neta de UCSUR.")

SUB("4. Inflación y su repercusión sobre los costos operativos")
T("Con una inflación de 5,25%, el efecto precio sobre la planilla (S/214,7 millones) y los gastos generales (S/128,2 millones) suma S/18,0 millones, 8,2% de la utilidad de operación. La planilla se reajusta con rezago, de modo que la inflación de 2026 pesará en los costos de 2027, cuando la inflación proyectada vuelve a 2,0% y las pensiones no podrán subir al mismo ritmo. La energía, en cambio, sube de inmediato con el petróleo. El margen operativo de 2023 (15,8%), con inflación promedio de 6,3%, muestra lo que ocurre cuando los costos suben más rápido que las pensiones.")
CADENA("Cadena 17. Inflación (P) → Salarios (w) → Costos Operativos de UCSUR",
       [("↑P", "π 5,25%"), ("↑w", "Reajustes 2027"), ("↑Personal", "S/214,7 → S/225,9 MM"), ("↑Generales", "S/128,2 → S/134,9 MM"), ("↑Costos", "+S/18,0 MM"), ("↓Margen operativo", "36,9% → ~33,9%")],
       "Si sube la inflación → suben los salarios y los servicios → suben los costos operativos en S/18,0 millones → si las pensiones no suben al mismo ritmo, el margen operativo bajaría unos 3 pp.")

SUB("5. Inflación y su repercusión sobre CxC y CxP")
T("La inflación redistribuye valor entre UCSUR, sus estudiantes y sus proveedores. Con 5,25%, las cuentas por cobrar de S/48,8 millones pierden S/2,6 millones de poder de compra al año, porque se cobran en soles nominales; las cuentas por pagar comerciales de S/40,0 millones alivian S/2,1 millones, porque se pagan con soles depreciados. El efecto neto es negativo (−S/0,5 millones) y crece con el plazo de cobro: si las cuentas por cobrar siguieran creciendo más rápido que las ventas, la pérdida real aumentaría. Los proveedores también trasladan inflación: las cuentas por pagar comerciales subieron 60,4% en 2025.")
CADENA("Cadena 18. Inflación (P) → Valor Real de CxC y CxP → Capital de Trabajo",
       [("↑P", "π 5,25%"), ("↓Valor real CxC", "−S/2,6 MM"), ("↓Valor real CxP", "+S/2,1 MM"), ("Efecto neto", "−S/0,5 MM"), ("↑Días de cobro", "18 → 30 días"), ("↑Necesidad de caja", "Capital de trabajo")],
       "Si sube la inflación → pierden valor real las cuentas por cobrar más de lo que se alivian las cuentas por pagar → con más días de cobro, aumenta la necesidad de capital de trabajo de UCSUR.")

SUB("6. Tipo de cambio y sus implicancias en operaciones y balance")
T("El tipo de cambio no afecta las ventas de UCSUR, que se cobran en soles, pero sí su inversión y algunos pasivos. La pérdida por diferencia de cambio subió a S/1,7 millones en 2025 y el equipamiento importado ya cuesta 5,1% más que en diciembre de 2025. Con un sol entre S/3,40 y S/3,50, el riesgo es moderado; una depreciación a S/3,60 elevaría el sobrecosto del capex a S/8,7 millones si fuera íntegramente importado.")
CADENA("Cadena 19. Tipo de Cambio (E) → Costo Importado → Balance de UCSUR",
       [("↑i*", "Fed 3,75%–4,00%"), ("↑E", "S/3,412 → S/3,60"), ("↑P* × E", "+10,9%"), ("↑Capex", "+S/8,7 MM"), ("↑Pérdida cambiaria", "−S/1,7 MM (2025)"), ("↓Flujo libre", "Tras capex")],
       "Si sube el tipo de cambio → sube el costo en soles del equipamiento y de los pasivos en dólares → aumenta el capex y la pérdida cambiaria → se reduce el flujo libre de UCSUR.")

SUB("7. Consumo, empleo y poder adquisitivo: efecto sobre la demanda")
T("El desempleo de Lima bajó a 4,4% y el juvenil a 11,3%, pero el ingreso promedio real cayó 4,0%. Para UCSUR, más empleo significa más familias que pueden matricular a un hijo; menos ingreso real significa que esas familias pagan con más dificultad. La señal ya está en su balance: los castigos de pensiones incobrables subieron 84%, de S/2,0 a S/3,7 millones, y la estimación para pérdidas crediticias 23,3%, de S/5,3 a S/6,5 millones.")
CADENA("Cadena 20. Empleo (N) y Poder Adquisitivo (w/P) → Demanda y Cobranza de UCSUR",
       [("↓u", "Lima 4,4%; jóvenes 11,3%"), ("↑N", "+242 mil formales"), ("↓w/P", "−4,0% real"), ("↓Capacidad de pago", "Familias de Lima Sur"), ("↑Castigos", "+84% (S/3,7 MM)"), ("↑Riesgo de deserción", "CxC S/48,8 MM")],
       "Si baja el desempleo pero cae el salario real → más familias matriculan, pero con menor capacidad de pago → suben los castigos y el riesgo de deserción en UCSUR.")

SUB("8. PBI de los clientes de UCSUR (familias de Lima Sur) y efecto indirecto")
T("UCSUR no tiene un cliente grande: sus clientes son hogares de clase media de Lima Sur, cuyo «PBI» es su ingreso laboral. Ese ingreso depende de sectores urbanos como comercio (+5,9% en 2026), servicios (+4,3%) y construcción (+9,5%), que crecen más que el PBI total (3,2%), y no de la minería o la pesca, que caen por El Niño. Por eso el efecto indirecto de la macroeconomía sobre UCSUR es más favorable que el del PBI agregado en volumen, pero más desfavorable en precios, porque la inflación golpea sobre todo a hogares urbanos que gastan en transporte y servicios.")
CADENA("Cadena 21. PBI Sectorial Urbano → Ingreso de las Familias de Lima Sur → Matrícula de UCSUR",
       [("↑Y no primario", "Comercio 5,9%; servicios 4,3%"), ("↑Construcción", "+9,5%"), ("↑Empleo urbano", "Lima 4,4% de desempleo"), ("↑Ingreso familiar", "Nominal +0,35%"), ("↓Ingreso real", "−4,0%"), ("Matrícula estable", "Precio limitado")],
       "Si crecen los sectores urbanos → sube el empleo de las familias de Lima Sur → se sostiene la matrícula; pero como el ingreso real cae → UCSUR tiene poco espacio para subir pensiones.")

SUB("9. Liquidez del sistema financiero, crédito y riesgo de morosidad")
T("La liquidez en soles crece 16,7% y el crédito de consumo 13,2%, sostenidos por una tasa real negativa. Ese entorno favorece la matrícula financiada, pero UCSUR no lo aprovecha: sus cuentas por cobrar crecieron 139% y su plazo de cobro subió a 30 días, lo que significa que financia a sus estudiantes con capital propio. Si el BCRP sube la tasa para corregir la inflación, el crédito se desacelerará y la morosidad de las familias subirá, justo cuando las provisiones de UCSUR ya llegaron a S/7,3 millones.")
CAP("Gráfico 14. Crédito de Consumo y Cobranza de UCSUR")
IMG("g12.png")
SRC("BCRPData, serie PN00537MM; UCSUR, EEFF auditados 2023-2025.")
CADENA("Cadena 22. Liquidez (M) → Crédito → Morosidad → CxC de UCSUR",
       [("↑M", "Liquidez +16,7%"), ("↑Crédito de consumo", "+13,2% (set-26)"), ("↑Matrícula", "Ingresos +41,5%"), ("↑i (escenario)", "Alza de 25 pb"), ("↑Morosidad", "Provisiones S/7,3 MM"), ("↑CxC UCSUR", "S/48,8 MM; 30 días")],
       "Si sube la liquidez → crece el crédito de consumo → más familias financian la matrícula; pero si sube la tasa → se encarece ese crédito → sube la morosidad → crecen las cuentas por cobrar y las provisiones de UCSUR.")

SUB("Herramientas de análisis macroeconómico aplicadas al impacto proyectado 2026-2028")
SUB("4.1 Cadenas de razonamiento")
CAP("Tabla 14. Cadenas de Impacto sobre UCSUR, 2026–2028")
APA(["Canal", "Notación con cifras", "Partida afectada"], [
    ["PBI → ventas", "↑Y 3,2% → ↑C 3,6% → ↑ventas S/743,3 MM", "Ingresos"],
    ["Tasa → CxC", "↑i → ↑fraccionamiento → ↑CxC S/48,8 MM", "Cuentas por cobrar"],
    ["Tasa → CxP y gastos financieros", "↑i +25 pb → ↑GF S/0,43 MM", "Gastos financieros"],
    ["Inflación → costos", "↑P 5,25% → ↑costos S/18,0 MM → ↓margen ~3 pp", "Costos operativos"],
    ["Inflación → CxC y CxP", "↑P → CxC −S/2,6 MM; CxP +S/2,1 MM", "Capital de trabajo"],
    ["Tipo de cambio", "↑E S/3,60 → ↑capex S/8,7 MM", "Inversión"],
    ["Empleo → demanda", "↓u 4,4% → ↓w/P −4,0% → ↑castigos 84%", "Cobranza"],
    ["Clientes → matrícula", "↑Y urbano → ↑empleo → precio limitado", "Ingresos"],
    ["Liquidez → morosidad", "↑M 16,7% → ↑crédito 13,2% → ↑i → ↑morosidad", "Provisiones"],
], [1.7, 3.2, 1.55])
SRC("Elaborado a partir de las cadenas 14 a 22.")
SUB("4.2 Fórmulas de sensibilidad – proyección 2026-2028")
CAP("Tabla 15. Sensibilidad de UCSUR a las Variables Macroeconómicas, 2026P–2028P (S/ millones)")
APA(["Fórmula (escenario base)", "2026P", "2027P", "2028P"], [
    ["Ventas = V(t−1) × (1 + 5,2 × %ΔC) × (1 + π)", "743,3", "876,4", "1.033,4"],
    ["ΔVentas por −1 pp de consumo = 5,2% × V(t−1)", "−30,9", "−38,7", "−45,6"],
    ["ΔCostos por inflación = π × costos(t−1)", "+18,0", "+7,2", "+7,4"],
    ["ΔGastos financieros por +25 pb = 0,25% × S/172,8 MM", "+0,43", "+0,43", "+0,43"],
    ["Pérdida real de CxC = π × S/48,8 MM", "−2,6", "−1,0", "−1,0"],
    ["ΔCapex por +10 céntimos de TC = (0,10 / 3,41) × S/80 MM", "+2,3", "+2,3", "+2,3"],
], [3.5, 0.95, 0.95, 0.95])
SRC("UCSUR, EEFF auditados 2025; BCRP, RI setiembre 2026. Supuestos del grupo para 2028P: consumo privado 3,0% e inflación 2,0%; deuda, CxC y capex constantes.")
SUB("4.3 Análisis causa-efecto: diagrama de Ishikawa")
CAP("Diagrama 4. Ishikawa del Impacto Macroeconómico sobre UCSUR, 2026–2028")
IMG("i4.png")
SRC("UCSUR, EEFF auditados 2025; BCRP, RI setiembre 2026; BCRPData. Diagrama conceptual.")
INT("El diagrama 4 muestra que el impacto proyectado se concentra en ventas (consumo) y costos (inflación); las cuentas por cobrar son el canal por el que la tasa de interés y el empleo llegan a los resultados.")
CRIT("los nueve canales muestran que el impacto macroeconómico sobre UCSUR se concentra en dos variables: el consumo privado y la inflación. El consumo es favorable en el escenario base: con una elasticidad de 5,2, las ventas crecerían a S/743,3 millones en 2026 y S/876,4 millones en 2027, aunque la sensibilidad es alta, porque cada punto menos de consumo resta unos S/31 millones. La inflación es el riesgo central: suma S/18,0 millones a los costos en 2026, resta S/2,6 millones al valor real de las cuentas por cobrar y reduce 4,0% el ingreso real de las familias. La tasa de interés y el tipo de cambio tienen efectos acotados en resultados (S/0,43 millones por 25 pb y S/2,3 millones por 10 céntimos), pero no son menores en el balance: la deuda de S/172,8 millones y un capex del orden de S/80 millones amplifican cualquier cambio. La señal más preocupante no es macroeconómica sino de gestión: las cuentas por cobrar crecieron 139%, más de tres veces que las ventas, y los castigos 84%. Si el ciclo de tasas se revierte, esa cartera se convertirá en morosidad y presionará las provisiones, que ya suman S/7,3 millones.")
ESTR("UCSUR debe gestionar cada variable con un instrumento distinto. Para el consumo, debe sostener el volumen sin forzar precios: reajustar pensiones con la inflación esperada (3,05%) y no con la observada (5,25%), sobre todo para alumnos de ciclos avanzados, porque perder un punto de crecimiento por deserción cuesta más que los 2,2 pp de reajuste no aplicado. Para la inflación, debe indexar a precios fijos sus contratos de energía y servicios y negociar reajustes salariales escalonados para 2027, cuando la inflación vuelve a 2,0%. Para la tasa de interés, debe fijar el costo de su deuda de S/172,8 millones mientras la tasa real ex post sea negativa y trasladar el fraccionamiento a convenios de crédito educativo con bancos y cajas, para bajar la cobranza de 30 a 20 días y liberar unos S/16 millones. Para el tipo de cambio, debe cubrir con forwards la mitad del capex importado de 2027. Con estas medidas, el margen operativo podría mantenerse por encima de 33% aun en el escenario de inflación de 5,25% y alza de tasas, y la caja operativa de S/230,6 millones seguiría financiando el crecimiento sin nueva deuda.")

# ================= SECCIÓN 3 =================
doc.add_page_break()
H1("SECCIÓN 3"); MARK("s3")
H2("Recomendaciones, Sugerencias y Comentarios")
SUB("1. Recomendaciones Estratégicas Macroeconómicas")
SUB("1.1 Política de pensiones frente a la inflación y el poder adquisitivo")
P("Recomendación R1. Reajustar las pensiones con la inflación esperada y no con la observada.", bold=True)
T("Variable y hallazgo: inflación y poder adquisitivo; la inflación de Lima llegó a 5,25% mientras el ingreso real de las familias cae 4,0% y la elasticidad aparente de las ventas es 10,4 (cadenas 8, 17 y 20). UCSUR debería limitar el reajuste de pensiones de 2027 a la inflación esperada (3,05%) y aplicarlo sobre todo a ingresantes, manteniendo las pensiones de los ciclos avanzados. Meta: retención igual o mayor a la de 2025 y crecimiento real de ingresos dentro del escenario base (15,6% en 2027).")
SUB("1.2 Estructura de la deuda frente al ciclo de tasas")
P("Recomendación R2. Fijar la tasa de la deuda antes de un alza del BCRP.", bold=True)
T("Variable y hallazgo: tasa de interés; la tasa real ex post es −1,00% y las expectativas de inflación (3,05%) superan el rango meta, lo que anticipa un alza (cadenas 12 y 16). UCSUR debería refinanciar o cubrir con swaps la porción variable de sus S/172,8 millones de deuda, aun pagando una prima de alrededor de 0,30 pp. Meta: costo financiero fijo para 2026-2028 y gastos financieros estables en torno a S/27,5 millones.")
SUB("1.3 Financiamiento de la matrícula y cobranza")
P("Recomendación R3. Trasladar el fraccionamiento de pensiones a convenios de crédito educativo.", bold=True)
T("Variable y hallazgo: liquidez y crédito; la liquidez en soles crece 16,7% y el crédito de consumo 13,2%, mientras las cuentas por cobrar de UCSUR crecieron 139% y el plazo de cobro llegó a 30 días (cadenas 11, 15 y 22). UCSUR debería firmar convenios con bancos y cajas para que las familias financien la matrícula con crédito educativo a tasa fija, con la universidad como originadora y no como prestamista. Meta: bajar la cobranza a 20 días y liberar unos S/16 millones de capital de trabajo.")
SUB("1.4 Cobertura cambiaria de la inversión académica")
P("Recomendación R4. Cubrir con forwards la mitad del capex importado.", bold=True)
T("Variable y hallazgo: tipo de cambio; con un diferencial de tasas de 0,375 pp y la Fed en 3,75%–4,00%, el riesgo de depreciación existe aunque el sol esté estable; el equipamiento ya cuesta 5,1% más que en diciembre de 2025 (cadenas 4, 6 y 19). UCSUR debería comprar forwards para la mitad de sus compras de equipamiento de 2027 cuando el tipo de cambio esté por debajo de S/3,45 y programar las compras en tramos trimestrales. Meta: costo del capex importado con una variación cambiaria máxima de 2%.")
CAP("Tabla 16. Análisis Costo-Beneficio de las Recomendaciones (S/ millones, horizonte 2026–2027)")
APA(["Recomendación", "Costo estimado", "Beneficio estimado", "Relación B/C"], [
    ["R1. Pensiones con inflación esperada", "13,1 (2,2 pp de reajuste no aplicado sobre S/594,8 MM)", "22,3 (evitar la pérdida de 3% de la matrícula en el escenario base 2026)", "1,7"],
    ["R2. Fijar la tasa de la deuda", "1,0 (prima de 0,30 pp × S/172,8 MM × 2 años)", "1,7 (alza evitada de 50 pb × S/172,8 MM × 2 años)", "1,7"],
    ["R3. Convenios de crédito educativo", "2,0 (comisiones y gestión, 2 años)", "7,2 (capital liberado S/16,3 MM × 10,2% × 2 años + 30% menos provisiones)", "3,6"],
    ["R4. Forwards para el capex", "0,7 (puntos forward de 0,375 pp y spread de 0,5% sobre S/40 MM al año, 2 años)", "4,4 (sobrecosto evitado si el TC llega a S/3,60: 5,5% × S/40 MM × 2 años)", "6,3"],
    ["Total", "16,8", "35,6", "2,1"],
], [1.7, 1.75, 2.25, 0.8])
SRC("Estimaciones del grupo con base en UCSUR, EEFF auditados 2025; BCRP, RI setiembre 2026; BCRPData. Cifras referenciales.")
INT("La tabla 16 indica que todas las recomendaciones tienen una relación beneficio/costo mayor a 1,5. R1 es la de mayor beneficio absoluto porque protege el volumen de matrícula, la variable que más pesa en los resultados; R4 tiene la mayor relación beneficio/costo por su bajo costo, aunque su beneficio solo se materializa si el sol se deprecia, y R3 actúa sobre las cuentas por cobrar, la partida que más se deterioró en 2025.")
SUB("2. Sugerencias Operativas con Base Macroeconómica")
SUB("2.1 Tipo de cambio")
T("SI: el tipo de cambio supera S/3,50 por dólar: postergar las compras de equipamiento no urgentes y ejecutar los forwards contratados. SI: el tipo de cambio cae por debajo de S/3,40: adelantar las compras del semestre siguiente y ampliar la cobertura al 70% del capex importado.")
SUB("2.2 Empleo, ingreso real y matrícula")
T("SI: el desempleo juvenil de Lima supera 13% o el ingreso real cae más de 5%: ampliar los descuentos por pronto pago y las becas internas en los ciclos avanzados, donde la deserción es más costosa. SI: el empleo formal sigue creciendo y el ingreso real se recupera: reforzar la captación de ingresantes en carreras de salud, donde la demanda es menos sensible al precio.")
SUB("2.3 Tasa de interés e inflación")
T("SI: el BCRP sube su tasa a 4,50% o más: activar los convenios de crédito educativo a tasa fija y endurecer el fraccionamiento propio para nuevos alumnos. SI: la inflación supera 5,5%: renegociar contratos de energía y servicios con tope de reajuste y escalonar los reajustes salariales de 2027. SI: la inflación vuelve al rango meta: aplicar el reajuste de pensiones completo a ingresantes.")
SUB("3. Comentarios Finales sobre el Entorno Macroeconómico 2026–2027")
T("El entorno macroeconómico de 2026–2027 es favorable para UCSUR en volumen y exigente en margen y cobranza. Los términos de intercambio récord (+18,1%), una demanda interna que crece 6,2% y un desempleo de 4,4% en Lima sostienen la matrícula de clase media; con una elasticidad base de 5,2, las ventas llegarían a S/743,3 millones en 2026 y S/876,4 millones en 2027. Pero la inflación de oferta (5,25%) reduce 4,0% el ingreso real de las familias y suma S/18,0 millones a los costos, y la tasa real negativa anticipa un alza que encarecería el crédito con que muchas familias pagan.")
T("La universidad depende más del poder adquisitivo de sus clientes que de cualquier variable financiera. Por eso su principal decisión macroeconómica no es de deuda ni de cobertura, sino de precios y de cobranza: reajustar pensiones con la inflación esperada, trasladar el financiamiento de la matrícula al sistema financiero y planificar 2027 con un consumo de 3,0%. Si lo hace, podrá mantener un margen operativo superior a 33% aun en un escenario de inflación persistente y alza de tasas.")

H1("Referencias")
for ref in [
    "Banco Central de Reserva del Perú. (2026a, 18 de setiembre). Reporte de Inflación: Panorama actual y proyecciones macroeconómicas 2026-2027. Setiembre de 2026. https://www.bcrp.gob.pe/publicaciones/reporte-de-inflacion.html",
    "Banco Central de Reserva del Perú. (2026b). BCRPData: Series estadísticas [Base de datos]. Consultado el 11 de noviembre de 2026. https://estadisticas.bcrp.gob.pe",
    "Federal Reserve. (2026). Open market operations: Policy rate changes. https://www.federalreserve.gov/monetarypolicy/openmarket.htm",
    "Universidad Científica del Sur S.A.C. (2024). Estados financieros al 31 de diciembre de 2023 y de 2022, con el informe de los auditores independientes (28 de mayo de 2024). Lima.",
    "Universidad Científica del Sur S.A.C. (2025). Estados financieros al 31 de diciembre de 2024 y de 2023, junto con el dictamen de los auditores independientes. Tanaka, Valdivia, Arribas & Asociados (12 de junio de 2025). Lima.",
    "Universidad Científica del Sur S.A.C. (2026). Estados financieros al 31 de diciembre de 2025 y de 2024, junto con el informe de los auditores independientes. Tanaka, Valdivia, Arribas & Asociados (1 de junio de 2026). Lima.",
]:
    p = P(ref); p.paragraph_format.left_indent = Cm(1.27); p.paragraph_format.first_line_indent = Cm(-1.27)

doc.save(OUT)
print("saved", OUT)

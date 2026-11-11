import os, sys
S = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(S, "lib3.py"), encoding="utf-8").read())
# A4 y márgenes de 2,5 cm
sec = doc.sections[0]; sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"): setattr(sec, m, Cm(2.5))

def pgN(key): return f"Página {PAGES.get(key, ['?'])[0]}."

def APA(header, rows, widths):
    t = doc.add_table(rows=len(rows) + 1, cols=len(header)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for j, h in enumerate(header):
        c = t.rows[0].cells[j]; cell_lines(c, [(h, True)], WD_ALIGN_PARAGRAPH.CENTER if j else WD_ALIGN_PARAGRAPH.LEFT); borders(c, top=12, bottom=6)
    for i, row in enumerate(rows, 1):
        for j, v in enumerate(row):
            c = t.rows[i].cells[j]; cell_lines(c, [(v, False)], WD_ALIGN_PARAGRAPH.CENTER if j and len(header) > 2 else WD_ALIGN_PARAGRAPH.LEFT)
            borders(c, bottom=12 if i == len(rows) else None)
    fix_widths(t, [Cm(w) for w in widths])
    for k, r in enumerate(t.rows):
        r._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        if k < len(t.rows) - 1:
            for c in r.cells:
                for p in c.paragraphs: p.paragraph_format.keep_with_next = True

_CADENA = CADENA
def CADENA(titulo, elems, nota=None, fuente=None):
    _CADENA(titulo, elems, None)
    SRC(fuente or "BCRP, RI setiembre 2026; BCRPData; UCSUR, EEFF auditados 2023-2025.")
    if nota: P(nota, bold=True)

def IMGW(name, w=12.5): IMG(name, min(w, 12.5) / 2.54)
def AC(text):
    p = doc.add_paragraph(); run(p, "Análisis crítico — ", True); run(p, text)

# ============ CARÁTULA ============
for txt in ("PONTIFICIA UNIVERSIDAD CATÓLICA DEL PERÚ", "ESCUELA DE POSGRADO"): P(txt, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = Pt(18)
p.add_run().add_picture(os.path.join(S, "logo", "word", "media", "image1.png"), width=Inches(3.0))
P("", after=40)
P("ANÁLISIS MACROECONÓMICO", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
P("UNIVERSIDAD CIENTÍFICA DEL SUR S.A.C. (RUC 20421239275)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=60)
P("PRESENTADO POR", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
P("[NOMBRE]", align=WD_ALIGN_PARAGRAPH.CENTER, after=30)
P("PROFESOR", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
P("Sergio Julio Chión Chacón", align=WD_ALIGN_PARAGRAPH.CENTER, after=90)
P("LIMA, NOVIEMBRE 2026", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

# ============ RESUMEN ============
H1("Resumen")
T("El entorno internacional de 2026 sostiene el ingreso de las familias peruanas, pero encarece los costos de UCSUR. La economía mundial crecería 3,1% en 2026 y 2027 y China 4,5% (BCRP, RI setiembre 2026); el cobre promedia US$6,14 por libra, 36% más que en 2025, y los términos de intercambio del Perú mejoran 18,1%, lo que eleva el empleo formal del que depende la matrícula. En sentido contrario, el conflicto en Medio Oriente llevó el petróleo WTI de US$64,4 a US$98,9 por barril entre febrero y octubre, y la Reserva Federal subió su tasa a 3,75%–4,00% ante una inflación PCE de 3,7%. Para UCSUR el efecto favorable llega con rezago por el empleo, mientras el desfavorable es inmediato: la energía de sus sedes y el equipamiento académico importado, que ya cuesta 5,1% más en soles que en diciembre de 2025. " + pgN("s1int"))
T("La economía peruana crece con empleo y crédito, pero con menos poder adquisitivo por una inflación de oferta. El PBI crecería 3,2% en 2026 y 3,0% en 2027 según el BCRP (3,4% en ambos años según el MMM 2027-2030), y el sector de otros servicios, que incluye la educación, creció 4,0% en 2025 y 4,6% entre enero y julio de 2026 (INEI). La inflación de Lima llegó a 5,25% en octubre, sobre el rango meta, y deja una tasa real ex post de −1,00% con la tasa de referencia en 4,25%; la liquidez en soles crece 16,7% y el crédito de consumo 13,2%. El desempleo de Lima bajó a 4,4%, pero el ingreso real promedio cae 4,0%. Hay más familias que pueden matricular a un hijo, pero cada pensión pesa más en su presupuesto, y el sol estable en S/3,412 contiene el costo importado. " + pgN("s1peru"))
T("UCSUR es una universidad privada licenciada por la SUNEDU que vende un servicio de consumo a hogares de clase media de Lima Sur, otorga crédito a sus estudiantes y se financia con bancos y proveedores. No tiene un cliente grande: sus ingresos por derechos de enseñanza, que pasaron de S/264,1 millones en 2022 a S/594,8 millones en 2025, provienen de miles de pensiones cobradas en soles. Su margen operativo subió de 15,8% en 2023 a 36,9% en 2025 y su utilidad neta llegó a S/141,6 millones. Financia a sus alumnos con el fraccionamiento de pensiones (cuentas por cobrar de S/48,8 millones, 30 días de cobro), recibe crédito de proveedores (S/40,0 millones) y de bancos (obligaciones financieras de S/172,8 millones) y compra en dólares parte de su capex de S/82,5 millones. Depende así de las cuatro variables clave: PBI, inflación, tasa de interés y tipo de cambio. " + pgN("s2desc"))
T("La incidencia más importante del entorno sobre UCSUR pasa por el consumo de servicios y por la inflación. Frente al PBI de otros servicios, la elasticidad de sus ingresos reales fue 6,4 en 2023, 7,7 en 2024 y 9,9 en 2025, porque además del ciclo ganó participación de mercado; con una elasticidad base de 4,0 y el crecimiento de servicios proyectado por el BCRP (4,3% en 2026 y 3,7% en 2027), sus ingresos llegarían a S/733,8 millones en 2026 y S/859,2 millones en 2027. La inflación de 5,25% eleva en S/18,0 millones la planilla y los gastos generales, resta S/2,6 millones al valor real de las cuentas por cobrar y alivia S/2,1 millones de las cuentas por pagar. Cada alza de 25 pb cuesta S/0,43 millones sobre una deuda con costo implícito de 10,2%, y un tipo de cambio de S/3,60 encarecería 10,9% el equipamiento importado. " + pgN("s2imp"))
T("La conclusión central es que el riesgo de UCSUR para 2026-2028 no está en el volumen, sostenido por el empleo y el crédito, sino en la cobranza y en el poder adquisitivo de sus familias. Las cuentas por cobrar crecieron 139% en 2025, más de tres veces que los ingresos (41,5%), y los castigos de pensiones 84%, en un ciclo de liquidez abundante (+16,7%) que el BCRP podría cerrar con un alza de tasas para corregir una tasa real negativa. Por eso la recomendación macroeconómica principal es trasladar el financiamiento de la matrícula al sistema financiero mediante convenios de crédito educativo a tasa fija con bancos y cajas, mientras el crédito de consumo crezca más de 10% y antes de que la tasa de referencia supere 4,25%. La meta es bajar la cobranza de 30 a 20 días y liberar S/16,3 millones de capital de trabajo. " + pgN("s3"))

# ============ SECCIÓN 1 ============
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
H2("Análisis de la economía internacional y sus incidencias sobre la economía del país en que la empresa desarrolla sus principales actividades.")

SUB("1. Crecimiento económico mundial y demanda de educación superior")
T("El BCRP mantuvo en 3,1% el crecimiento mundial para 2026 y 2027, debajo del 3,4% de 2025 (RI setiembre 2026). El conflicto en Medio Oriente resta actividad, pero la inversión en inteligencia artificial y la transición energética la compensan: Estados Unidos crecería 2,2%, China 4,5% y América Latina 2,2%. El Perú (3,2%) crece por encima del promedio porque exporta los metales que esa inversión demanda, y ese ingreso externo se convierte en empleo: el sector privado formal sumó alrededor de 242 mil puestos en 2026 (BCRP, RI setiembre 2026). UCSUR no exporta, pero su demanda depende del empleo de las familias de Lima Sur; por eso el crecimiento mundial le llega a través del PBI peruano, del empleo y del consumo de servicios, con rezago.")
CAP("Gráfico 1. Crecimiento del PBI por Economía, 2025–2027 (var. % real)")
IMGW("g1.png")
SRC("BCRP, Reporte de Inflación setiembre 2026, con base en FMI y Consensus Forecast.")
INT("El gráfico 1 muestra que el Perú crece 0,1 pp por encima del mundo y 1,0 pp por encima de América Latina. Para el BCRP, esa diferencia viene del ingreso minero; para UCSUR, es el empleo formal que sostiene la matrícula universitaria privada de clase media.")
CADENA("Cadena 1. Crecimiento Mundial (Y*) → PBI Peruano (Y) → Ingresos de UCSUR",
       [("↑Y*", "Mundo 3,1%; China 4,5%"), ("↑Px", "Cobre +36%"), ("↑TI", "+18,1% (2026)"), ("↑Y", "Perú 3,2%"), ("↑Empleo", "+242 mil formales"), ("↑Ventas UCSUR", "S/594,8 MM (2025)")],
       "Si crece la economía mundial → suben los precios de los metales y los términos de intercambio → crece el PBI peruano y el empleo formal → las familias de Lima Sur matriculan y pagan pensiones → suben los ingresos de UCSUR.")
CADENA("Cadena 2. Crecimiento Mundial (Y*) → Inflación (P) y Tasa de Interés (i): Ajuste hasta Y = Yn",
       [("↑Y*", "Aceleración mundial; WTI US$98,9"), ("Y > Yn", "DA +6,2% (2026P)"), ("↑P", "π 5,25% (oct-26)"), ("↓M/P", "Saldos reales a la baja"), ("↑i", "Presión sobre 4,25%"), ("↓Y", "3,0% (2027P), hasta Y = Yn")],
       "Si la demanda empuja el producto sobre su potencial → suben los precios → caen los saldos reales → sube la tasa de interés → el PBI se modera a 3,0% en 2027 hasta que Y = Yn. Para UCSUR, el ajuste significa crédito educativo más caro y matrícula 2027 más lenta.")

SUB("2. Precios internacionales de commodities: petróleo, energía y cobre")
T("El petróleo WTI promedió US$98,9 por barril en octubre de 2026, frente a US$64,4 en febrero y a US$65,5 de promedio en 2025 (BCRPData, serie PN01660XM); el RI supuso US$82 para 2026, de modo que octubre lo supera en 21%. El cobre promedió US$6,59 por libra en octubre y US$6,14 entre enero y octubre (PN01652XM), 36% más que en 2025. Para el Perú el saldo es positivo, porque los metales pesan más en las exportaciones que el petróleo en las importaciones. Para UCSUR el saldo es mixto: el cobre sostiene el ingreso nacional, pero la energía se traslada en semanas a las tarifas eléctricas de sus laboratorios y campus, dentro de gastos generales de S/128,2 millones en 2025 (EEFF 2025, nota 19), y a los pasajes de sus estudiantes.")
CAP("Gráfico 2. Petróleo WTI y Cobre LME, enero 2025 – octubre 2026 (promedio mensual)")
IMGW("g2.png")
SRC("BCRPData, series PN01660XM y PN01652XM (consulta del 11 de noviembre de 2026); BCRP, RI setiembre 2026.")
CAP("Modelo 1. Mercado Internacional del Petróleo: Contracción de la Oferta, 2026")
IMGW("m1.png", 10.5)
SRC("BCRPData (WTI de febrero y octubre de 2026). Curvas ilustrativas con precios observados; diagrama conceptual.")
INT("El modelo 1 muestra que la oferta se contrajo de S₀ a S₁ y, con una demanda poco sensible al precio, el equilibrio pasó de E₀ (US$64,4) a E₁ (US$98,9), +53,5%. Para el BCRP es un choque de oferta que sube la inflación sin elevar el producto; para UCSUR es un choque de costos, no de demanda.")
CADENA("Cadena 3. Petróleo → Inflación (P) → Salario Real y Costos de UCSUR",
       [("↑WTI", "US$64,4 → US$98,9"), ("↑P energía", "Tarifas y pasajes"), ("↑π", "5,25% (oct-26)"), ("↓w/P", "Ingreso real −4,0%"), ("↑Costos UCSUR", "Generales S/128,2 MM"), ("↓Margen", "36,9% en riesgo")],
       "Si sube el petróleo → sube la inflación → cae el salario real de las familias y suben los costos operativos de UCSUR → se reduce su margen y la capacidad de pago de sus estudiantes al mismo tiempo.")

SUB("3. Desempeño financiero de Universidad Científica del Sur S.A.C. 2024–2025")
T("En 2025 UCSUR facturó S/594,8 millones por derechos de enseñanza (+41,5%; EEFF 2025, nota 17), su máximo histórico, en un año de inflación baja (1,5%) y sol apreciado. La planilla docente y administrativa creció 26,7%, a S/214,7 millones (nota 18), y los gastos generales 17,8%, a S/128,2 millones (nota 19); como los costos crecieron menos que los ingresos, el margen operativo subió de 28,8% a 36,9% y la utilidad neta de S/76,5 a S/141,6 millones. El flujo de operación fue S/230,6 millones, que financió un capex de S/82,5 millones (nota 9(a)) y un prepago de arrendamientos de S/77,3 millones (nota 8(c)). El balance mostró dos alertas: las cuentas por cobrar crecieron 139%, a S/48,8 millones (nota 4), y las obligaciones financieras 31,6%, a S/172,8 millones (nota 13).")
CAP("Gráfico 3. Resultados de UCSUR, 2022–2025 (S/ millones y margen operativo)")
IMGW("g13.png")
SRC("UCSUR, Estados financieros auditados 2023, 2024 y 2025, estado de resultados integrales (notas 17 a 19). Cifras de 2024 según el comparativo del informe 2025.")
INT("El gráfico 3 muestra que el margen cayó en 2023 (15,8%), cuando el PBI se contrajo y la inflación promedio fue 6,3%, y subió hasta 36,9% con inflación de 1,5%. La lectura macro es directa: los costos de UCSUR son en gran parte fijos, por lo que la inflación y la matrícula mueven la utilidad más que proporcionalmente.")
CADENA("Cadena 4. Consumo de Servicios (C) e Inflación (P) → Margen de UCSUR",
       [("↑C servicios", "Otros servicios +4,0% (2025)"), ("↓π", "1,5% (2025)"), ("↑Ingresos", "+41,5%"), ("Costos fijos", "Personal +26,7%"), ("↑Margen", "28,8% → 36,9%"), ("↑Utilidad", "S/141,6 MM (+85,1%)")],
       "Si crece el consumo de servicios con inflación baja → los ingresos crecen más que los costos fijos → sube el margen operativo → la utilidad crece más que proporcionalmente; con inflación alta, el apalancamiento opera al revés.",
       "INEI; BCRPData; UCSUR, EEFF auditados 2025, notas 17 a 19.")

SUB("4. Política monetaria global y tipo de cambio")
T("La Reserva Federal subió su tasa 25 pb el 17 de setiembre de 2026, a 3,75%–4,00%, después de haberla recortado a 3,50%–3,75% en diciembre de 2025 (Federal Reserve, 2026). Con el BCRP en 4,25%, el diferencial frente al punto medio de la Fed se redujo a 0,375 pp. El sol, sin embargo, se mantiene estable: S/3,442 en promedio en octubre y S/3,412 el 9 de noviembre, frente a S/3,367 en diciembre de 2025 (BCRPData, PN01210PM y PD04638PD), porque el superávit comercial y las compras del BCRP compensan el menor atractivo de las tasas en soles.")
EQ("Paridad descubierta de tasas: i = i* + Δe esperada + ρ   →   4,25% = 3,875% + (Δe + ρ)   →   Δe + ρ = 0,375 pp")
CAP("Gráfico 4. Tasa de Referencia del BCRP y Tasa de la Fed, enero 2024 – octubre 2026 (%)")
IMGW("g16.png")
SRC("BCRPData, serie PD04722MM; Federal Reserve (2026), cambios de la tasa de política (punto medio del rango).")
INT("El gráfico 4 muestra que el diferencial se estrechó de más de 1 pp en 2024 a 0,375 pp en 2026. Para el BCRP, un margen tan pequeño implica que el sol depende del superávit externo y de sus reservas, no de las tasas; para UCSUR, que cobra en soles, el riesgo está en el costo de lo que importa.")
CAP("Modelo 2. Mercado Cambiario: Oferta y Demanda de Dólares, diciembre 2025 – noviembre 2026")
IMGW("m2.png", 10.5)
SRC("BCRPData; BCRP, RI setiembre 2026. Diagrama conceptual con valores observados.")
INT("El modelo 2 muestra que la Fed y el petróleo desplazan la demanda de dólares de D$₀ a D$₁, pero la oferta abundante limita el alza: el equilibrio pasa de E₀ (S/3,367) a E₁ (S/3,412), apenas +1,3%.")
CADENA("Cadena 5. Tasa de la Fed (i*) → Tipo de Cambio (E) → Costo Importado de UCSUR",
       [("↑i*", "Fed 3,75%–4,00%"), ("↓(i − i*)", "0,375 pp"), ("↑Salida de capital", "No residentes 45%"), ("↑E", "S/3,367 → S/3,412"), ("↑Costo importado", "Equipos y licencias"), ("↑Capex UCSUR", "S/82,5 MM (2025)")],
       "Si sube la tasa de la Fed → se reduce el diferencial de tasas → salen capitales → sube el tipo de cambio → sube el costo en soles del equipamiento → sube el capex de UCSUR.")

SUB("5. Economía de Estados Unidos, inflación importada y costo del equipamiento académico")
T("UCSUR ofrece carreras de ciencias de la salud, ambientales y veterinaria que requieren laboratorios, simuladores clínicos, equipos de diagnóstico y licencias de software facturados en dólares. La inflación PCE de Estados Unidos proyectada para 2026 es 3,7% (Fed, citada en BCRP, RI setiembre 2026), y el sol pasó de S/3,367 en diciembre de 2025 a S/3,412. Con compras de activos fijos de S/82,5 millones en 2025 (+78,7%; EEFF 2025, nota 9(a)), la universidad está expuesta a ambas variables.")
EQ("Costo en soles = P* × (1 + π*) × E   →   US$1 MM: 1,037 × 3,412 = S/3,538 MM frente a S/3,367 MM en dic-25 (+5,1%)")
CAP("Gráfico 5. Costo en Soles de un Equipo Académico de US$1 MM: Efectos de Precio y Tipo de Cambio")
IMGW("g5.png")
SRC("Cálculo con tipo de cambio de BCRPData (diciembre de 2025 y 9 de noviembre de 2026) e inflación PCE 2026 de 3,7% (Fed, citada en BCRP, RI setiembre 2026).")
INT("El gráfico 5 muestra que, con un sol estable, casi todo el encarecimiento viene de la inflación de EE.UU.; cada 10 céntimos de alza del tipo de cambio añaden cerca de 3 pp. Con S/3,60, el mismo equipo costaría 10,9% más que en diciembre de 2025.")
CADENA("Cadena 6. Inflación de EE.UU. (π*) → Tipo de Cambio (E) → Capex de UCSUR",
       [("↑π*", "PCE 3,7% (2026P)"), ("↑i*", "Fed 3,75%–4,00%"), ("↑E", "S/3,412 (9-nov)"), ("↑P* × E", "Equipo +5,1% en S/"), ("↑Capex", "S/82,5 MM (2025)"), ("↓Flujo libre UCSUR", "Tras capex y deuda")],
       "Si sube la inflación de EE.UU. → la Fed mantiene tasas altas → sube el tipo de cambio → sube el precio en soles del equipamiento → sube el capex → se reduce el flujo libre de UCSUR.")
T("El diagrama de Ishikawa agrupa los seis factores internacionales: las espinas verdes empujan el ingreso de las familias y las rojas, los costos de UCSUR.")
CAP("Diagrama 1. Ishikawa de Factores Internacionales que Afectan a UCSUR, 2026–2027")
IMGW("i1.png")
SRC("BCRP, RI setiembre 2026; BCRPData; Federal Reserve (2026). Diagrama conceptual.")
CRIT("el entorno internacional de 2026 favorece a UCSUR por el ingreso nacional y la perjudica por los costos, y ambos efectos llegan a destiempo. Los términos de intercambio crecen 18,1% y el superávit comercial llega a US$48.865 millones, pero esa riqueza se concentra en minería y en el fisco y llega a las familias de Lima Sur con rezago, a través del empleo formal (242 mil puestos). El petróleo, en cambio, pasó de US$64,4 a US$98,9 en ocho meses y se trasladó en semanas a pasajes y tarifas: la inflación de 5,25% de octubre lo confirma, con un ingreso real que cae 4,0%. La Fed agrega una tercera presión: con un diferencial de solo 0,375 pp, el sol depende de las compras del BCRP y no de las tasas. El crecimiento de 41,5% de los ingresos de UCSUR en 2025 no se explica por el entorno externo, que fue similar en 2024 y 2025; por eso la universidad no debe leer el buen momento minero como una garantía de demanda, sino como un viento de cola que puede revertirse si el cobre cae o si la Fed vuelve a subir.")
ESTR("UCSUR debe usar la estabilidad cambiaria que hoy le dan el superávit externo y las reservas de US$96.668 millones para blindar su estructura de costos antes de que el ciclo cambie. Con un capex del orden de S/80 millones al año y un diferencial de tasas de 0,375 pp, conviene comprar forwards para la mitad de sus compras de equipamiento de 2027 mientras el tipo de cambio esté por debajo de S/3,45; si el sol llegara a S/3,60, esa cobertura evitaría hasta S/2,2 millones de sobrecosto al año. Frente al petróleo a US$98,9, debe negociar contratos de energía con precio fijo o tope por 24 meses, porque la inflación de energía se traslada a sus costos antes que a sus pensiones. Y debe programar las compras de equipos en tramos trimestrales y priorizar proveedores con precios fijados en soles, para promediar el tipo de cambio en un año en que la Fed puede volver a subir. Estas medidas no dependen de la matrícula: protegen el margen de 36,9% justo cuando el entorno internacional deja de ser un viento de cola y pasa a ser una fuente de costos.")

H2("Situación macroeconómica del Perú y perspectivas 2025–2027: Dependencia de Universidad Científica del Sur S.A.C. del entorno nacional"); MARK("s1peru")

SUB("1. PBI sectorial con énfasis en servicios y educación privada, sectores clave de UCSUR")
T("El PBI peruano creció 3,4% en 2025 y crecería 3,2% en 2026 y 3,0% en 2027 según el BCRP (RI setiembre 2026), y 3,4% en ambos años según el MEF (MMM 2027-2030), que además espera 4,0% en promedio para 2028-2030; el Consejo Fiscal considera exigente esa cifra, por lo que para 2028 se adopta como supuesto un crecimiento de 3,0%. Para UCSUR el PBI relevante no es el total sino el de educación. El INEI no publica una serie anual de educación por separado: la registra dentro de «Otros servicios», que comprende la educación pública y privada, la salud y los servicios inmobiliarios y personales. Ese sector creció 3,4%, 2,3%, 3,6% y 4,0% entre 2022 y 2025, más que el PBI total, y 4,6% entre enero y julio de 2026; en el primer trimestre de 2026 la educación privada creció 4,2% (INEI). Se elige este PBI porque mide la demanda del servicio que vende UCSUR: en 2023, cuando el PBI cayó 0,4%, otros servicios crecieron 2,3%.")
CAP("Tabla 1. PBI Total, Otros Servicios (Educación) y Consumo Privado, 2022–2026 (var. % real)")
APA(["Indicador", "2022", "2023", "2024", "2025", "2026*"], [
    ["PBI total", "2,8", "−0,4", "3,5", "3,4", "3,1"],
    ["Otros servicios (incluye educación pública y privada)", "3,4", "2,3", "3,6", "4,0", "4,6"],
    ["Consumo privado", "3,6", "0,1", "2,8", "3,6", "3,6"],
    ["Ingresos reales de UCSUR", "—", "14,7", "27,7", "39,4", "—"],
    ["Elasticidad ingresos UCSUR / otros servicios", "—", "6,4", "7,7", "9,9", "—"],
], [6.4, 1.7, 1.7, 1.7, 1.7, 1.7])
SRC("INEI, Informe Técnico PBI Trimestral IV-2022 (cuadro de otros servicios), Compendio Estadístico 2025 (cuadro 1.3.1), PBI Trimestral I-2026 (cuadro 21) y Producción Nacional julio 2026; BCRPData (PBI y consumo por tipo de gasto); UCSUR, EEFF auditados. * 2026: PBI enero-agosto, otros servicios enero-julio y consumo privado proyectado por el BCRP.")
EQ("PBI = C + I + G + (X − M)   →   3,20% = 2,36 (C) + 2,87 (Ipriv) + 0,06 (Ipub) + 0,70 (inventarios) + 0,45 (G) + 0,03 (X) − 3,27 (M)")
T("Para el BCRP, la identidad, calculada con las ponderaciones reales de 2025 (BCRPData, PN02528AQ a PN02537AQ), cuadra con su proyección y muestra un crecimiento de demanda interna: consumo e inversión aportan 5,23 pp. Para UCSUR, el consumo privado (65,6% del PBI) es su mercado, y los servicios, donde está la educación, crecerían 4,3% en 2026 y 3,7% en 2027 (RI setiembre 2026).")
CAP("Tabla 2. Proyecciones Macroeconómicas del Perú: BCRP frente al MEF, 2026–2028")
APA(["Variable", "BCRP 2026P", "BCRP 2027P", "MEF 2026P", "MEF 2027P", "MEF 2028P"], [
    ["PBI (var. %)", "3,2", "3,0", "3,4", "3,4", "4,0*"],
    ["Consumo privado (var. %)", "3,6", "3,0", "n. d.", "n. d.", "n. d."],
    ["Inversión privada (var. %)", "14,0", "8,5", "10,5", "n. d.", "n. d."],
    ["Servicios (var. %)", "4,3", "3,7", "n. d.", "n. d.", "n. d."],
    ["Inflación (%)", "4,2", "2,0", "n. d.", "2,5", "n. d."],
    ["Tipo de cambio (S/ por US$)", "n. d.", "n. d.", "n. d.", "3,35", "n. d."],
    ["Déficit fiscal (% del PBI)", "1,5", "1,5", "n. d.", "1,4", "1,0*"],
    ["Deuda pública (% del PBI)", "n. d.", "28,2", "29,3", "n. d.", "28,6**"],
], [5.1, 2.0, 2.0, 2.0, 2.0, 2.0])
SRC("BCRP, RI setiembre 2026; MEF, Marco Macroeconómico Multianual 2027-2030 y supuestos del Proyecto de Presupuesto 2027, según Gestión, Forbes Perú y Energiminas (agosto-setiembre de 2026); el PDF del MEF no fue accesible desde el entorno de trabajo. * Promedio 2028-2030. ** 2030. n. d.: no disponible en las fuentes consultadas.")
CAP("Gráfico 6. PBI Total, Otros Servicios y Consumo Privado, 2022–2026 (var. % real)")
IMGW("g15.png")
SRC("INEI y BCRPData, según la tabla 1.")
INT("El gráfico 6 muestra que el sector que incluye la educación crece de forma más estable que el PBI: no cayó en 2023 y se acelera en 2026. Para UCSUR eso significa una demanda menos cíclica que la de la economía, pero sensible al ingreso de las familias.")
CAP("Modelo 3. Oferta Agregada y Demanda Agregada: Perú 2025–2026")
IMGW("m3.png", 10.5)
SRC("BCRP, RI setiembre 2026; BCRPData. Diagrama conceptual con cifras observadas y proyectadas.")
INT("El modelo 3 muestra que la demanda agregada se desplazó a la derecha por la inversión y el consumo, y la oferta a la izquierda por el petróleo y El Niño: el equilibrio pasa de E₀ (π 1,5%; PBI 3,4%) a E₁ (π 5,25%; PBI 3,2%). Para UCSUR, OA₁ sube los precios sin subir el ingreso de sus familias.")
CADENA("Cadena 7. PBI de Servicios (Y servicios) y Consumo (C) → Ventas de UCSUR",
       [("↑C", "+3,6% (2026P)"), ("↑Y servicios", "+4,3% (2026P)"), ("↑Educación privada", "+4,2% (I-26)"), ("↑Ventas UCSUR", "ε = 7,7–9,9"), ("↓C en 2027", "+3,0%"), ("↓Crecimiento", "Menor espacio de precios")],
       "Si crecen el consumo y el PBI de servicios → sube la demanda de educación privada → suben las ventas de UCSUR; si el consumo se desacelera a 3,0% en 2027 → se reduce el espacio para subir pensiones.")

SUB("2. Inflación y poder adquisitivo del consumidor")
T("La inflación de Lima llegó a 5,25% en octubre de 2026, con 0,57% mensual y 4,88% acumulado en el año (INEI, vía BCRPData, PN01273PM). El origen es de oferta: combustibles, tarifas eléctricas, pasajes y El Niño; la inflación sin alimentos, energía y transporte era 1,8% en setiembre (RI setiembre 2026). El RI proyectó 4,2% para diciembre; para cumplirlo, noviembre y diciembre deberían sumar −0,65%, lo que es improbable, de modo que 2026 cerraría por encima de 5%. Las expectativas a 12 meses están en 3,05% (PD12912AM) y el MEF supone 2,5% para 2027.")
EQ("Cierre 2026:  π nov-dic = (1 + 4,2%) / (1 + 4,88%) − 1 = −0,65%")
CAP("Gráfico 7. Inflación en Lima Metropolitana y Expectativas, enero 2025 – octubre 2026 (%)")
IMGW("g8.png")
SRC("BCRPData, series PN01273PM y PD12912AM; BCRP, RI setiembre 2026.")
INT("El gráfico 7 muestra que la inflación salió del rango meta en marzo y no volvió, mientras las expectativas suben de 2,8% a 3,05%. Para el BCRP es una señal de alza de tasas; para UCSUR, una inflación de servicios proyectada en 5,3% en 2026 hace que la pensión pese más en el presupuesto familiar.")
CADENA("Cadena 8. Inflación (P) → Salario Real (w/P) → Poder Adquisitivo de las Familias",
       [("↑P", "π 5,25% (oct-26)"), ("w nominal", "+0,35%"), ("↓w/P", "−4,0% real"), ("↓Poder de compra", "Familias de Lima Sur"), ("↑Peso de la pensión", "Servicios +5,3%"), ("↑Riesgo de deserción", "Matrícula UCSUR")],
       "Si sube la inflación más que los salarios → cae el salario real → baja el poder de compra de las familias → la pensión pesa más → aumenta el riesgo de deserción en UCSUR.")

SUB("3. Tipo de cambio y su efecto sobre el costo importado")
T("El sol cotizó S/3,412 por dólar el 9 de noviembre de 2026, apenas 1,3% por encima del promedio de diciembre de 2025, después de apreciarse 10,2% en 2025 (BCRPData). El BCRP compró US$15.715 millones en 2026 para moderar la apreciación, y el MEF supone S/3,35 para 2027. Para la economía, un sol estable limita el traslado cambiario a precios; para UCSUR, que importa equipamiento académico y paga licencias en dólares, significa un costo de inversión predecible dentro de un rango de S/3,40–3,50, aunque su pérdida por diferencia de cambio subió a S/1,7 millones en 2025 (EEFF 2025, nota 25.1(ii)).")
CAP("Gráfico 8. Tipo de Cambio Sol/Dólar, enero 2025 – noviembre 2026")
IMGW("g3.png")
SRC("BCRPData, series PN01210PM (promedio mensual bancario) y PD04638PD (interbancario venta, 9 de noviembre de 2026).")
INT("El gráfico 8 muestra que el sol oscila entre S/3,36 y S/3,45 en 2026. Para el BCRP, la estabilidad ancla las expectativas; para UCSUR, permite presupuestar el capex en dólares con un margen de error acotado.")
CADENA("Cadena 9. Tipo de Cambio (E) → Precios Importados (P*×E) → Costos de UCSUR",
       [("↑i*", "Fed 3,75%–4,00%"), ("↑E", "S/3,367 → S/3,412"), ("↑P* × E", "+5,1% por equipo"), ("↑Capex", "S/82,5 MM (2025)"), ("↑Pérdida cambiaria", "−S/1,7 MM (2025)"), ("↓Utilidad UCSUR", "S/141,6 MM (2025)")],
       "Si sube el tipo de cambio → sube el precio en soles de lo importado → sube el capex y la pérdida cambiaria → se reduce la utilidad de UCSUR.")

SUB("4. Empleo, salarios y consumo masivo")
T("La tasa de desempleo de Lima Metropolitana bajó de 5,7% a 4,4% entre los trimestres móviles terminados en setiembre de 2025 y de 2026, y la de los jóvenes de 14 a 24 años de 13,9% a 11,3% (INEI, vía BCRPData, PN38063GM y PN38066GM). El ingreso promedio mensual, en cambio, fue S/2.302, apenas 0,35% más que un año antes (PN38070GM), lo que equivale a una caída real de 4,0% con la inflación de setiembre (4,5%). El consumo privado crecería 3,6% en 2026 y 3,0% en 2027 (RI setiembre 2026). Para UCSUR, el desempleo juvenil importa dos veces: muchos de sus estudiantes trabajan para pagar sus estudios, y la empleabilidad de sus egresados es su principal argumento de venta.")
CAP("Gráfico 9. Desempleo e Ingreso Promedio en Lima Metropolitana, enero 2025 – setiembre 2026")
IMGW("g11.png")
SRC("BCRPData, series PN38063GM, PN38066GM y PN38070GM (promedio móvil de tres meses), con datos del INEI.")
INT("El gráfico 9 muestra la divergencia de 2026: más empleo y menos poder de compra. Para la familia de clase media de Lima Sur, una pensión que sube 5% pesa más que el año anterior, aunque haya más miembros trabajando.")
CADENA("Cadena 10. Empleo (N) → Ingreso de los Hogares (w × N) → Consumo (C) → Matrícula",
       [("↓u", "Lima 4,4%; jóvenes 11,3%"), ("↑N", "+242 mil formales"), ("w nominal", "S/2.302 (+0,35%)"), ("↓w/P", "−4,0% real"), ("C moderado", "+3,6% → +3,0%"), ("Matrícula", "Más alumnos, menos pago")],
       "Si baja el desempleo → sube el número de hogares con ingreso; pero si la inflación supera al salario → el consumo se modera → más familias acceden a la universidad, pero con menor capacidad de pago.")

SUB("5. Términos de intercambio peruanos y contexto del sector de educación superior privada")
T("Los términos de intercambio crecerían 18,1% en 2026 y alcanzarían en 2027 su nivel más alto desde que hay registro (RI setiembre 2026). Las exportaciones sumarían US$119.876 millones y las importaciones US$71.011 millones, con un saldo comercial de US$48.865 millones (12,1% del PBI) y un superávit en cuenta corriente de 4,0% del PBI. Para el sector de educación superior privada, ese ingreso nacional se traduce en empleo urbano y en demanda de servicios, en un mercado que se reordenó con el licenciamiento de la SUNEDU, que dejó operando solo a las universidades licenciadas. UCSUR obtuvo su licencia institucional en 2018 (Res. 039-2018-SUNEDU/CD) y la amplió a tres locales adicionales en Lima en 2021 (Res. 052-2021-SUNEDU/CD), lo que explica parte de su ganancia de participación.")
EQ("Balanza de pagos: BP = CA + KA + ER   →   CA = +4,0% del PBI   →   KA + ER = −4,0% del PBI   →   ↑RIN (US$96.668 MM)")
T("Para el BCRP, el superávit corriente se compensa con salida de capitales y acumulación de reservas, que llegaron a US$96.668 millones el 9 de noviembre (BCRPData). Para UCSUR, esas reservas son un seguro que reduce la probabilidad de un salto cambiario que encarezca su equipamiento.")
CAP("Gráfico 10. Balanza Comercial del Perú, 2025–2027 (US$ miles de millones)")
IMGW("g4.png")
SRC("BCRP, Reporte de Inflación setiembre 2026, cuadro de balanza comercial.")
INT("El gráfico 10 muestra que el saldo comercial sube de US$35.433 millones en 2025 a US$48.865 millones en 2026. Para el país es ingreso disponible y estabilidad cambiaria; para UCSUR, más empleo urbano en sus familias y un costo importado acotado.")
CADENA("Cadena 11. Términos de Intercambio (TI) → Balanza de Pagos (BP) → Tipo de Cambio (E) → UCSUR",
       [("↑TI", "+18,1% (2026)"), ("↑CA", "+4,0% del PBI"), ("↑Oferta de US$", "Saldo US$48.865 MM"), ("↑RIN", "US$96.668 MM"), ("E estable", "S/3,40–3,50"), ("↓Riesgo cambiario", "Capex de UCSUR")],
       "Si mejoran los términos de intercambio → sube el superávit en cuenta corriente → entran más dólares y el BCRP acumula reservas → el tipo de cambio se mantiene estable → baja el riesgo cambiario del capex de UCSUR.")

SUB("6. Crédito educativo y financiamiento de las familias")
T("La liquidez en soles de las sociedades de depósito creció 16,7% interanual en setiembre de 2026 (BCRPData, PN00189MM) y el crédito de consumo 13,2%, frente a 7,3% un año antes (PN00537MM). Ese crédito es la vía por la que muchas familias financian estudios: préstamos de consumo, tarjetas, créditos educativos de bancos y cajas, y becas y créditos públicos del Pronabec, cuyo presupuesto depende de un consumo público que se desacelera de 3,2% en 2026 a 2,3% en 2027 (RI setiembre 2026). La teoría cuantitativa permite leer el exceso de liquidez:")
EQ("M × V = P × Y   →   16,7% + %ΔV = 4,5% + 3,2%   →   %ΔV = −9,0%")
T("Para el BCRP, una caída de 9,0% en la velocidad significa que hay saldos acumulados que pueden convertirse en demanda y en precios si las expectativas suben. Para UCSUR, esa liquidez es hoy una fuente de pago de pensiones; si el BCRP la retira con alzas de tasa, el crédito educativo se encarecerá.")
CAP("Gráfico 11. Liquidez en Soles e Inflación, enero 2025 – octubre 2026 (var. % 12 meses)")
IMGW("g9.png")
SRC("BCRPData, series PN00189MM y PN01273PM; BCRP, RI setiembre 2026.")
CAP("Modelo 4. IS-MP: Crédito, Tasa Real y Producto, 2026")
IMGW("m5.png", 10.5)
SRC("BCRPData (tasa de referencia y expectativas, octubre de 2026); BCRP, RI setiembre 2026. Diagrama conceptual.")
INT("El modelo 4 muestra la IS desplazada a la derecha (IS₁) por el crédito de consumo y la inversión, con la regla monetaria en r = 1,20% (E₁). Si el BCRP sube 25 pb, la MP pasa a MP₁ y el producto se modera en E₂: menos crédito para pensiones y más morosidad para UCSUR.")
CADENA("Cadena 12. Dinero (M) → Crédito de Consumo → Financiamiento Educativo",
       [("↑M", "Liquidez +16,7%"), ("↓V", "−9,0%"), ("↑Crédito de consumo", "+13,2% (set-26)"), ("↑Financiamiento", "Bancos, cajas, Pronabec"), ("↑P", "π 5,25%"), ("↑i (riesgo)", "Ajuste monetario 2027")],
       "Si la liquidez crece más que la economía → se expande el crédito de consumo → más familias financian estudios; pero el exceso de dinero presiona precios → el BCRP puede subir la tasa → el crédito educativo se encarece en 2027.")

SUB("7. Crédito, ciclo de efectivo y capital de trabajo")
T("El BCRP mantiene su tasa de referencia en 4,25% desde setiembre de 2025 (PD04722MM). Con expectativas de inflación de 3,05% y una inflación observada de 5,25%, la tasa real es positiva ex ante y negativa ex post:")
EQ("Fisher: i = r + πᵉ   →   r ex ante = 4,25% − 3,05% = 1,20%;   r ex post = 4,25% − 5,25% = −1,00%")
T("Para el BCRP, una tasa real ex post negativa con inflación sobre el rango meta justifica un alza de 25 pb; el crédito total al sector privado ya crece 10,3%. Para UCSUR, el ciclo de efectivo se alargó: los días de cobro subieron de 18 a 30 entre 2024 y 2025 (cuentas por cobrar / ingresos × 365; EEFF 2025, nota 4), y los días de pago a proveedores de 84 a 114 (cuentas por pagar comerciales / gastos generales × 365; nota 10). La universidad se financia más con proveedores, pero también financia más a sus alumnos.")
CAP("Gráfico 12. Crédito de Consumo y Cobranza de UCSUR")
IMGW("g12.png")
SRC("BCRPData, serie PN00537MM; UCSUR, EEFF auditados 2023-2025, nota 4.")
INT("El gráfico 12 muestra dos ciclos paralelos: el crédito de consumo se acelera desde mediados de 2025 y las cuentas por cobrar de UCSUR saltan en 2025. Si el BCRP sube la tasa, ambos se revierten a la vez.")
CADENA("Cadena 13. Inflación (P) → Tasa de Interés (i) → Ciclo de Efectivo de UCSUR",
       [("↑P", "π 5,25%"), ("↓r", "Ex post −1,00%"), ("↑i BCRP", "4,25% → 4,50% (escenario)"), ("↑Tasas de crédito", "Consumo y empresas"), ("↑Días de cobro", "18 → 30 días"), ("↑Capital de trabajo", "CxC S/48,8 MM")],
       "Si la inflación supera el rango meta → la tasa real cae → el BCRP sube la tasa → se encarece el crédito → las familias pagan más tarde → crece el capital de trabajo que UCSUR inmoviliza en cuentas por cobrar.")
T("El diagrama de Ishikawa doméstico reúne los seis factores de la economía peruana que determinan la matrícula, la cobranza y el margen de UCSUR.")
CAP("Diagrama 2. Ishikawa de Factores Domésticos que Afectan a UCSUR, 2026–2027")
IMGW("i2.png")
SRC("BCRP, RI setiembre 2026; BCRPData; UCSUR, EEFF auditados 2025. Diagrama conceptual.")
CRIT("la economía peruana de 2026 le ofrece a UCSUR más empleo, más liquidez y más crédito, pero menos ingreso real. El desempleo de Lima bajó a 4,4%, la liquidez en soles crece 16,7% y el crédito de consumo 13,2%, mientras el ingreso promedio real cae 4,0% y la inflación llega a 5,25%. La teoría cuantitativa lo explica: con una velocidad que cae 9,0%, hay saldos acumulados que hoy pagan pensiones pero que mañana pueden traducirse en inflación y en un alza de tasas, porque la tasa real ex post ya es −1,00%. El sector que incluye la educación crece 4,6% en 2026, más que el PBI, pero la oferta se contrajo por el petróleo y El Niño, y el modelo OA-DA muestra el resultado: más precios con el mismo producto. Para una universidad que vende a la clase media de Lima Sur, esa combinación es especialmente peligrosa, porque la matrícula se sostiene por el empleo mientras la capacidad de pago se erosiona por la inflación. La política fiscal no compensa: el consumo público se desacelera de 3,2% a 2,3% y limita las becas justo cuando más familias las necesitan.")
ESTR("UCSUR debe aprovechar la ventana de liquidez y crédito barato de 2026 antes de que el ciclo monetario se endurezca. Con la liquidez creciendo 16,7% y el crédito de consumo 13,2%, los bancos y cajas tienen fondos para ofrecer crédito educativo a las familias de Lima Sur; la universidad debe asociarse con ellos para que el financiamiento de la matrícula salga de su balance. Al mismo tiempo, debe preparar su política de precios para un escenario de alza de tasas en 2027: con la tasa real ex post en −1,00% y expectativas de 3,05%, el BCRP tiene razones para subir 25 pb, lo que encarecería el crédito de sus estudiantes. Frente a un ingreso real que cae 4,0%, conviene diferenciar los reajustes: moderados para alumnos de ciclos avanzados, que ya cubrieron el costo de captación, y alineados con la inflación esperada para ingresantes. Y debe planificar 2027-2028 con un PBI de 3,0% y un crecimiento de servicios de 3,7%, no con el ritmo de 2025 ni con el 4,0% del MMM, reservando parte de la caja operativa como colchón frente a una mayor morosidad.")

# ============ SECCIÓN 2 ============
doc.add_page_break()
H1("Sección 2."); MARK("s2desc")
H2("Descripción de la empresa enfatizando los temas relativos a su dependencia del marco macroeconómico en el cual se desenvuelve la empresa")
SUB("Perfil institucional y posición competitiva")
T("Universidad Científica del Sur S.A.C. (UCSUR) es una universidad privada constituida como sociedad anónima cerrada, licenciada por la SUNEDU, que ofrece pregrado y posgrado con énfasis en ciencias de la salud, ciencias ambientales y veterinaria. Vende un servicio de consumo —la educación universitaria— a estudiantes de clase media de Lima Sur y a sus familias, que pagan pensiones en soles con su salario, con crédito o con becas. No tiene un cliente grande: sus ingresos provienen de miles de hogares, por lo que su riesgo depende del empleo, los salarios y el crédito de las familias. Otorga crédito a sus estudiantes mediante el fraccionamiento de pensiones, recibe crédito de proveedores y de bancos, y compra en dólares parte de su equipamiento.")
CAP("Tabla 1. Ficha Institucional de Universidad Científica del Sur S.A.C.")
APA(["Concepto", "Detalle"], [
    ["Razón social y RUC", "Universidad Científica del Sur S.A.C. — RUC 20421239275"],
    ["Actividad", "Educación superior universitaria privada (pregrado y posgrado)"],
    ["Licenciamiento SUNEDU", "Licencia institucional: Res. 039-2018-SUNEDU/CD (2 de mayo de 2018); modificación con tres locales adicionales en Lima: Res. 052-2021-SUNEDU/CD"],
    ["Propiedad", "Sociedad anónima cerrada; en 2024 absorbió a Pacífico Educad S.A.C. y Rondy S.A.C. (EEFF 2025, nota 1(c))"],
    ["Fundación, sedes y número de alumnos", "No consignados en los EEFF de insumos/; no verificados"],
    ["Clientes", "Estudiantes de clase media de Lima Sur y sus familias; sin cliente grande"],
    ["Moneda de ingresos y costos", "Ingresos 100% en soles; parte del capex y algunos pasivos en dólares"],
    ["Ingresos 2025", "S/594,8 millones (+41,5%; nota 17)"],
    ["Utilidad operativa / neta 2025", "S/219,5 millones (margen 36,9%) / S/141,6 millones"],
    ["Activo total / patrimonio 2025", "S/760,2 millones / S/350,6 millones (nota 15)"],
    ["Auditor 2024-2025", "Tanaka, Valdivia, Arribas & Asociados"],
], [5.0, 11.0])
SRC("UCSUR, Estados financieros auditados 2023, 2024 y 2025; SUNEDU, Res. 039-2018-SUNEDU/CD y Res. 052-2021-SUNEDU/CD.")
INT("La tabla 1 muestra una empresa cuya dependencia macroeconómica es directa: vende un servicio de consumo a hogares, financia parte de esa venta con crédito propio y compra en dólares parte de su inversión.")
SUB("Dependencia de Universidad Científica del Sur S.A.C. respecto a las 4 Variables Macroeconómicas Clave")
T("Las cuatro variables de orientación llegan a UCSUR por canales distintos. El PBI de servicios, donde está la educación, y el consumo privado determinan cuántas familias pueden pagar una universidad privada. La inflación eleva sus costos fijos y reduce el poder de compra de sus clientes. La tasa de interés define el costo del crédito con que las familias pagan y el de la deuda de la universidad. El tipo de cambio afecta el costo de su equipamiento importado.")
CAP("Tabla 2. Variables Macroeconómicas Clave y su Impacto en UCSUR 2023-2027P")
APA(["Variable", "2023", "2024", "2025", "2026P", "2027P", "Impacto en UCSUR"], [
    ["PBI (var. %) BCRP / MEF", "−0,4", "3,5", "3,4", "3,2 / 3,4", "3,0 / 3,4", "↑ Matrícula"],
    ["Otros servicios, incluye educación (var. %)", "2,3", "3,6", "4,0", "4,3*", "3,7*", "↑ Ventas"],
    ["Inflación fin de periodo (%) BCRP / MEF", "3,2", "2,0", "1,5", "4,2 (5,25 oct)", "2,0 / 2,5", "↑ Costos; ↓ poder de compra"],
    ["Tasa de referencia (%)", "6,75", "5,00", "4,25", "4,25 (nov)", "n. d.", "Costo de deuda y crédito"],
    ["Tipo de cambio dic. (S/ por US$)", "3,734", "3,735", "3,367", "3,412 (9-nov)", "3,35 (MEF)", "Costo del equipamiento"],
], [3.7, 1.35, 1.35, 1.35, 2.3, 2.0, 3.0])
SRC("BCRPData (PBI, IPC de Lima, tasa de referencia y tipo de cambio promedio de diciembre); INEI (otros servicios); BCRP, RI setiembre 2026; MEF, MMM 2027-2030 y supuestos del Presupuesto 2027, según prensa. * Proyección del BCRP para el sector servicios.")
INT("La tabla 2 muestra que 2026 combina el mayor crecimiento del sector de servicios del ciclo con la inflación más alta desde 2023, lo que explica el sesgo de tasas al alza y la presión sobre el poder de compra de las familias.")
CAP("Tabla 3. Estados Financieros de UCSUR, 2022–2025 (S/ millones)")
APA(["Partida (nota del EEFF)", "2022", "2023", "2024", "2025", "Var. 25/24"], [
    ["Ingresos por derechos de enseñanza (17)", "264,1", "321,8", "420,4", "594,8", "+41,5%"],
    ["Gastos de personal (18)", "116,8", "152,5", "169,5", "214,7", "+26,7%"],
    ["Gastos generales de operación (19)", "78,4", "94,7", "108,8", "128,2", "+17,8%"],
    ["Provisiones (20)", "2,2", "3,7", "6,2", "7,3", "+17,1%"],
    ["Utilidad de operación", "55,0", "50,8", "121,1", "219,5", "+81,2%"],
    ["Gastos financieros (21)", "16,9", "23,0", "27,2", "27,5", "+1,2%"],
    ["Diferencia de cambio, neta (25.1(ii))", "0,0", "−0,1", "−0,4", "−1,7", "—"],
    ["Utilidad neta", "25,0", "22,0", "76,5", "141,6", "+85,1%"],
    ["Derechos de enseñanza por cobrar (4)", "13,4", "17,7", "20,4", "48,8", "+139,1%"],
    ["Cuentas por pagar comerciales (10)", "23,1", "25,9", "24,9", "40,0", "+60,4%"],
    ["Obligaciones financieras (13)", "89,0", "113,1", "131,3", "172,8", "+31,6%"],
    ["Pasivos por arrendamiento (12)", "98,4", "90,0", "142,6", "102,9", "−27,8%"],
    ["Compra de activos fijos (9(a))", "61,2", "58,6", "46,2", "82,5", "+78,7%"],
    ["Flujo de efectivo de operación", "61,3", "50,2", "141,7", "230,6", "+62,8%"],
], [6.2, 1.8, 1.8, 1.8, 1.8, 2.2])
SRC("UCSUR, Estados financieros auditados 2023, 2024 y 2025 (estado de situación financiera, estado de resultados integrales y estado de flujos de efectivo). Los números entre paréntesis remiten a las notas citadas en los estados; los PDF de insumos/ no incluyen el texto de las notas. Cifras de 2024 según el comparativo reexpresado del informe 2025.")
CAP("Tabla 4. Ratios Financieros de UCSUR, 2022–2025")
APA(["Ratio", "2022", "2023", "2024", "2025"], [
    ["Margen operativo (%)", "20,8", "15,8", "28,8", "36,9"],
    ["Margen neto (%)", "9,5", "6,8", "18,2", "23,8"],
    ["Gastos de personal / ingresos (%)", "44,2", "47,4", "40,3", "36,1"],
    ["Días de cobro (CxC / ingresos × 365)", "19", "20", "18", "30"],
    ["Días de pago (CxP / gastos generales × 365)", "108", "100", "84", "114"],
    ["Liquidez corriente (veces)", "0,83", "0,86", "1,34", "1,43"],
    ["Pasivo total / patrimonio (veces)", "1,78", "1,72", "1,65", "1,17"],
    ["Obligaciones financieras / patrimonio (veces)", "0,64", "0,71", "0,59", "0,49"],
    ["Rentabilidad del patrimonio, ROE (%)", "17,9", "13,9", "34,5", "40,4"],
    ["Rotación del activo (veces)", "0,68", "0,75", "0,72", "0,78"],
], [8.0, 2.0, 2.0, 2.0, 2.0])
SRC("Cálculos con base en UCSUR, EEFF auditados 2023, 2024 y 2025.")
INT("Las tablas 3 y 4 muestran una empresa que ganó rentabilidad y liquidez (liquidez corriente de 0,83 a 1,43 y ROE de 40,4%) y redujo su apalancamiento, pero cuyo capital de trabajo se tensó en 2025: los días de cobro subieron de 18 a 30 y los de pago de 84 a 114.")

SUB("Variable 1. PBI y Consumo Privado: el consumo de servicios educativos define el volumen de ventas")
T("La relación entre el PBI de educación y las ventas de UCSUR es más que proporcional. Frente al PBI de otros servicios, que incluye la educación, la elasticidad de sus ingresos reales fue 6,4 en 2023, 7,7 en 2024 y 9,9 en 2025 (promedio 8,0): mucho mayor que la típica de un servicio de consumo, porque UCSUR además ganó participación tras el licenciamiento. Para proyectar se usan tres escenarios: un techo con la elasticidad promedio (8,0), una base que supone que la mitad de esa elasticidad se mantiene (4,0) y uno prudente sin ganancias de participación (1,5); los dos últimos son supuestos del grupo. Con el crecimiento de servicios del BCRP (4,3% en 2026 y 3,7% en 2027), un supuesto de 3,7% para 2028 y la inflación de 5,25%, 2,0% y 2,0%:")
EQ("ε = %Δ Ingresos reales / %Δ PBI de otros servicios = 39,39% / 4,0% = 9,85 (2025);   Ventas(t) = Ventas(t−1) × (1 + ε × %ΔY servicios) × (1 + π)")
CAP("Tabla 5. Proyección de Ingresos de UCSUR según el PBI de Servicios, 2026P–2028P (S/ millones)")
APA(["Escenario", "Elasticidad", "2025", "2026P", "2027P", "2028P"], [
    ["Techo (promedio 2023-2025)", "8,0", "594,8", "841,4", "1.112,3", "1.470,4"],
    ["Base (supuesto del grupo)", "4,0", "594,8", "733,8", "859,2", "1.006,1"],
    ["Prudente (supuesto del grupo)", "1,5", "594,8", "666,5", "717,5", "772,5"],
    ["PBI de servicios (var. %)", "—", "4,0", "4,3", "3,7", "3,7"],
    ["Inflación (%)", "—", "1,5", "5,25", "2,0", "2,0"],
], [5.0, 2.0, 2.0, 2.2, 2.2, 2.2])
SRC("UCSUR, EEFF 2025, nota 17; INEI (otros servicios 2025); BCRP, RI setiembre 2026 (servicios e inflación 2027P); BCRPData (inflación 2026). Supuestos del grupo para 2028P: servicios 3,7% e inflación 2,0% (centro del rango meta).")
CAP("Figura 1. Ingresos de UCSUR por Escenario y PBI de Servicios, 2022–2028P")
IMGW("g14b.png")
SRC("UCSUR, EEFF auditados 2022-2025; INEI; BCRP, RI setiembre 2026. Proyecciones según la tabla 5.")
INT("La figura 1 muestra que, en el escenario base, los ingresos llegarían a S/733,8 millones en 2026 y S/1.006,1 millones en 2028. El multiplicador opera también a la baja: cada punto menos de crecimiento de servicios resta 4,0 pp al crecimiento real, unos S/23,8 millones sobre la base de 2025.")
CAP("Diagrama 3. Ishikawa de la Variable PBI sobre las Ventas de UCSUR")
IMGW("i5.png")
SRC("INEI; BCRP, RI setiembre 2026; SUNEDU; UCSUR, EEFF 2025. Diagrama conceptual.")

SUB("Variable 2. Inflación: presión sobre costos fijos y sobre el poder de compra")
T("La planilla docente y administrativa (S/214,7 millones; nota 18) y los gastos generales (S/128,2 millones; nota 19) suman S/342,8 millones, 57,6% de los ingresos de 2025. Con una inflación de 5,25%, el solo efecto precio los elevaría en S/18,0 millones, 8,2% de la utilidad de operación. UCSUR no puede trasladar toda la inflación a precios: con una elasticidad alta y un ingreso real que cae 4,0%, un alza de pensiones igual a la inflación observada arriesga matrícula. En 2023, con inflación promedio de 6,3%, el margen operativo cayó a 15,8%.")
CAP("Tabla 6. Inflación y Costos Operativos de UCSUR, 2025–2028P (S/ millones)")
APA(["Concepto", "2025", "2026P", "2027P", "2028P"], [
    ["Inflación aplicada (%)", "1,5", "5,25", "2,0", "2,0"],
    ["Gastos de personal (efecto precio)", "214,7", "225,9", "230,4", "235,0"],
    ["Gastos generales (efecto precio)", "128,2", "134,9", "137,6", "140,3"],
    ["Aumento de costos por inflación", "—", "18,0", "7,2", "7,4"],
], [7.0, 2.2, 2.2, 2.2, 2.2])
SRC("UCSUR, EEFF 2025, notas 18 y 19; BCRPData (inflación 2025 y octubre 2026); BCRP, RI setiembre 2026 (2027P); supuesto del grupo para 2028P. Costos ajustados solo por inflación, sin cambios de plantilla.")
CAP("Figura 2. Costos Operativos de UCSUR e Inflación, 2022–2025")
IMGW("g17.png")
SRC("UCSUR, EEFF auditados 2023-2025, notas 18 y 19; BCRPData (IPC de Lima, promedio anual).")
CAP("Modelo 5. Isocuanta del Servicio Educativo: Docentes y Capital Académico ante la Inflación")
IMGW("m4.png", 10.5)
SRC("UCSUR, EEFF auditados 2025 (gastos de personal y capex); BCRPData. Diagrama conceptual.")
INT("La figura 2 muestra que los costos crecieron 75,7% entre 2022 y 2025 aun con la inflación a la baja, por la expansión. El modelo 5 muestra que la inflación salarial vuelve más empinada la recta de isocosto y desplaza el óptimo de A a B: más laboratorios y plataformas digitales por alumno y menos horas docentes por estudiante, la lógica del capex de S/82,5 millones.")
CAP("Diagrama 4. Ishikawa de la Variable Inflación sobre los Costos de UCSUR")
IMGW("i6.png")
SRC("BCRP; BCRPData; UCSUR, EEFF 2025, notas 10, 18 y 19. Diagrama conceptual.")

SUB("Variable 3. Tipo de Cambio Sol/USD: exposición moderada concentrada en el capex")
T("UCSUR factura en soles y su exposición cambiaria en resultados es pequeña, pero creciente: la pérdida por diferencia de cambio pasó de S/0,1 millones en 2023 a S/1,7 millones en 2025 (nota 25.1(ii)), en un año en que el sol se apreció 10,2%, lo que indica pasivos o compromisos netos en dólares. El detalle de activos y pasivos en moneda extranjera está en la nota 25.1(ii), que no forma parte de los PDF de insumos/. El riesgo mayor está en la inversión: el equipamiento y las licencias se pagan en dólares.")
CAP("Tabla 7. Escenarios de Tipo de Cambio y Costo del Equipamiento Importado de UCSUR")
APA(["Escenario", "TC", "Costo de US$1 MM (S/ MM)", "Var. vs. dic-25", "Sobrecosto en capex de S/80 MM"], [
    ["Apreciación", "3,30", "3,422", "+1,6%", "S/1,3 MM"],
    ["Base (9-nov-26)", "3,412", "3,538", "+5,1%", "S/4,1 MM"],
    ["Depreciación moderada", "3,50", "3,630", "+7,8%", "S/6,2 MM"],
    ["Depreciación fuerte", "3,60", "3,733", "+10,9%", "S/8,7 MM"],
], [3.8, 1.6, 3.4, 2.6, 4.6])
SRC("BCRPData (tipo de cambio); inflación PCE 2026 de 3,7% (Fed, citada en BCRP, RI setiembre 2026). Capex de S/80 MM: supuesto del grupo, cercano a las compras de activos fijos de 2025 (nota 9(a)).")
CAP("Figura 3. Tipo de Cambio de Diciembre y Diferencia de Cambio de UCSUR, 2022–2025")
IMGW("g19.png")
SRC("BCRPData, serie PN01210PM; UCSUR, EEFF auditados 2023-2025, nota 25.1(ii).")
INT("La figura 3 muestra que la pérdida cambiaria creció mientras el sol se apreciaba, señal de una posición pasiva en dólares. Para UCSUR, el tipo de cambio es un riesgo de inversión, no de ventas.")
CAP("Diagrama 5. Ishikawa de la Variable Tipo de Cambio sobre UCSUR")
IMGW("i7.png")
SRC("BCRP, RI setiembre 2026; BCRPData; UCSUR, EEFF 2025. Diagrama conceptual.")

SUB("Variable 4. Tasa de Referencia BCRP: costo de la deuda y del crédito de las familias")
T("La tasa de referencia bajó de 7,50% en diciembre de 2022 a 4,25% en 2025. En ese periodo, UCSUR casi duplicó sus obligaciones financieras, de S/89,0 a S/172,8 millones (nota 13), mientras sus gastos financieros subieron de S/16,9 a S/27,5 millones (nota 21), de los cuales S/12,0 millones son intereses de arrendamientos (nota 12(c)). Excluyendo esos intereses, el costo implícito de su deuda financiera fue 10,2% en 2025. Su posición de liquidez es holgada: caja de S/139,4 millones (nota 3) e ingresos financieros de S/10,1 millones.")
CAP("Tabla 8. Tasa de Referencia y Estructura Financiera de UCSUR, 2022–2025 (S/ millones)")
APA(["Indicador (nota)", "2022", "2023", "2024", "2025"], [
    ["Tasa de referencia BCRP, diciembre (%)", "7,50", "6,75", "5,00", "4,25"],
    ["Obligaciones financieras corrientes (13)", "15,1", "12,3", "17,7", "25,5"],
    ["Obligaciones financieras no corrientes (13)", "73,9", "100,9", "113,6", "147,2"],
    ["Pasivos por arrendamiento (12)", "98,4", "90,0", "142,6", "102,9"],
    ["Gastos financieros (21)", "16,9", "23,0", "27,2", "27,5"],
    ["Intereses de arrendamientos (12(c))", "n. d.", "n. d.", "11,7", "12,0"],
    ["Efectivo y equivalentes (3)", "6,1", "9,8", "75,4", "139,4"],
], [7.0, 2.2, 2.2, 2.2, 2.2])
SRC("BCRPData, serie PD04722MM; UCSUR, EEFF auditados 2023, 2024 y 2025.")
CAP("Figura 4. Gastos Financieros, Diferencia de Cambio y Deuda Financiera de UCSUR, 2022–2025")
IMGW("g10.png")
SRC("UCSUR, EEFF auditados 2023-2025, notas 13, 21 y 25.1(ii).")
INT("La figura 4 muestra que la deuda casi se duplicó, pero los gastos financieros se estabilizaron gracias a la baja de tasas y a la caja acumulada. La sensibilidad de UCSUR a la tasa es moderada en intereses (S/0,43 millones por 25 pb), pero alta en la cobranza.")
CAP("Diagrama 6. Ishikawa de la Variable Tasa de Interés sobre el Financiamiento de UCSUR")
IMGW("i8.png")
SRC("BCRPData; UCSUR, EEFF 2025, notas 3, 12, 13 y 21. Diagrama conceptual.")

H2("En base al análisis de la sección anterior, analizar el impacto del entorno macroeconómico sobre la empresa en cuestión, considerando la situación actual y los próximos tres años."); MARK("s2imp")

SUB("1. Variaciones del PBI y su efecto sobre las ventas de UCSUR")
T("En 2023 el PBI cayó 0,4%, el sector de otros servicios creció 2,3% y los ingresos reales de UCSUR 14,7%; en 2024 y 2025 el sector creció 3,6% y 4,0%, y los ingresos reales 27,7% y 39,4% (nota 17). La universidad crece por encima de la economía porque gana participación, pero su crecimiento sigue atado al consumo de servicios. En el escenario base (ε = 4,0), los ingresos llegarían a S/733,8 millones en 2026, S/859,2 millones en 2027 y S/1.006,1 millones en 2028. Si El Niño redujera el crecimiento de servicios a 3,0% en 2026, la proyección de ese año bajaría a S/701,2 millones.")
AC("el riesgo no es la caída del PBI, sino que la elasticidad se normalice cuando se agote la ganancia de participación; por eso el escenario base usa la mitad de la elasticidad observada.")
CAP("Gráfico 13. PBI, Consumo Privado e Ingresos Reales de UCSUR, 2023–2025 (var. % real)")
IMGW("g7.png")
SRC("UCSUR, EEFF auditados 2023-2025, nota 17; BCRPData.")
CADENA("Cadena 14. PBI de Servicios (Y) → Ventas de UCSUR",
       [("↑Y servicios", "4,3% (2026P)"), ("↑C", "3,6% (2026P)"), ("↑Demanda de educación", "ε base = 4,0"), ("↑Ventas", "S/733,8 MM (2026P)"), ("↓Y servicios 2027", "3,7%"), ("Ventas 2028P", "S/1.006,1 MM")],
       "Si crece el PBI de servicios → sube la demanda de educación privada → suben las ventas de UCSUR; si el sector se desacelera a 3,7% en 2027 → el crecimiento real baja de 17,2% a 14,8%.",
       "INEI; BCRP, RI setiembre 2026; UCSUR, EEFF 2025, nota 17.")

SUB("2. Tasa de interés y su efecto sobre las cuentas por cobrar (CxC)")
T("Las cuentas por cobrar de UCSUR crecieron 139% en 2025, hasta S/48,8 millones (nota 4), y los días de cobro subieron de 18 a 30. La estimación para pérdidas crediticias subió de S/5,3 a S/6,5 millones y los castigos de pensiones de S/2,0 a S/3,7 millones (nota 4(d)). El fraccionamiento funciona como un crédito sin interés explícito: cuando las tasas del sistema suben, se vuelve más atractivo que el crédito bancario y las cuentas por cobrar crecen. Con un costo implícito de deuda de 10,2%, financiar S/48,8 millones de cuentas por cobrar le cuesta a UCSUR unos S/5,0 millones al año en costo de oportunidad.")
AC("el deterioro de 2025 ocurrió con tasas bajas; con un alza de 25 pb a 50 pb en 2027, los días de cobro podrían superar 30 si no cambia la política de fraccionamiento.")
CAP("Tabla 9. Cuentas por Cobrar y Cobranza Dudosa de UCSUR, 2022–2025 (S/ millones)")
APA(["Partida (nota)", "2022", "2023", "2024", "2025"], [
    ["Derechos de enseñanza por cobrar, neto (4)", "13,4", "17,7", "20,4", "48,8"],
    ["Estimación para pérdidas crediticias del año (4(d))", "1,7", "3,6", "5,3", "6,5"],
    ["Castigos de derechos por cobrar (4(d))", "3,1", "0,7", "2,0", "3,7"],
    ["Días de cobro", "19", "20", "18", "30"],
], [7.6, 2.0, 2.0, 2.0, 2.0])
SRC("UCSUR, EEFF auditados 2023-2025, estado de situación financiera y estado de flujos de efectivo, nota 4.")
CADENA("Cadena 15. Tasa de Interés (i) → Crédito de las Familias → CxC de UCSUR",
       [("↑i BCRP", "4,25% → 4,50% (escenario)"), ("↑Tasa de consumo", "Crédito más caro"), ("↑Fraccionamiento", "Pago a plazos"), ("↑CxC", "S/48,8 MM; 30 días"), ("↑Costo de oportunidad", "10,2% × CxC = S/5,0 MM"), ("↑Estimación", "S/6,5 MM (2025)")],
       "Si sube la tasa de interés → se encarece el crédito de consumo → más familias fraccionan la pensión → crecen las cuentas por cobrar y su costo → sube la estimación de cobranza dudosa de UCSUR.",
       "BCRPData; UCSUR, EEFF 2025, nota 4.")

SUB("3. Tasa de interés: efecto sobre cuentas por pagar y gastos financieros")
T("UCSUR tiene obligaciones financieras por S/172,8 millones, S/147,2 millones a largo plazo (nota 13), y pasivos por arrendamiento por S/102,9 millones (nota 12). En 2025 recibió S/61,7 millones de nuevos préstamos y amortizó S/30,6 millones (nota 25.4). Sus gastos financieros fueron S/27,5 millones, casi iguales a los de 2024 pese a una deuda 31,6% mayor, gracias a la baja de tasas y a ingresos financieros de S/10,1 millones. Un alza de 25 pb aplicada a toda la deuda costaría S/0,43 millones al año, y una de 50 pb, S/0,86 millones. Las cuentas por pagar comerciales (S/40,0 millones; nota 10) son financiamiento sin costo: con tasas más altas, su valor aumenta.")
AC("el riesgo de tasas es bajo en resultados (0,2% de la utilidad de operación por cada 25 pb), pero la deuda creció 31,6% y su refinanciamiento en 2027 coincidiría con el posible alza.")
CAP("Tabla 10. Sensibilidad de los Gastos Financieros de UCSUR a la Tasa, 2026P–2028P (S/ millones)")
APA(["Escenario de tasa", "2026P", "2027P", "2028P"], [
    ["Base: gastos financieros constantes (21)", "27,5", "27,5", "27,5"],
    ["Alza de 25 pb sobre S/172,8 MM", "+0,43", "+0,43", "+0,43"],
    ["Alza de 50 pb sobre S/172,8 MM", "+0,86", "+0,86", "+0,86"],
    ["Valor de CxP sin costo al 10,2% (S/40,0 MM)", "4,1", "4,1", "4,1"],
], [8.0, 2.4, 2.4, 2.4])
SRC("UCSUR, EEFF 2025, notas 10, 12, 13 y 21. Supuesto del grupo: deuda constante en 2026-2028.")
CADENA("Cadena 16. Tasa de Interés (i) → Gastos Financieros y CxP de UCSUR",
       [("↑P", "π 5,25%"), ("↓r", "Ex post −1,00%"), ("↑i", "+25 pb (escenario)"), ("↑Gastos financieros", "+S/0,43 MM al año"), ("↑Valor de CxP", "S/40,0 MM sin costo"), ("↓Utilidad neta", "S/141,6 MM (2025)")],
       "Si la inflación lleva al BCRP a subir la tasa → suben los gastos financieros de la deuda de S/172,8 millones → gana valor el crédito de proveedores → se reduce levemente la utilidad neta de UCSUR.",
       "BCRPData; UCSUR, EEFF 2025, notas 10, 13 y 21.")

SUB("4. Inflación y su repercusión sobre los costos operativos")
T("Con una inflación de 5,25%, el efecto precio sobre la planilla (S/214,7 millones; nota 18) y los gastos generales (S/128,2 millones; nota 19) suma S/18,0 millones en 2026, y S/7,2 y S/7,4 millones en 2027 y 2028 con inflación de 2,0%. La planilla se reajusta con rezago, de modo que la inflación de 2026 pesará en los costos de 2027, cuando las pensiones no podrán subir al mismo ritmo. Si los ingresos no se ajustaran, el margen operativo bajaría de 36,9% a 33,9%. El margen de 2023 (15,8%), con inflación promedio de 6,3%, muestra lo que ocurre cuando los costos suben más rápido que las pensiones.")
AC("el traslado a precios es limitado: con un ingreso real que cae 4,0%, UCSUR puede reajustar con la inflación esperada (3,05%), pero no con la observada.")
CADENA("Cadena 17. Inflación (P) → Salarios (w) → Costos Operativos de UCSUR",
       [("↑P", "π 5,25%"), ("↑w", "Reajustes 2027"), ("↑Personal", "S/214,7 → S/225,9 MM"), ("↑Generales", "S/128,2 → S/134,9 MM"), ("↑Costos", "+S/18,0 MM"), ("↓Margen operativo", "36,9% → 33,9%")],
       "Si sube la inflación → suben los salarios y los servicios → suben los costos operativos en S/18,0 millones → si las pensiones no suben al mismo ritmo, el margen operativo bajaría 3,0 pp.",
       "BCRPData; UCSUR, EEFF 2025, notas 18 y 19.")

SUB("5. Inflación y su repercusión sobre CxC y CxP")
T("La inflación redistribuye valor entre UCSUR, sus estudiantes y sus proveedores. Con 5,25%, las cuentas por cobrar de S/48,8 millones (nota 4) pierden S/2,6 millones de poder de compra al año, porque se cobran en soles nominales; las cuentas por pagar comerciales de S/40,0 millones (nota 10) alivian S/2,1 millones, porque se pagan con soles depreciados. El efecto neto es negativo (−S/0,5 millones) y crece con el plazo de cobro. Los proveedores ya trasladan inflación: las cuentas por pagar comerciales subieron 60,4% en 2025 y los días de pago de 84 a 114.")
AC("con 30 días de cobro y 114 días de pago, UCSUR se financia con proveedores, pero esa ventaja se pierde si la inflación lleva a los proveedores a acortar plazos.")
CAP("Tabla 11. Efecto de la Inflación sobre el Valor Real de CxC y CxP de UCSUR, 2026P–2028P (S/ millones)")
APA(["Concepto", "2026P", "2027P", "2028P"], [
    ["Inflación (%)", "5,25", "2,0", "2,0"],
    ["Pérdida real de CxC (π × S/48,8 MM)", "−2,6", "−1,0", "−1,0"],
    ["Alivio real de CxP (π × S/40,0 MM)", "+2,1", "+0,8", "+0,8"],
    ["Efecto neto", "−0,5", "−0,2", "−0,2"],
], [8.0, 2.4, 2.4, 2.4])
SRC("UCSUR, EEFF 2025, notas 4 y 10; BCRPData; BCRP, RI setiembre 2026; supuesto del grupo para 2028P.")
CADENA("Cadena 18. Inflación (P) → Valor Real de CxC y CxP → Capital de Trabajo",
       [("↑P", "π 5,25%"), ("↓Valor real CxC", "−S/2,6 MM"), ("↓Valor real CxP", "+S/2,1 MM"), ("Efecto neto", "−S/0,5 MM"), ("↑Días de cobro", "18 → 30 días"), ("↑Necesidad de caja", "Capital de trabajo")],
       "Si sube la inflación → las cuentas por cobrar pierden más valor real del que se alivia en las cuentas por pagar → con más días de cobro, aumenta la necesidad de capital de trabajo de UCSUR.",
       "BCRPData; UCSUR, EEFF 2025, notas 4 y 10.")

SUB("6. Tipo de cambio y sus implicancias en operaciones y balance")
T("El tipo de cambio no afecta las ventas de UCSUR, que se cobran en soles, pero sí su inversión y algunos pasivos. La pérdida por diferencia de cambio subió a S/1,7 millones en 2025 (nota 25.1(ii)) y el equipamiento importado ya cuesta 5,1% más que en diciembre de 2025. Con un sol entre S/3,40 y S/3,50 en 2026 y S/3,35 en 2027 según el MEF, el riesgo es moderado; una depreciación a S/3,60 elevaría el sobrecosto del capex a S/8,7 millones si fuera íntegramente importado (tabla 7).")
AC("la exposición está concentrada en un rubro que la empresa controla —el calendario de compras de equipos—, por lo que puede cubrirse sin derivados complejos.")
CADENA("Cadena 19. Tipo de Cambio (E) → Costo Importado → Balance de UCSUR",
       [("↑i*", "Fed 3,75%–4,00%"), ("↑E", "S/3,412 → S/3,60"), ("↑P* × E", "+10,9%"), ("↑Capex", "+S/8,7 MM"), ("↑Pérdida cambiaria", "−S/1,7 MM (2025)"), ("↓Flujo libre", "S/148,1 MM (2025)")],
       "Si sube el tipo de cambio → sube el costo en soles del equipamiento y de los pasivos en dólares → aumenta el capex y la pérdida cambiaria → se reduce el flujo libre de UCSUR.",
       "BCRPData; UCSUR, EEFF 2025, notas 9(a) y 25.1(ii).")

SUB("7. Consumo, empleo y poder adquisitivo: efecto sobre la demanda")
T("El desempleo de Lima bajó a 4,4% y el juvenil a 11,3%, pero el ingreso promedio real cayó 4,0%. Para UCSUR, más empleo significa más familias que pueden matricular a un hijo; menos ingreso real significa que esas familias pagan con más dificultad. La señal ya está en su balance: los castigos de pensiones incobrables subieron 84% y la estimación para pérdidas crediticias 23,3% (nota 4(d)), en un año en que los ingresos crecieron 41,5%.")
AC("la demanda se sostiene, pero la calidad de la cobranza empeora; el indicador a vigilar no es la matrícula sino la relación entre castigos e ingresos.")
CADENA("Cadena 20. Empleo (N) y Poder Adquisitivo (w/P) → Demanda y Cobranza de UCSUR",
       [("↓u", "Lima 4,4%; jóvenes 11,3%"), ("↑N", "+242 mil formales"), ("↓w/P", "−4,0% real"), ("↓Capacidad de pago", "Familias de Lima Sur"), ("↑Castigos", "+84% (S/3,7 MM)"), ("↑Riesgo de deserción", "CxC S/48,8 MM")],
       "Si baja el desempleo pero cae el salario real → más familias matriculan, pero con menor capacidad de pago → suben los castigos y el riesgo de deserción en UCSUR.",
       "BCRPData; UCSUR, EEFF 2025, nota 4(d).")

SUB("8. PBI de los clientes de UCSUR (familias de clase media de Lima Sur) y efecto indirecto")
T("UCSUR no tiene un cliente grande: sus clientes son hogares de clase media de Lima Sur, cuyo «PBI» es su ingreso laboral. Ese ingreso depende de sectores urbanos como comercio (+5,9% en 2026), servicios (+4,3%) y construcción (+9,5%), que crecen más que el PBI total (3,2%), y no de la minería o la pesca, que caen por El Niño (RI setiembre 2026). Por eso el efecto indirecto de la macroeconomía sobre UCSUR es más favorable que el del PBI agregado en volumen, pero más desfavorable en precios, porque la inflación golpea sobre todo a hogares urbanos que gastan en transporte y servicios.")
AC("el cliente de UCSUR está en los sectores que más crecen, pero también en los que más sufren la inflación de oferta.")
CADENA("Cadena 21. PBI Sectorial Urbano → Ingreso de las Familias de Lima Sur → Matrícula de UCSUR",
       [("↑Y no primario", "Comercio 5,9%; servicios 4,3%"), ("↑Construcción", "+9,5%"), ("↑Empleo urbano", "Desempleo Lima 4,4%"), ("↑Ingreso familiar", "Nominal +0,35%"), ("↓Ingreso real", "−4,0%"), ("Matrícula estable", "Precio limitado")],
       "Si crecen los sectores urbanos → sube el empleo de las familias de Lima Sur → se sostiene la matrícula; pero como el ingreso real cae → UCSUR tiene poco espacio para subir pensiones.",
       "BCRP, RI setiembre 2026; BCRPData.")

SUB("9. Liquidez del sistema financiero, crédito y riesgo de morosidad")
T("La liquidez en soles crece 16,7% y el crédito de consumo 13,2%, sostenidos por una tasa real negativa. Ese entorno favorece la matrícula financiada, pero UCSUR no lo aprovecha: financia a sus estudiantes con capital propio. Su ciclo de caja lo permite —flujo de operación de S/230,6 millones y flujo libre de S/148,1 millones después del capex en 2025—, pero inmoviliza S/48,8 millones en cuentas por cobrar con una estimación de S/6,5 millones. Si el BCRP sube la tasa, el crédito se desacelerará y la morosidad de las familias subirá.")
AC("la liquidez del sistema es hoy la mejor oportunidad para trasladar el financiamiento de la matrícula a bancos y cajas; en 2027 puede ser tarde.")
CAP("Tabla 12. Ciclo de Caja de UCSUR, 2022–2025 (S/ millones)")
APA(["Concepto", "2022", "2023", "2024", "2025"], [
    ["Flujo de efectivo de operación", "61,3", "50,2", "141,7", "230,6"],
    ["Compra de activos fijos (9(a))", "−61,2", "−58,6", "−46,2", "−82,5"],
    ["Flujo libre (operación − capex)", "0,1", "−8,3", "95,5", "148,1"],
    ["Días de cobro / días de pago", "19 / 108", "20 / 100", "18 / 84", "30 / 114"],
], [7.6, 2.0, 2.0, 2.0, 2.0])
SRC("UCSUR, EEFF auditados 2023-2025, estado de flujos de efectivo y notas 4, 9(a) y 10.")
CADENA("Cadena 22. Liquidez (M) → Crédito → Morosidad → CxC de UCSUR",
       [("↑M", "Liquidez +16,7%"), ("↑Crédito de consumo", "+13,2% (set-26)"), ("↑Matrícula", "Ingresos +41,5%"), ("↑i (escenario)", "Alza de 25 pb"), ("↑Morosidad", "Estimación S/6,5 MM"), ("↑CxC UCSUR", "S/48,8 MM; 30 días")],
       "Si sube la liquidez → crece el crédito de consumo → más familias financian la matrícula; pero si sube la tasa → se encarece ese crédito → sube la morosidad → crecen las cuentas por cobrar y las estimaciones de UCSUR.",
       "BCRPData; UCSUR, EEFF 2025, nota 4.")
CRIT("los nueve canales muestran que el impacto macroeconómico sobre UCSUR se concentra en dos variables: el consumo de servicios y la inflación. El consumo es favorable en el escenario base: con una elasticidad de 4,0 frente al PBI de servicios, los ingresos crecerían a S/733,8 millones en 2026 y S/1.006,1 millones en 2028, aunque cada punto menos de crecimiento del sector restaría unos S/24 millones. La inflación es el riesgo central: suma S/18,0 millones a los costos en 2026, resta S/2,6 millones al valor real de las cuentas por cobrar y reduce 4,0% el ingreso real de las familias. La tasa de interés y el tipo de cambio tienen efectos acotados en resultados (S/0,43 millones por 25 pb y S/2,3 millones por cada 10 céntimos en el capex), pero la deuda de S/172,8 millones y un capex del orden de S/80 millones los amplifican. La señal más preocupante está en el balance: las cuentas por cobrar crecieron 139%, más de tres veces que los ingresos, y los castigos 84%. Si el ciclo de tasas se revierte, esa cartera se convertirá en morosidad.")
ESTR("UCSUR debe gestionar cada variable con un instrumento distinto. Para el consumo, debe sostener el volumen sin forzar precios: reajustar pensiones con la inflación esperada (3,05%) y no con la observada (5,25%), sobre todo para alumnos de ciclos avanzados, porque perder matrícula por deserción cuesta más que los 2,2 pp de reajuste no aplicado. Para la inflación, debe fijar precios en sus contratos de energía y servicios y escalonar los reajustes salariales de 2027, cuando la inflación vuelve a 2,0%. Para la tasa de interés, debe fijar el costo de su deuda de S/172,8 millones mientras la tasa real ex post sea negativa y trasladar el fraccionamiento a convenios de crédito educativo con bancos y cajas, para bajar la cobranza de 30 a 20 días y liberar S/16,3 millones. Para el tipo de cambio, debe cubrir con forwards la mitad del capex importado de 2027. Con estas medidas, el margen operativo podría mantenerse por encima de 33% aun con inflación de 5,25% y alza de tasas, y el flujo libre seguiría financiando el crecimiento sin nueva deuda.")

# ============ SECCIÓN 3 ============
doc.add_page_break()
H1("Sección 3."); MARK("s3")
H2("Recomendaciones, Sugerencias y Comentarios")
SUB("1. Recomendaciones Estratégicas Macroeconómicas")
P("Recomendación R1. Trasladar el financiamiento de la matrícula a convenios de crédito educativo.", bold=True)
T("Variable y hallazgo: liquidez, crédito y tasa de interés; la liquidez en soles crece 16,7% y el crédito de consumo 13,2% (Sección 1, subtema 6), mientras las cuentas por cobrar de UCSUR crecieron 139% y los días de cobro llegaron a 30 (Sección 2, canales 2 y 9). Mientras el crédito de consumo crezca más de 10% y antes de que la tasa de referencia supere 4,25%, UCSUR debería firmar convenios con bancos y cajas para que las familias financien la matrícula con crédito educativo a tasa fija. Meta: bajar la cobranza a 20 días y liberar S/16,3 millones de capital de trabajo en 2027.")
P("Recomendación R2. Reajustar las pensiones con la inflación esperada y no con la observada.", bold=True)
T("Variable y hallazgo: inflación y poder adquisitivo; la inflación llegó a 5,25% con un ingreso real que cae 4,0% (Sección 1, subtemas 2 y 4) y la elasticidad de las ventas al PBI de servicios es alta (Sección 2, Variable 1). Mientras la inflación supere 3%, UCSUR debería limitar el reajuste de 2027 a la inflación esperada (3,05%) y aplicarlo sobre todo a ingresantes. Meta: retención igual o mayor a la de 2025 e ingresos dentro del escenario base (S/859,2 millones en 2027).")
P("Recomendación R3. Fijar la tasa de la deuda antes de un alza del BCRP.", bold=True)
T("Variable y hallazgo: tasa de interés; la tasa real ex post es −1,00% (Sección 1, subtema 7) y cada 25 pb cuestan S/0,43 millones sobre S/172,8 millones de deuda (Sección 2, canal 3). Mientras la tasa de referencia esté en 4,25%, UCSUR debería refinanciar o cubrir con swaps la porción variable de su deuda, aun pagando una prima de alrededor de 0,30 pp. Meta: gastos financieros estables en torno a S/27,5 millones en 2026-2028.")
P("Recomendación R4. Cubrir con forwards la mitad del capex importado.", bold=True)
T("Variable y hallazgo: tipo de cambio; el diferencial con la Fed es 0,375 pp (Sección 1, subtema 4) y el equipamiento ya cuesta 5,1% más en soles; con S/3,60 el sobrecosto llegaría a S/8,7 millones (Sección 2, Variable 3). Mientras el tipo de cambio esté por debajo de S/3,45, UCSUR debería comprar forwards para la mitad de su capex importado de 2027 y programar las compras en tramos trimestrales. Meta: variación cambiaria máxima de 2% en el costo del capex.")
CAP("Tabla 13. Análisis Costo-Beneficio de las Recomendaciones (S/ millones, horizonte 2026–2027)")
APA(["Recomendación", "Costo estimado", "Beneficio estimado", "B/C"], [
    ["R1. Convenios de crédito educativo", "2,0 (comisiones y gestión, 2 años)", "7,2 (capital liberado S/16,3 MM × 10,2% × 2 años + 30% menos estimación de cobranza dudosa)", "3,6"],
    ["R2. Pensiones con inflación esperada", "13,1 (2,2 pp de reajuste no aplicado sobre S/594,8 MM)", "22,0 (evitar la pérdida de 3% de la matrícula del escenario base 2026)", "1,7"],
    ["R3. Fijar la tasa de la deuda", "1,0 (prima de 0,30 pp × S/172,8 MM × 2 años)", "1,7 (alza evitada de 50 pb × S/172,8 MM × 2 años)", "1,7"],
    ["R4. Forwards para el capex", "0,7 (puntos forward de 0,375 pp y spread de 0,5% sobre S/40 MM al año)", "4,4 (sobrecosto evitado si el TC llega a S/3,60: 5,5% × S/40 MM × 2 años)", "6,3"],
    ["Total", "16,8", "35,3", "2,1"],
], [3.8, 4.6, 6.4, 1.2])
SRC("Estimaciones del grupo con base en UCSUR, EEFF auditados 2025; BCRP, RI setiembre 2026; BCRPData. Cifras referenciales.")
INT("La tabla 13 indica que todas las recomendaciones tienen una relación beneficio/costo mayor a 1,5. R2 es la de mayor beneficio absoluto porque protege el volumen de matrícula; R1 resuelve el problema que más se deterioró en 2025, la cobranza; y R4 tiene la mayor relación beneficio/costo, aunque su beneficio solo se materializa si el sol se deprecia.")
SUB("2. Sugerencias Operativas con Base Macroeconómica")
T("S1. SI: el tipo de cambio supera S/3,50 por dólar: postergar las compras de equipamiento no urgentes y ejecutar los forwards contratados; si cae por debajo de S/3,40, adelantar las compras del semestre siguiente.")
T("S2. SI: el crecimiento de otros servicios (INEI) baja de 3% o el desempleo juvenil de Lima supera 13%: congelar las pensiones de los ciclos avanzados y ampliar los descuentos por pronto pago, porque la deserción es más costosa que el reajuste.")
T("S3. SI: el BCRP sube su tasa a 4,50% o más: activar los convenios de crédito educativo a tasa fija y limitar el fraccionamiento propio a nuevos alumnos con buen historial de pago.")
T("S4. SI: la inflación de Lima supera 5,5%: renegociar los contratos de energía y servicios con tope de reajuste y escalonar los reajustes salariales de 2027; si vuelve al rango meta, aplicar el reajuste completo de pensiones a ingresantes.")
SUB("3. Comentarios Finales sobre el Entorno Macroeconómico 2026–2027")
T("C1. El entorno 2026-2028 es favorable para UCSUR en volumen: el sector de servicios, que incluye la educación, crecería 4,3% en 2026 y 3,7% en 2027, el desempleo de Lima está en 4,4% y el crédito de consumo crece 13,2%; con una elasticidad base de 4,0, los ingresos superarían S/1.000 millones en 2028.")
T("C2. El entorno es exigente en margen y cobranza: la inflación de oferta de 5,25% suma S/18,0 millones a los costos y reduce 4,0% el ingreso real de las familias, mientras las cuentas por cobrar ya crecieron 139% y una tasa real negativa anticipa un alza que encarecería el crédito de los estudiantes.")
T("C3. La principal decisión macroeconómica de UCSUR no es de deuda ni de cobertura, sino de precios y de cobranza: reajustar pensiones con la inflación esperada y trasladar el financiamiento de la matrícula al sistema financiero mientras la liquidez lo permita. Si lo hace, podrá mantener un margen operativo superior a 33% aun con inflación persistente y alza de tasas.")

H1("Referencias")
for ref in [
    "Banco Central de Reserva del Perú. (2026a, 18 de setiembre). Reporte de Inflación: Panorama actual y proyecciones macroeconómicas 2026-2027. Setiembre de 2026. https://www.bcrp.gob.pe/publicaciones/reporte-de-inflacion.html",
    "Banco Central de Reserva del Perú. (2026b). BCRPData: Series estadísticas [Base de datos]. Consultado el 11 de noviembre de 2026. https://estadisticas.bcrp.gob.pe",
    "Federal Reserve. (2026). Open market operations: Policy rate changes. https://www.federalreserve.gov/monetarypolicy/openmarket.htm",
    "Instituto Nacional de Estadística e Informática. (2023). Comportamiento de la economía peruana en el cuarto trimestre de 2022 (Informe Técnico PBI Trimestral). https://www.inei.gob.pe/media/MenuRecursivo/boletines/01-informe-tecnico-pbi-iv-trim-2022.pdf",
    "Instituto Nacional de Estadística e Informática. (2025). Compendio Estadístico Perú 2025. https://www.inei.gob.pe/media/MenuRecursivo/publicaciones_digitales/Est/Lib2025/libro.pdf",
    "Instituto Nacional de Estadística e Informática. (2026a). Comportamiento de la economía peruana en el primer trimestre de 2026 (Informe Técnico PBI Trimestral N.° 02). https://www.inei.gob.pe/media/MenuRecursivo/boletines/pbi-trimestral-i-trim-2026.pdf",
    "Instituto Nacional de Estadística e Informática. (2026b). Producción Nacional: julio 2026 (Boletín N.° 9). https://www.inei.gob.pe/media/MenuRecursivo/boletines/boletin-produccion-nacional-set2026.pdf",
    "Ministerio de Economía y Finanzas. (2026). Marco Macroeconómico Multianual 2027-2030. Lima: MEF. Cifras tomadas de Gestión, Forbes Perú y Energiminas (agosto-setiembre de 2026).",
    "Superintendencia Nacional de Educación Superior Universitaria. (2018). Resolución del Consejo Directivo N.° 039-2018-SUNEDU/CD. Lima: SUNEDU.",
    "Superintendencia Nacional de Educación Superior Universitaria. (2021). Resolución del Consejo Directivo N.° 052-2021-SUNEDU/CD. Lima: SUNEDU.",
    "Universidad Científica del Sur S.A.C. (2024). Estados financieros al 31 de diciembre de 2023 y de 2022, con el informe de los auditores independientes (28 de mayo de 2024). Lima.",
    "Universidad Científica del Sur S.A.C. (2025). Estados financieros al 31 de diciembre de 2024 y de 2023, junto con el dictamen de los auditores independientes. Tanaka, Valdivia, Arribas & Asociados (12 de junio de 2025). Lima.",
    "Universidad Científica del Sur S.A.C. (2026). Estados financieros al 31 de diciembre de 2025 y de 2024, junto con el informe de los auditores independientes. Tanaka, Valdivia, Arribas & Asociados (1 de junio de 2026). Lima.",
]:
    p = P(ref); p.paragraph_format.left_indent = Cm(1.27); p.paragraph_format.first_line_indent = Cm(-1.27)

doc.save(OUT)
print("saved", OUT)

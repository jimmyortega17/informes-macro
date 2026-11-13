import os, sys
S = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(S, "lib3.py"), encoding="utf-8").read())
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
import re as _re
_NC = [0]
def CADENA(titulo, elems, nota=None, fuente=None):
    _NC[0] += 1; titulo = f"Cadena {_NC[0]}. " + _re.sub(r"^Cadena \d+\.\s*", "", titulo)
    _CADENA(titulo, elems, None)
    p = doc.add_paragraph()
    if nota: run(p, nota + " ", True)
    run(p, "Fuente: " + (fuente or "BCRP; BCRPData; MINEM; EEFF estimados por el grupo."))

def IMGW(name, w=8.2):
    if name.startswith("i"): w = 8.8
    IMG(name, min(w, 8.8) / 2.54)
def AC(text):
    p = doc.add_paragraph(); run(p, "Análisis crítico — ", True); run(p, text)
def FORM(ecuacion, letras, reemplazo, resultado):
    EQ(ecuacion)
    p = doc.add_paragraph(); run(p, "Qué significa cada letra: ", True); run(p, letras)
    p = doc.add_paragraph(); run(p, "Reemplazo con cifras: ", True); run(p, reemplazo)
    p = doc.add_paragraph(); run(p, "Resultado y lectura para OCP: ", True); run(p, resultado)
_CNT = {"Tabla": 0, "Figura": 0, "Gráfico": 0, "Modelo": 0, "Diagrama": 0}
_CAP0 = CAP
def CAP(t):
    m = _re.match(r"^(Tabla|Figura|Gráfico|Modelo|Diagrama) \d+\.\s*", t)
    if m:
        k = m.group(1); _CNT[k] += 1; t = f"{k} {_CNT[k]}. " + t[m.end():]
    return _CAP0(t)
def RESET_TF(): _CNT["Tabla"] = 0; _CNT["Figura"] = 0
def CONJ(text):
    p = doc.add_paragraph(); run(p, "Conjetura del grupo — ", True, italic=True); run(p, text, italic=True)

EST = "EEFF estimados por el grupo (OCP_EEFF.xlsx)"

# ============ CARÁTULA ============
for txt in ("PONTIFICIA UNIVERSIDAD CATÓLICA DEL PERÚ", "ESCUELA DE POSGRADO"): P(txt, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = Pt(18)
p.add_run().add_picture(os.path.join(S, "logo", "word", "media", "image1.png"), width=Inches(3.0))
P("", after=40)
P("ANÁLISIS MACROECONÓMICO", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
P("OPERADORES CONCENTRADOS PERUANOS S.A.C. – MINA COBRIZA (RUC 20608321731)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=60)
P("PRESENTADO POR", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
P("[NOMBRE]", align=WD_ALIGN_PARAGRAPH.CENTER, after=30)
P("PROFESOR", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
P("Sergio Julio Chión Chacón", align=WD_ALIGN_PARAGRAPH.CENTER, after=90)
P("LIMA, NOVIEMBRE 2026", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

# ============ RESUMEN ============
H1("Resumen")
T("El entorno internacional de 2026 es el más favorable para un productor de concentrado de cobre de la última década, pero esa ventaja depende de China y de un precio que puede revertirse. El cobre promedió US$6,14 por libra entre enero y octubre, 36% más que en 2025, y la plata US$71,6 por onza, 79% más (BCRPData), porque la demanda de redes eléctricas e inteligencia artificial choca con una oferta de mina rígida: las fundiciones chinas aceptaron un cargo de tratamiento de US$0 en 2026. El mundo crecería 3,1% y China 4,5% (BCRP, RI setiembre 2026). En sentido contrario, la Fed subió su tasa a 3,75%–4,00% y el petróleo llegó a US$98,9 por barril, lo que encarece el diésel, los fletes y el capex importado. " + pgN("s1int"))
T("La economía peruana crece 3,2% en 2026 por la demanda interna, no por la minería, y esa combinación sube los costos locales de una mina sin elevar su producción. El PBI de minería metálica cayó 0,2% entre enero y agosto, después de crecer 10,9% en 2023, 3,2% en 2024 y 1,9% en 2025 (BCRPData), y el MEF espera 1,7% en 2026, 3,0% en 2027 y 1,5% en 2028 (MMM 2027-2030). Los términos de intercambio mejoran 18,1% y mantienen el sol en S/3,412. La inflación de Lima subió a 5,25% en octubre, sobre el rango meta, y la tasa real ex post es −1,00% con la referencia en 4,25%. Para OCP, que vende en dólares y paga cerca de 55% de su costo en soles, la inflación local y un sol fuerte se suman contra el margen. " + pgN("s1peru"))
T("Operadores Concentrados Peruanos S.A.C. (OCP), del Grupo Dyer Coriat, opera la mina subterránea Cobriza (Huancavelica), que compró en 2022 por US$22 millones y reinició en febrero de 2023 (437-461 trabajadores en planilla en 2025). Produjo 16.545 toneladas de cobre fino y 711 mil onzas de plata en 2025 (MINEM), 0,6% del cobre nacional, sin zinc ni oro. Vende concentrado en dólares a traders en el Callao, según la empresa Perubar (Glencore) y Mercuria; SUNAT no registra exportaciones a su nombre. Como no publica estados financieros, el grupo los estimó: ventas de US$176,6 millones, EBITDA de US$72,7 millones (41%) y utilidad neta de US$37,0 millones en 2025, con un capex de US$40 millones y deuda con vinculadas de US$45,6 millones. Recibe crédito de proveedores y de su grupo, no otorga crédito y tiene dos clientes grandes. " + pgN("s2desc"))
T("La incidencia más fuerte del entorno sobre OCP pasa por el precio del cobre y no por el PBI peruano. Las ventas tienen una elasticidad de 0,86 frente al precio del cobre, el EBITDA de 1,55 y la utilidad neta de 1,89, porque el costo por tonelada es casi fijo. Con cobre de US$5,70 (MMM), las ventas serían US$233 millones en 2027; con US$7,00 subirían a US$286 millones y con US$4,50 caerían a US$177 millones, con un EBITDA de US$164, US$117 y US$64 millones, respectivamente. El precio de equilibrio está en US$2,83 por libra. La inflación de 5,25% suma unos US$3,0 millones a los costos en soles; una depreciación de 10% añadiría US$4,5 millones al EBITDA y cada 25 pb de tasa apenas US$0,1 millones de intereses. Las cuentas por cobrar (US$14,5 millones) son de traders solventes y el riesgo está en la concentración de clientes. " + pgN("s2imp"))
T("La conclusión central es que OCP tiene hoy un margen extraordinario que no depende de su gestión sino de un ciclo de precios que el propio mercado considera transitorio: el MEF proyecta que el cobre baje de US$5,90 en 2026 a US$5,60 en 2028, y un enfriamiento de China lo llevaría cerca de US$4,50. La recomendación macroeconómica principal es fijar con sus compradores, mientras el cobre supere US$5,50 por libra, el precio de 30% a 40% de la producción de 2027 mediante coberturas o un contrato de compra anticipada con Glencore o Mercuria, y usar ese flujo para financiar la ampliación a 12.000 t/d sin deuda nueva. La meta es asegurar un EBITDA superior a US$80 millones en 2027 aunque se materialice el escenario bajo, frente a US$64 millones sin cobertura. " + pgN("s3"))

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

SUB("1. Crecimiento económico mundial y demanda de cobre")
T("El BCRP mantuvo en 3,1% el crecimiento mundial de 2026 y 2027, por debajo del 3,4% de 2025 (RI setiembre 2026); el MEF usa 3,0% y 3,2% (MMM 2027-2030, cuadro C-01). China, que compra más de la mitad del cobre refinado del mundo y es el destino final de casi todo el concentrado peruano, crecería 4,5% en 2026 y 4,2% en 2027, mientras Estados Unidos crecería 2,2%. La desaceleración es suave, pero el patrón del crecimiento favorece al cobre: la inversión en centros de datos, redes de transmisión, vehículos eléctricos y defensa usa más metal por dólar de PBI que la construcción residencial china, que fue el motor del ciclo anterior. Para OCP, que vende el 100% de su producción como concentrado de cobre con plata, el crecimiento mundial no le llega por el PBI peruano, sino directamente por el precio y por las condiciones que ponen los compradores.")
CAP("Gráfico 1. Crecimiento del PBI por Economía, 2025–2027 (var. % real)")
IMGW("g1.png")
SRC("BCRP, Reporte de Inflación setiembre 2026, con base en FMI y Consensus Forecast.")
INT("El gráfico 1 muestra que China crece 1,4 pp por encima del mundo en 2026 y que la brecha se reduce en 2027. Para el BCRP esa brecha sostiene los términos de intercambio; para OCP, cada décima menos de crecimiento chino es una presión a la baja sobre su precio de venta, sin que la empresa pueda compensarla con volumen.")
CADENA("Cadena 1. Crecimiento Mundial (Y*) → Precio del Cobre (Pcu) → Ventas de OCP",
       [("↑Y*", "Mundo 3,1%; China 4,5%"), ("↑D cobre", "Redes, IA, autos eléctricos"), ("S rígida", "TC/RC = US$0 (2026)"), ("↑Pcu", "US$4,51 → 6,14/lb"), ("↑Ventas OCP", "US$176,6 → 249,2 MM"), ("↑EBITDA", "41% → 55% de margen")],
       "Si crece la economía mundial con inversión intensiva en metales → sube la demanda de cobre frente a una oferta de mina que no responde → sube el precio → suben las ventas y, más que proporcionalmente, el EBITDA de OCP.")
CADENA("Cadena 2. Crecimiento Mundial (Y*) → Inflación (P) y Tasa de Interés (i): Ajuste hasta Y = Yn",
       [("↑Y*", "Inversión en IA y energía"), ("Y > Yn", "Brecha positiva en EE.UU."), ("↑P", "PCE EE.UU. 3,7%"), ("↓M/P", "Saldos reales a la baja"), ("↑i*", "Fed 3,75%–4,00%"), ("↓Y*", "China 4,2% en 2027; ↓Pcu")],
       "Si la demanda mundial empuja el producto por encima de su potencial → sube la inflación → caen los saldos reales → sube la tasa de interés → el crecimiento se modera hasta que Y = Yn. Para OCP, ese ajuste es el mecanismo que bajaría el cobre de US$6,14 a US$5,60 en 2028 (MMM).")

SUB("2. Precios internacionales de commodities: cobre, plata, zinc y petróleo")
T("El cobre LME promedió US$6,59 por libra en octubre de 2026 y US$6,14 entre enero y octubre, frente a US$4,51 en 2025 y US$3,85 en 2023 (BCRPData, PN01652XM). La plata pasó de US$23,4 a US$71,6 por onza entre 2023 y 2026 (PN01655XM), aunque en octubre ya había retrocedido a US$57,2 desde su pico de enero. El zinc subió 33%, a US$1,73 por libra en octubre (PN01657XM). El petróleo WTI llegó a US$98,9 por barril en octubre, frente a US$64,4 en febrero, por el conflicto en Medio Oriente (PN01660XM). El BCRP proyecta el cobre en US$6,15 en 2026 y US$6,38 en 2027; el MEF es más prudente, con US$5,90, US$5,70 y US$5,60 entre 2026 y 2028 (MMM 2027-2030, cuadro C-01). La plata es para OCP un crédito de subproducto que pasó de 10% a 19% de sus ingresos brutos estimados; el zinc no la afecta directamente, porque el MINEM no le registra producción de zinc, pero es un termómetro de la demanda industrial china.")
CAP("Gráfico 2. Cobre, Plata, Zinc y Petróleo, enero 2023 – octubre 2026 (índice ene-2023 = 100)")
IMGW("g2.png")
SRC("BCRPData, series PN01652XM, PN01655XM, PN01657XM y PN01660XM (consulta del 13 de noviembre de 2026).")
INT("El gráfico 2 muestra que el cobre (índice 162) y la plata (241) se separaron del petróleo (126) y del zinc (117) desde 2025. Para el Perú esa separación es un aumento del ingreso nacional; para OCP es un margen que crece porque sus dos productos suben más que su principal insumo importado, el combustible.")
CAP("Modelo 1. Mercado Internacional del Cobre: Expansión de la Demanda con Oferta Rígida, 2025–2026")
IMGW("m1.png", 6.6)
SRC("BCRPData (precio promedio 2025 y enero-octubre 2026); BCRP, RI setiembre 2026. Diagrama conceptual con precios observados.")
INT("El modelo 1 muestra que la demanda se desplazó de D₀ a D₁ y, con una oferta poco elástica (nuevas minas tardan diez años), el equilibrio pasó de E₀ (US$4,51) a E₁ (US$6,14), +36%. El cargo de tratamiento de US$0 en 2026 (y negativo en el mercado spot, hasta −US$125 por tonelada en junio) indica que el cuello de botella está en la mina y no en la fundición. Para OCP, esa escasez de concentrado vale doble: sube el precio y mejora los términos de venta.")
CADENA("Cadena 3. Petróleo (Poil) → Inflación (P) → Costos Mineros de OCP",
       [("↑Poil", "WTI US$64,4 → 98,9"), ("↑Diésel", "Flota y generación"), ("↑Fletes", "Mina → Callao ~480 km"), ("↑π", "Lima 5,25% (oct-26)"), ("↑Costo/t", "US$52 → 56/t (2026P)"), ("↓Margen", "Amortiguado por Cu +36%")],
       "Si sube el petróleo → suben el diésel, los fletes y la inflación local → sube el costo por tonelada de OCP; mientras el cobre suba más que el petróleo, el margen se mantiene, pero el costo no baja cuando el cobre caiga.")

SUB("3. Desempeño de Operadores Concentrados Peruanos S.A.C. – Cobriza, 2023–2026")
T("OCP reinició Cobriza en febrero de 2023, después de doce años de liquidación de Doe Run Perú, y la llevó de 10 toneladas de cobre fino ese mes a 1.250 toneladas mensuales a fin de año (MINEM). Produjo 8.351 toneladas de cobre fino en 2023, 14.791 en 2024 (+77,1%) y 16.545 en 2025 (+11,9%); entre enero y agosto de 2026 produjo 10.528 toneladas, 3,2% menos que un año antes, con un febrero débil (904 toneladas). La plata pasó de 346 mil a 711 mil onzas entre 2023 y 2025, y en julio de 2025 el BCRP atribuyó a OCP el alza de 11,7% del cobre de Huancavelica (BCRP, 2025). Como la empresa no publica estados financieros, el grupo estimó (tabla 6 de la Sección 2): ventas de US$68,2, US$134,5 y US$176,6 millones entre 2023 y 2025, y US$249,2 millones en 2026P; EBITDA de US$5,3, US$45,2, US$72,7 y US$136,0 millones.")
CAP("Gráfico 3. Producción Mensual de Cobre y Plata de OCP – Cobriza, enero 2023 – agosto 2026")
IMGW("g3.png")
SRC("MINEM, Producción Minera por titular y unidad (archivos 2023, 2024, 2025 y enero-agosto 2026), unidad «Expansión Cobriza».")
INT("El gráfico 3 muestra que el volumen creció hasta 2025 y se estancó en 2026, mientras las ventas estimadas siguieron subiendo por el precio. La lectura macro es central para todo el informe: desde 2026 el resultado de OCP depende del cobre y no de su producción; el margen EBITDA pasó de 41% a 55% sin que la mina produjera más.")
CADENA("Cadena 4. Precio del Cobre (Pcu) y Volumen (Q) → Margen de OCP",
       [("↑Q", "8.351 → 16.545 TMF"), ("↓Costo unitario", "C1 US$3,49 → 2,32/lb"), ("↑Pcu", "+36% (2026)"), ("Q estable", "−3,2% (ene-ago 26)"), ("↑Margen", "EBITDA 41% → 55%"), ("↑Utilidad", "US$37,0 → 75,1 MM")],
       "Si sube el volumen en una mina de costos fijos → baja el costo por libra; si después sube el precio con volumen estable → el margen crece por precio. La primera fuente es gestión; la segunda es macroeconomía y puede revertirse.",
       "MINEM; BCRPData; " + EST + ".")

SUB("4. Política monetaria global y tipo de cambio")
T("La Reserva Federal subió su tasa 25 pb el 17 de setiembre de 2026, a 3,75%–4,00%, después de haberla recortado a 3,50%–3,75% en diciembre de 2025, porque la inflación PCE de 2026 llegaría a 3,7% (Federal Reserve, 2026; BCRP, RI setiembre 2026). Con el BCRP en 4,25% desde setiembre de 2025, el diferencial frente al punto medio de la Fed bajó a 0,375 pp. El sol no se debilitó: cotizó S/3,412 el 9 de noviembre, frente a S/3,367 en diciembre de 2025 y a S/3,568 de promedio en 2025 (BCRPData, PN01210PM y PD04638PD), porque el superávit comercial y las compras del BCRP compensan el menor atractivo de las tasas. ")
FORM("Paridad de tasas: i = i* + (depreciación esperada + riesgo país)",
     "i = tasa de interés en soles (BCRP); i* = tasa de interés en dólares (Fed); el paréntesis es lo que un inversionista exige por pasar de dólares a soles.",
     "4,25% = 3,875% + (depreciación esperada + riesgo país)  →  depreciación esperada + riesgo país = 4,25% − 3,875% = 0,375 pp.",
     "el premio por invertir en soles es casi nulo; el sol no se sostiene por las tasas sino por los dólares del cobre. Si el cobre baja, el sol puede depreciarse, lo que a OCP le conviene porque vende en dólares.")
CAP("Gráfico 5. Tasa de Referencia del BCRP y Tasa de la Fed, enero 2024 – octubre 2026 (%)")
IMGW("g4.png")
SRC("BCRPData, serie PD04722MM; Federal Reserve (2026), cambios de la tasa de política (punto medio del rango).")
CAP("Modelo 2. Mercado Cambiario: Oferta y Demanda de Dólares, 2025 – noviembre 2026")
IMGW("m2.png", 6.6)
SRC("BCRPData; BCRP, RI setiembre 2026. Diagrama conceptual con valores observados.")
INT("El modelo 2 muestra que las exportaciones mineras desplazan la oferta de dólares de S$₀ a S$₁ y llevan el equilibrio de E₀ (S/3,568, promedio de 2025) a E₁ (S/3,412). La paradoja para OCP es que el mismo cobre caro que eleva sus ventas aprecia el sol y encarece sus costos en soles: parte de su ganancia de precio la devuelve por el tipo de cambio.")
CADENA("Cadena 5. Tasa de la Fed (i*) → Tipo de Cambio (E) → Costos en Dólares de OCP",
       [("↑i*", "Fed 3,75%–4,00%"), ("↓(i − i*)", "0,375 pp"), ("↑Superávit externo", "US$48.865 MM"), ("↓E", "S/3,568 → 3,412"), ("↑Costo en US$", "~55% del costo en soles"), ("↓Margen OCP", "−US$4,5 MM por 10% de TC")],
       "Si la Fed sube la tasa pero el superávit minero domina el mercado cambiario → el sol se aprecia → los costos en soles de OCP suben medidos en dólares → se reduce parte del margen que dio el precio del cobre.")

SUB("5. Economía de Estados Unidos, inflación importada y costo del capex importado")
T("OCP no importa insumos operativos: el registro de aduanas muestra 168 declaraciones de importación por US$7,27 millones CIF entre 2023 y noviembre de 2026, todas de bienes de capital y repuestos (Veritrade, con datos de SUNAT). Lo principal son filtros prensa de Italia para el tratamiento de agua y relaves (US$4,41 millones), una bomba de relleno en pasta de Alemania (US$1,15 millones), partes de chancado y molienda (US$0,79 millones) y un topador de ruedas (US$0,32 millones). El 77% vino de Italia y Alemania y se paga en dólares o euros; el resto, de Estados Unidos, Canadá y China. Con una inflación PCE de 3,7% en Estados Unidos y el euro fortalecido, el costo de reposición de ese capex sube aunque el sol esté estable.")
FORM("Costo en soles de un equipo importado = P* × (1 + π*) × E",
     "P* = precio del equipo en dólares; π* = inflación de EE.UU.; E = tipo de cambio (soles por dólar).",
     "equipo de US$1 millón: 1 × (1 + 0,037) × 3,412 = S/3,538 millones, frente a 1 × 3,367 = S/3,367 millones en diciembre de 2025.",
     "el mismo equipo cuesta 5,1% más en soles aunque el sol casi no se movió; casi todo el aumento viene de la inflación externa. OCP debe presupuestar su capex importado con esa inflación.")
CAP("Gráfico 6. Importaciones de OCP por Año y País de Origen, 2023–2026 (US$ millones CIF)")
IMGW("g5.png")
SRC("Veritrade, registro de declaraciones de importación del RUC 20608321731 (base SUNAT), enero 2019 – noviembre 2026. * 2026: enero-noviembre.")
INT("El gráfico 5 muestra que el capex importado se multiplicó por 18 entre 2024 y 2025 y casi se duplicó en 2026, en línea con el informe técnico sustentatorio de agua y relaves (US$8,25 millones) y con la ampliación de la planta. Para OCP, la inflación de EE.UU. y de Europa es un costo de inversión, no de operación: los insumos de la operación diaria se compran a proveedores locales.")
CADENA("Cadena 6. Inflación de EE.UU. y Europa (π*) → Tipo de Cambio (E) → Capex de OCP",
       [("↑π*", "PCE EE.UU. 3,7%"), ("↑i*", "Fed 3,75%–4,00%"), ("E estable", "S/3,412"), ("↑P* × E", "Equipo +5,1% en S/"), ("↑Capex importado", "US$2,53 → 4,59 MM"), ("↓Flujo libre", "US$50,9 MM (2026P)")],
       "Si sube la inflación de EE.UU. y Europa → la Fed mantiene tasas altas → aunque el sol se mantenga estable, sube el costo de los equipos → crece el capex importado → se reduce el flujo libre de OCP.",
       "Veritrade/SUNAT; BCRPData; BCRP, RI setiembre 2026; " + EST + ".")
CAP("Diagrama 1. Ishikawa de Factores Internacionales que Afectan a OCP – Cobriza, 2026–2027")
IMGW("i1.png")
SRC("BCRP, RI setiembre 2026; BCRPData; Federal Reserve (2026); Veritrade/SUNAT. Diagrama conceptual.")
CRIT("el entorno internacional le entrega a OCP un margen que no se explica por su eficiencia. Entre 2025 y 2026 la producción de cobre de Cobriza cayó 3,2%, pero las ventas estimadas subieron 41% porque el cobre subió 36% y la plata 79%. Ese resultado descansa en tres supuestos frágiles. Primero, que China siga creciendo cerca de 4,5%: el BCRP ya proyecta 4,2% para 2027. Segundo, que la escasez de concentrado persista: un cargo de tratamiento de US$0 es históricamente anómalo y las fundiciones chinas están perdiendo dinero, por lo que reducirán su producción o subirán los cargos. Tercero, que la Fed no fuerce un dólar más fuerte: con la PCE en 3,7%, un nuevo alza encarecería el dólar y suele bajar los metales. El petróleo en US$98,9, en cambio, sí se trasladó a costos. La conjetura del grupo es que el ciclo de precios de 2026 es el pico y no el nuevo piso: el MEF ya proyecta US$5,60 en 2028, 9% menos que el promedio de 2026, y el escenario bajo de US$4,50 solo requiere que China vuelva a crecer cerca de 4%, que es su tendencia.")
ESTR("OCP debe convertir parte de un precio extraordinario en flujo asegurado antes de que el ciclo cambie. Con el cobre sobre US$6,00, fijar el precio de 30% a 40% de la producción de 2027 (unas 6.000 toneladas) mediante un contrato de compra anticipada o una cobertura con su comprador le aseguraría unos US$75 millones de ingresos aunque el cobre caiga a US$4,50, porque cada dólar por libra sobre 6.000 toneladas vale US$13 millones. El costo es renunciar al alza si el cobre sube a US$7,00, pero el riesgo es asimétrico: en el escenario alto el EBITDA de 2027 sería US$151 millones con cobertura frente a US$164 millones sin ella, y en el bajo subiría de US$64 a US$83 millones gracias a ella. Al mismo tiempo, debe negociar con Glencore o Mercuria un cargo de tratamiento plurianual cercano a cero mientras el mercado spot sea negativo, y comprar en 2027 el equipamiento europeo pendiente de la ampliación, porque el euro y la inflación de EE.UU. lo encarecen cada trimestre que se posterga.")

H2("Situación macroeconómica del Perú y perspectivas 2025–2027: Dependencia de Operadores Concentrados Peruanos S.A.C. del entorno nacional"); MARK("s1peru")

SUB("1. PBI sectorial con énfasis en minería metálica, sector clave de OCP")
T("El PBI peruano creció 3,4% en 2025 y crecería 3,2% en 2026 y 3,0% en 2027 según el BCRP (RI setiembre 2026), y 3,40%, 3,44% y 3,96% entre 2026 y 2028 según el MEF (MMM 2027-2030, cuadro C-01), que se usa como referencia oficial para 2028. El PBI que importa para OCP es el de minería metálica: creció 10,9% en 2023 por el arranque de Quellaveco, 3,2% en 2024 y 1,9% en 2025, y cayó 0,2% entre enero y agosto de 2026 (BCRPData, índice PN01760AM), con agosto en −6,1%. El MEF proyecta 1,68% en 2026, 3,02% en 2027 y 1,46% en 2028 (cuadro C-02). El crecimiento de 2026 es de demanda interna: la inversión privada crecería 14,0% y la construcción 9,5%, mientras la minería se estanca. OCP, en cambio, pasó de 0,30% del cobre nacional en 2023 a 0,60% en 2025, con un volumen que creció 77,1% en 2024 y 11,9% en 2025 y cayó 3,2% entre enero y agosto de 2026.")
FORM("PBI = C + I + G + (X − M)",
     "C = consumo de las familias; I = inversión de las empresas y del Estado (más inventarios); G = consumo del gobierno; X = exportaciones; M = importaciones. Cada término se expresa como su aporte en puntos al crecimiento de 2026.",
     "3,20% = 2,36 (C) + 2,87 (inversión privada) + 0,06 (inversión pública) + 0,70 (inventarios) + 0,45 (G) + 0,03 (X) − 3,27 (M), con las ponderaciones reales de 2025 (BCRPData, PN02528AQ a PN02537AQ).",
     "la suma cuadra con el 3,2% del BCRP y muestra que las exportaciones en volumen aportan apenas 0,03 pp: el auge del cobre llega al PBI por precios e inversión, no por más toneladas. Para OCP, su sector no lidera el crecimiento, pero sí lo financia: la inversión privada (+14,0%) incluye la ampliación de minas como Cobriza.")
T("La política fiscal acompaña poco. El consumo público (G) crecería 3,2% en 2026 y 2,3% en 2027 según el BCRP, y apenas 2,94% en 2026 y 0% en 2027 y 2028 según el MEF, que reduce el déficit fiscal de 1,76% a 1,02% del PBI entre 2026 y 2028, con una deuda pública de 29,3% del PBI (MMM 2027-2030, cuadro C-01). La política monetaria, en cambio, sigue holgada (tasa de 4,25% con inflación de 5,25%). El comportamiento de los agentes explica el resto: los inversionistas privados responden al cobre caro con una inversión que crece 14,0% (10,5% según el MEF) y los consumidores mantienen un gasto de 3,6% pese a la caída del salario real. Para OCP, la consolidación fiscal importa por la regalía y el IEM: con el cobre alto, el Estado recauda más de la minería. El MEF y la SUNAT no publican la regalía ni el IEM por empresa, de modo que el monto de OCP es una estimación del grupo (US$9,6 millones en 2026P) y ese ingreso le permite reducir el déficit sin subir impuestos.")
CAP("Gráfico 7. PBI Total y Minería Metálica, 2022–2028P (var. % real)")
IMGW("g6.png")
SRC("BCRPData (PN01728AM y PN01760AM); MEF, MMM 2027-2030, cuadros C-01 y C-02 (2027P-2028P). * 2026: enero-agosto.")
INT("El gráfico 6 muestra que la minería metálica pasó de liderar el crecimiento en 2023 a restarle en 2026. Para OCP, cuya producción depende de su propia mina y no del ciclo nacional, el PBI minero es un indicador de competencia por equipos, contratistas y permisos, no de demanda: sus ventas no dependen del PBI peruano.")
CAP("Modelo 3. Oferta Agregada y Demanda Agregada: Perú 2025–2026")
IMGW("m3.png", 6.6)
SRC("BCRP, RI setiembre 2026; BCRPData. Diagrama conceptual con cifras observadas y proyectadas.")
INT("El modelo 3 muestra que la demanda agregada se desplazó a la derecha por la inversión y el ingreso minero, y la oferta a la izquierda por el petróleo, El Niño y una minería estancada: el equilibrio pasa de E₀ (π 1,5%; PBI 3,4%) a E₁ (π 5,25%; PBI 3,2%). Para OCP, OA₁ significa costos locales más altos sin más producción.")
CADENA("Cadena 7. Términos de Intercambio (TI) → Demanda Interna (DA) → Costos Locales de OCP",
       [("↑TI", "+18,1% (2026)"), ("↑Ingreso nacional", "Superávit US$48.865 MM"), ("↑DA", "Inversión privada +14,0%"), ("Y minero estancado", "−0,2% (ene-ago 26)"), ("↑P", "π 5,25%"), ("↑Costos OCP", "Contratistas y servicios")],
       "Si mejoran los términos de intercambio → sube el ingreso nacional y la demanda interna → con una oferta minera estancada, suben los precios locales → suben los costos de contratistas y servicios de OCP.")

SUB("2. Inflación y costos de la operación minera")
T("La inflación de Lima llegó a 5,25% en octubre de 2026, con 0,57% mensual y 4,88% acumulado en el año (INEI, vía BCRPData, PN01273PM). Su origen es de oferta: combustibles, tarifas eléctricas, pasajes y El Niño; la inflación sin alimentos ni energía era 1,8% en setiembre (RI setiembre 2026). El RI proyectó 4,2% para diciembre; para cumplirlo, noviembre y diciembre deberían sumar −0,65%, lo que es improbable, de modo que 2026 cerraría sobre 5%. Las expectativas a 12 meses están en 3,05% (PD12912AM) y el MEF espera 2,53% en 2027 y 2,50% en 2028. Para OCP la inflación relevante es la de sus insumos locales: diésel, explosivos, reactivos, bolas de molienda, energía y mano de obra.")
FORM("Inflación que faltaría en noviembre-diciembre = (1 + meta del año) / (1 + inflación acumulada a octubre) − 1",
     "la meta del año es la proyección del RI para diciembre (4,2%); la inflación acumulada es la de enero a octubre (4,88%).",
     "(1 + 0,042) / (1 + 0,0488) − 1 = −0,65%.",
     "harían falta dos meses de deflación para cumplir la proyección, lo que no ocurre desde hace años: 2026 cerraría sobre 5%. Para OCP, los reajustes de 2027 de sus contratistas y de su convenio colectivo partirán de una inflación de 5%, no de 4,2%.")
CAP("Gráfico 8. Inflación en Lima Metropolitana y Expectativas, enero 2025 – octubre 2026 (%)")
IMGW("g7.png")
SRC("BCRPData, series PN01273PM y PD12912AM; BCRP, RI setiembre 2026.")
INT("El gráfico 7 muestra que la inflación salió del rango meta en marzo y no volvió, mientras las expectativas suben a 3,05%. Para el BCRP es una señal de alza de tasas; para OCP es un aumento de costo que no puede trasladar, porque su precio de venta lo fija la LME y no el mercado peruano.")
CADENA("Cadena 8. Inflación (P) → Salarios (w) → Costo por Tonelada de OCP",
       [("↑P", "π 5,25% (oct-26)"), ("↑Insumos locales", "Diésel, explosivos, reactivos"), ("↑w", "437-461 en planilla"), ("↑Costo/t", "US$52 → 56/t"), ("Precio LME", "No se traslada"), ("↓Margen", "−US$1,0 MM por 1 pp")],
       "Si sube la inflación → suben los insumos locales y los salarios → sube el costo por tonelada → como el precio de venta lo fija la LME, OCP absorbe todo el aumento en su margen.")

SUB("3. Tipo de cambio y su efecto sobre ventas y costos")
T("El sol cotizó S/3,412 por dólar el 9 de noviembre de 2026, apenas 1,3% por encima del promedio de diciembre de 2025, después de apreciarse 10,2% en 2025 (BCRPData). El BCRP compró US$15.715 millones en 2026 para moderar la apreciación, y el MEF proyecta un tipo de cambio promedio de S/3,39 en 2026, S/3,35 en 2027 y S/3,37 en 2028 (MMM 2027-2030, cuadro C-01). OCP tiene una exposición opuesta a la de una empresa importadora: vende 100% en dólares y, según el supuesto del grupo, paga cerca de 55% de su costo operativo en soles (planilla, contratistas, energía e insumos locales). Por eso un sol fuerte la perjudica y un sol débil la favorece.")
CAP("Gráfico 9. Tipo de Cambio Sol/Dólar, enero 2025 – noviembre 2026")
IMGW("g8.png")
SRC("BCRPData, series PN01210PM (promedio mensual bancario) y PD04638PD (interbancario venta, 9 de noviembre de 2026).")
INT("El gráfico 8 muestra que el sol se movió en una banda de S/3,36 a S/3,45 en 2026, después de una apreciación de casi 40 céntimos en 2025. Para el BCRP, esa estabilidad ancla las expectativas; para OCP, la apreciación de 2025 equivale a un alza de 4,6% de sus costos en soles medidos en dólares.")
CADENA("Cadena 9. Precio del Cobre (Pcu) → Tipo de Cambio (E) → Margen de OCP",
       [("↑Pcu", "US$6,14/lb"), ("↑Exportaciones", "US$119.876 MM"), ("↑Oferta de US$", "Compras BCRP US$15.715 MM"), ("↓E", "S/3,568 → 3,412"), ("↑Costo en US$", "~55% del costo en soles"), ("↓Margen OCP", "Se devuelve parte del precio")],
       "Si sube el cobre → aumentan las exportaciones y la oferta de dólares → el sol se aprecia → los costos en soles de OCP suben medidos en dólares → la mina devuelve una parte de la ganancia de precio por el tipo de cambio.")

SUB("4. Empleo, salarios y relación con la comunidad")
T("La tasa de desempleo de Lima Metropolitana bajó de 5,7% a 4,4% entre los trimestres móviles terminados en setiembre de 2025 y de 2026, y el ingreso promedio mensual fue S/2.302, apenas 0,35% más que un año antes, lo que equivale a una caída real de 4,0% (INEI, vía BCRPData, PN38063GM y PN38070GM). En Huancavelica, una de las regiones más pobres del país, OCP es el principal empleador formal privado de su zona: recontrató a 604 trabajadores de Doe Run en 2022 (Proactivo, 2022) y en 2025 su planilla propia osciló entre 437 y 461 trabajadores mensuales (datosperu.org), cifra que puede excluir a contratistas. El empleo minero tiene dos efectos sobre la empresa: la inflación presiona los reajustes del convenio colectivo y la participación de los trabajadores en las utilidades (8%) sube con el precio del cobre: el grupo la estima en US$4,6 millones en 2025 y US$9,3 millones en 2026P.")
FORM("Curva de Phillips simple: π = πᵉ − β × (u − u*)",
     "π = inflación; πᵉ = inflación esperada; u = tasa de desempleo; u* = desempleo «normal» o natural, que no presiona precios; β = cuánto sube la inflación por cada punto que el desempleo baja de su nivel normal.",
     "πᵉ = 3,05% (BCRPData); u = 4,4% (Lima, setiembre 2026); u* = 6,0% y β = 0,5 (supuestos del grupo, cercanos al desempleo de Lima antes de la pandemia)  →  π = 3,05% − 0,5 × (4,4% − 6,0%) = 3,05% + 0,8% = 3,85%.",
     "el mercado laboral apretado explica una inflación de demanda de 3,85%; la diferencia con la observada (5,25%), unos 1,4 pp, viene del choque de oferta (petróleo y El Niño). Para OCP, la parte laboral es la más persistente: un desempleo bajo sostiene los reclamos salariales en la mina aunque el petróleo baje.")
CAP("Gráfico 10. Desempleo e Ingreso Promedio en Lima Metropolitana, enero 2025 – setiembre 2026")
IMGW("g12.png")
SRC("BCRPData, series PN38063GM, PN38066GM y PN38070GM (promedio móvil de tres meses), con datos del INEI.")
INT("El gráfico 9 muestra más empleo y menos poder de compra. Para OCP, con una planilla que es parte fija de su costo, la pérdida de salario real presiona el reajuste del convenio colectivo justo cuando el cobre eleva las utilidades que ven sus trabajadores y la comunidad.")
CADENA("Cadena 10. Inflación (P) → Salario Real (w/P) → Costo Laboral y Conflictividad de OCP",
       [("↑P", "π 5,25%"), ("↓w/P", "Ingreso real −4,0%"), ("↑Reajuste", "Convenio colectivo"), ("↑Pcu", "Utilidad US$75,1 MM (2026P)"), ("↑Participación 8%", "US$9,3 MM (2026P)"), ("↑Expectativas locales", "Huancavelica")],
       "Si la inflación baja el salario real mientras el cobre eleva las utilidades → los trabajadores y la comunidad exigen una mayor participación del auge → suben el costo laboral y el riesgo de conflicto de OCP.")

SUB("5. Términos de intercambio peruanos y contexto del sector minero del cobre")
T("Los términos de intercambio crecerían 18,1% en 2026 según el BCRP (16,7% según el MEF) y alcanzarían su máximo histórico, porque el índice de precios de exportación sube 23,9% y el de importación 6,2% (MMM 2027-2030, cuadro C-01). Las exportaciones sumarían US$119.876 millones y las importaciones US$71.011 millones, con un saldo comercial de US$48.865 millones (12,1% del PBI) y un superávit en cuenta corriente de 4,0% del PBI (RI setiembre 2026). El cobre es el primer producto de exportación: sus ventas al exterior crecieron 19,3% en 2025, a US$28.130 millones (MINEM). En ese mercado OCP es un productor pequeño (0,6% del cobre nacional) que no exporta directamente: SUNAT no registra exportaciones con su RUC, porque vende el concentrado en el Callao a traders que figuran como exportadores.")
FORM("Balanza de pagos: BP = CA + KA + ER",
     "CA = cuenta corriente (exportaciones menos importaciones, rentas y transferencias); KA = cuenta financiera o de capitales (entradas menos salidas de inversión y préstamos); ER = errores y omisiones. Si BP es positivo, el BCRP acumula reservas.",
     "CA = +4,0% del PBI (RI setiembre 2026). Como el BCRP compró US$15.715 millones y las reservas llegaron a US$96.668 millones (BCRPData, 9 de noviembre), la entrada neta de dólares por la cuenta corriente supera la salida neta de capitales: BP > 0.",
     "al país le sobran dólares, y por eso el sol se mantiene fuerte. Para OCP, esas reservas reducen el riesgo de una depreciación brusca que le favorecería y sostienen un sol que le resta margen en sus costos en soles.")
T("La relación también opera en sentido inverso, de la economía doméstica a la mundial: el Perú produce cerca de 12% del cobre de mina del mundo, de modo que una paralización de grandes minas peruanas por conflictos, como las de Las Bambas en años anteriores, reduce la oferta mundial y sube el precio. Para OCP, que produce poco, un conflicto en otra mina peruana es paradójicamente una buena noticia de precio; un conflicto en Cobriza, en cambio, le resta toda su producción sin mover el precio.")
CAP("Gráfico 11. Balanza Comercial del Perú, 2025–2027 (US$ miles de millones)")
IMGW("g9.png")
SRC("BCRP, Reporte de Inflación setiembre 2026, cuadro de balanza comercial.")
INT("El gráfico 10 muestra que el saldo comercial sube de US$35.433 millones en 2025 a US$48.865 millones en 2026 y se mantiene en 2027. Para el país es ingreso disponible y estabilidad cambiaria; para OCP, una señal de que el mercado ya incorporó el precio alto del cobre y de que el ajuste vendrá por el precio, no por el volumen.")
CADENA("Cadena 11. Términos de Intercambio (TI) → Balanza de Pagos (BP) → Tipo de Cambio (E) → OCP",
       [("↑TI", "+18,1% (2026)"), ("↑CA", "+4,0% del PBI"), ("↑Oferta de US$", "Saldo US$48.865 MM"), ("↑RIN", "US$96.668 MM"), ("E estable/↓", "S/3,40–3,45"), ("Ventas en S/ ↓", "Costos en S/ ↑ en US$")],
       "Si mejoran los términos de intercambio → sube el superávit en cuenta corriente → entran dólares y el BCRP acumula reservas → el sol se mantiene fuerte → el ingreso en soles de OCP crece menos que su precio en dólares.")

SUB("6. Crédito, liquidez y financiamiento de la inversión minera")
T("La liquidez en soles de las sociedades de depósito creció 16,7% interanual en setiembre de 2026 (BCRPData, PN00189MM) y el crédito al sector privado 10,3%. Una mediana minera como OCP no se financia en ese mercado: sus fuentes son el aporte de su grupo, los préstamos de empresas vinculadas y los prepagos de sus compradores, que adelantan dinero a cambio de concentrado futuro y cobran una tasa ligada a la SOFR. Mercuria, por ejemplo, colocó cerca de US$2.000 millones en acuerdos de concentrado de cobre en 2025, varios con prepago (Mining.com, 2025). El grupo estima que OCP necesitó US$48 millones de financiamiento en 2023-2024 para un capex de US$75 millones, y que la deuda llegó a US$51,3 millones en 2024 antes de bajar a cero en 2026P. La teoría cuantitativa permite leer el exceso de liquidez local:")
FORM("Teoría cuantitativa del dinero: M × V = P × Y  (en variaciones: %ΔM + %ΔV = %ΔP + %ΔY)",
     "M = cantidad de dinero (liquidez en soles); V = velocidad, es decir, cuántas veces circula cada sol; P = nivel de precios; Y = producción real.",
     "16,7% (liquidez, setiembre 2026) + %ΔV = 4,5% (inflación de setiembre) + 3,2% (PBI 2026P)  →  %ΔV = 7,7% − 16,7% = −9,0%.",
     "hay más dinero del que la economía usa: el exceso está guardado (la velocidad cae). Si las expectativas suben, ese dinero se gasta y presiona precios; por eso el BCRP tenderá a subir la tasa.")
CAP("Gráfico 12. Liquidez en Soles e Inflación, enero 2025 – octubre 2026 (var. % 12 meses)")
IMGW("g10.png")
SRC("BCRPData, series PN00189MM y PN01273PM; BCRP, RI setiembre 2026.")
INT("El gráfico 11 muestra que la liquidez crece 16,7% frente a una inflación de 5,25% y un PBI de 3,2%. La diferencia es dinero ocioso que el BCRP probablemente retirará con tasas más altas en 2027, lo que encarecerá el crédito de los contratistas mineros.")
CADENA("Cadena 12. Dinero (M) → Inflación (P) → Tasa (i) → Costo de los Contratistas de OCP",
       [("↑M", "Liquidez +16,7%"), ("↓V", "−9,0%"), ("↑P", "π 5,25%"), ("↑i (riesgo)", "4,25% → 4,50%"), ("↑Costo del crédito", "Contratistas locales"), ("↑Tarifas", "Servicios mineros de OCP")],
       "Si la liquidez crece más que la economía → presiona los precios → el BCRP sube la tasa → se encarece el crédito de los contratistas → lo trasladan a sus tarifas → sube el costo de los servicios mineros de OCP.")

SUB("7. Tasa de interés, ciclo de efectivo y capital de trabajo")
T("El BCRP mantiene su tasa de referencia en 4,25% desde setiembre de 2025 (PD04722MM). Con expectativas de inflación de 3,05% y una inflación observada de 5,25%, la tasa real es positiva ex ante y negativa ex post:")
FORM("Ecuación de Fisher: i = r + π   →   r = i − π",
     "i = tasa de interés nominal (la de referencia del BCRP); r = tasa de interés real, lo que gana de verdad quien presta; π = inflación (esperada para el cálculo ex ante, observada para el ex post).",
     "r ex ante = 4,25% − 3,05% = 1,20%;   r ex post = 4,25% − 5,25% = −1,00%.",
     "con la inflación de hoy, prestar en soles hace perder poder de compra: la política monetaria es estimulante. Para OCP, que se financia en dólares, el efecto directo es pequeño, pero la tasa real negativa empuja el gasto, la inflación y sus costos locales.")
T("La regla de Taylor, en su forma simple, indica qué tasa debería tener el banco central según la inflación y el uso de la capacidad de la economía:")
FORM("Regla de Taylor simple: i = r* + π + 0,5 × (π − π*) + 0,5 × (brecha del producto)",
     "i = tasa de referencia sugerida; r* = tasa real neutral (ni estimula ni frena), 1,75%; π = inflación; π* = meta del BCRP, 2%; brecha del producto = cuánto se aleja el PBI de su potencial (positiva si la economía está «caliente»).",
     "con la inflación observada (5,25%) y una brecha del producto de cero (supuesto del grupo): 1,75% + 5,25% + 0,5 × (5,25% − 2%) + 0,5 × 0 = 8,6%. Con la inflación esperada (3,05%): 1,75% + 3,05% + 0,5 × 1,05% + 0 = 5,3%.",
     "en ambos casos la tasa sugerida supera el 4,25% del BCRP, de modo que la política está holgada. El BCRP prefiere mirar la inflación esperada porque el choque es de oferta, pero aun así le faltan unos 100 pb: el escenario más probable para 2027 es un alza gradual. Para OCP, un alza encarece a sus proveedores locales y puede apreciar el sol.")
T("Para el BCRP, una tasa real ex post negativa con inflación fuera del rango meta justifica un alza de 25 pb. Para OCP, el ciclo de efectivo es corto y está en dólares: el comprador paga cerca de 90% del valor provisional al embarque y liquida el saldo uno a tres meses después, con el precio del periodo de cotización. El grupo estima cuentas por cobrar de 30 días (US$14,5 millones en 2025), inventarios de 30 días de costo y cuentas por pagar de 45 días: el capital de trabajo neto es pequeño y la tasa de interés local casi no lo afecta.")
CAP("Modelo 4. IS-MP: Inversión Minera, Tasa Real y Producto, 2026")
IMGW("m5.png", 6.6)
SRC("BCRPData (tasa de referencia y expectativas, octubre de 2026); BCRP, RI setiembre 2026. Diagrama conceptual.")
INT("El modelo 4 muestra la IS desplazada a la derecha (IS₁) por la inversión minera y el crédito, con la regla monetaria en r = 1,20% (E₁). Si el BCRP sube 25 pb, la MP pasa a MP₁ y el producto se modera en E₂. Para OCP el efecto directo es pequeño: su financiamiento está en dólares y depende de la Fed y de sus compradores, no del BCRP.")
CADENA("Cadena. Tasa de Interés (i) → Inversión y Consumo → PBI (Y)",
       [("↑i", "4,25% → 4,50% (escenario)"), ("↑r", "−1,00% → −0,75%"), ("↓I privada", "+14,0% → +8,5% (2027)"), ("↓C", "3,6% → 3,0%"), ("↓DA", "Demanda interna"), ("↓Y", "3,2% → 3,0% (2027)")],
       "Si el BCRP sube la tasa → sube la tasa real → se encarece el crédito para invertir y consumir → crece menos la demanda interna → el PBI se modera de 3,2% a 3,0%, que es la trayectoria del RI para 2027.",
       "BCRP, RI setiembre 2026; BCRPData.")
CADENA("Cadena. Tasa de Interés (i) → Tipo de Cambio (E) y Demanda → Balanza Comercial (X − M)",
       [("↑i", "+25 pb"), ("↑(i − i*)", "0,375 → 0,625 pp"), ("↓E", "Sol más fuerte"), ("↓DA", "Menos importaciones"), ("↓M", "M +10,8% → +6,1%"), ("↑(X − M)", "Saldo US$48.865 MM")],
       "Si sube la tasa → entran capitales y el sol se aprecia, y además se enfría la demanda interna → las importaciones crecen menos → la balanza comercial mejora; para OCP, el sol más fuerte encarece sus costos en soles medidos en dólares.",
       "BCRP, RI setiembre 2026; BCRPData.")
CADENA("Cadena 13. Inflación (P) → Tasa de Interés (i) → Capital de Trabajo de OCP",
       [("↑P", "π 5,25%"), ("↓r", "Ex post −1,00%"), ("↑i BCRP", "4,25% → 4,50% (escenario)"), ("↑Tasas en soles", "Proveedores locales"), ("↓Plazo de pago", "CxP 45 días"), ("↑Capital de trabajo", "+US$2,3 MM por 15 días")],
       "Si la inflación supera el rango meta → la tasa real cae → el BCRP sube la tasa → los proveedores locales acortan plazos → OCP debe financiar más capital de trabajo, aunque su exposición directa a la tasa es baja.")
CAP("Diagrama 2. Ishikawa de Factores Domésticos que Afectan a OCP – Cobriza, 2026–2028")
IMGW("i2.png")
SRC("BCRP, RI setiembre 2026; BCRPData; MINEM; OEFA; " + EST + ". Diagrama conceptual.")
CRIT("la economía peruana de 2026 juega en contra de OCP en casi todas las variables internas y a favor solo por el canal externo. El PBI crece 3,2% por la demanda interna, mientras la minería metálica cae 0,2%; esa combinación es la del modelo OA-DA: más demanda por contratistas, equipos y mano de obra calificada con una oferta que no crece, lo que se traduce en costos. La inflación de 5,25% golpea los insumos locales que OCP compra en soles, y el superávit externo sostiene un sol fuerte que encarece esos costos en dólares. La tasa de interés, que en otras empresas es la variable clave, aquí es secundaria, porque OCP se financia en dólares con su grupo y sus compradores. El riesgo doméstico que el grupo considera más subestimado es regulatorio y social: OEFA ya multó a OCP con 10,3 UIT por el manejo de efluentes (Res. 0155-2025-OEFA/DFAI) y con 34,2 UIT por la estabilidad de un depósito de desmonte (Res. 1807-2025-OEFA/DFAI), la ampliación a 12.000 t/d depende de una MEIA de US$93,3 millones aún en evaluación, y una comunidad que ve utilidades de US$75 millones con salarios reales que caen 4,0% presionará por una mayor participación del auge.")
ESTR("OCP debe usar la estabilidad cambiaria y la holgura de caja de 2026 para fijar sus costos locales antes de que la inflación se consolide. Con un flujo libre estimado de US$50,9 millones en 2026, puede firmar contratos de mediano plazo con sus contratistas de mina y de transporte al Callao con reajustes atados a la inflación esperada (3,05%) y no a la observada (5,25%), lo que le ahorraría alrededor de US$1,2 millones al año sobre unos US$56 millones de costos en soles. Debe dejar la mayor parte de su caja en dólares y convertir a soles solo lo necesario para la planilla y los proveedores de cada trimestre, porque el sol fuerte de hoy es la mejor tasa de conversión que tendrá si el cobre baja y el BCRP deja de comprar dólares. Y debe adelantar la inversión social y ambiental comprometida en la MEIA: con una tasa real negativa y utilidades récord, el costo de hacerla ahora es menor que el de un conflicto que pare la mina durante un mes, que el grupo estima en unos US$20 millones de ventas.")

# ============ SECCIÓN 2 ============
H1("Sección 2."); MARK("s2desc"); RESET_TF()
H2("Descripción de la empresa enfatizando los temas relativos a su dependencia del marco macroeconómico en el cual se desenvuelve la empresa")
SUB("Perfil corporativo y posición competitiva")
T("Operadores Concentrados Peruanos S.A.C. (OCP) es una sociedad anónima cerrada del Grupo Dyer Coriat que opera la mina subterránea de cobre Cobriza, en San Pedro de Coris (Churcampa, Huancavelica). Compró los activos de Doe Run Perú en liquidación por US$19,7 millones más IGV (Andina, 2022). Produce concentrado de cobre con contenido de plata, que vende en dólares a traders en el Callao: según la información de la empresa y el grupo, sus compradores son Perubar S.A. (filial de Glencore, que almacena y embarca concentrados en el puerto) y Mercuria Energy Group. Vende un commodity cuyo precio fija la LME, compra la mayor parte de sus insumos en el mercado local, recibe crédito de sus proveedores y de su grupo, no otorga crédito comercial más allá de los plazos de liquidación y tiene dos clientes grandes, cuyo negocio depende de la demanda china.")
CAP("Tabla 1. Ficha Institucional de Operadores Concentrados Peruanos S.A.C.")
APA(["Concepto", "Detalle"], [
    ["Razón social y RUC", "Operadores Concentrados Peruanos S.A.C. — RUC 20608321731 (Principal Contribuyente Nacional de SUNAT)"],
    ["Grupo económico", "Grupo Dyer Coriat (Grupo DC)"],
    ["Actividad", "Extracción y concentración de mineral de cobre con plata (minería subterránea, flotación)"],
    ["Unidad minera", "Expansión Cobriza, San Pedro de Coris, Churcampa, Huancavelica; planta de 9.100 t/d"],
    ["Adquisición", "Subasta de activos de Doe Run Perú (2022): US$19,7 MM sin IGV, ~US$22 MM en total"],
    ["Producción 2025 (MINEM)", "16.545 TMF de cobre y 22.130 kg (711 mil oz) de plata; sin zinc ni oro"],
    ["Trabajadores", "604 recontratados en 2022 (prensa); 437-461 en planilla mensual en 2025 (datosperu.org; puede excluir contratistas)"],
    ["Clientes", "Perubar S.A. (Glencore) y Mercuria Energy Group, según información de la empresa/grupo; destino final: fundiciones de China"],
    ["Moneda de ingresos y costos", "Ingresos 100% en US$; ~55% del costo operativo en soles (supuesto del grupo)"],
    ["Inversión y permisos", "MEIA-d por US$93,3 MM (optimización a 12.000 t/d, en evaluación del Senace); 8.° ITS por US$8,25 MM aprobado"],
    ["Capital", "Reducción de capital de S/22.638.000 acordada en junta del 24/09/2024 (aviso en El Peruano, nov-2024)"],
    ["Estados financieros", "No publica EEFF (S.A.C. no listada): estimados por el grupo"],
], [4.6, 11.4])
SRC("MINEM; SUNAT (Res. 000009-2024, anexo de PRICO); Andina (2022); Energiminas (2023); Proactivo (2022, 2025); El Peruano (2024); información de la empresa/grupo sobre clientes.")
INT("La tabla 1 muestra una empresa cuya dependencia macroeconómica es la de un exportador indirecto de un solo producto: su ingreso depende del precio mundial del cobre y de dos compradores, y su costo, de la economía peruana.")
SUB("Qué es dato real y qué es estimación: cuatro conceptos que no son equivalentes")
T("Para una minera que no cotiza conviene separar cuatro conceptos: (a) la producción minera, que OCP declara al MINEM y es pública; (b) las ventas comerciales, que en su caso son ventas locales de concentrado a traders y no se publican; (c) las exportaciones, que SUNAT registra por el RUC del exportador, que aquí es el trader y no OCP; y (d) los ingresos declarados a SUNAT, que son reservados. La producción (a) se usa como dato real y las ventas (b) solo como estimación del grupo, nunca como ventas verificadas. La cifra de «US$90 millones anuales» difundida por la prensa en 2022 era una proyección del comprador al adjudicarse la mina, no una venta.")
CAP("Tabla 2. Línea de Tiempo de OCP – Cobriza, 2021–2025")
APA(["Año", "Hecho", "Naturaleza del dato"], [
    ["2021", "Doe Run Perú en liquidación; sin producción de OCP", "Contexto"],
    ["2022", "Adjudicación a OCP por US$19,7 MM + IGV; inicio de actividades el 21/06/2022; toma de posesión el 19/10/2022", "Precio de activos, no ventas"],
    ["2023", "Facturación electrónica desde febrero; arranque de producción (8.351 TMF de Cu)", "Producción real (MINEM)"],
    ["2024-2025", "14.791 y 16.545 TMF de Cu; 649 y 711 mil oz de Ag", "Producción real (MINEM); ventas estimadas"],
], [1.8, 9.6, 4.6])
SRC("Andina (2022); SUNAT (ficha RUC); MINEM, Producción Minera por titular.")
T("La producción real puede contrastarse con el plan de minado 2022-2035 que la propia unidad presentó en la Segunda Modificación del Plan de Cierre de Mina, con información a diciembre de 2021 (SINIA/MINAM). El plan suponía 1,6-1,8 millones de toneladas de mineral al año y un concentrado de 23%-23,5% de cobre; el MINEM registra un cumplimiento de 60% en 2023, 97% en 2024 y 94% en 2025.")
CAP("Tabla 3. Plan de Minado frente a Producción Real de Cobre de OCP, 2022–2025")
APA(["Año", "Mineral plan (t)", "Concentrado plan (t secas)", "Cu plan (t)", "Cu real MINEM (TMF)", "Cumplimiento"], [
    ["2022", "548.000", "19.461", "4.281", "0", "0%"],
    ["2023", "1.649.000", "60.025", "13.806", "8.351", "60%"],
    ["2024", "1.644.000", "64.755", "15.217", "14.791", "97%"],
    ["2025", "1.826.000", "74.820", "17.583", "16.545", "94%"],
], [1.4, 2.8, 3.2, 2.2, 3.2, 2.4])
SRC("SINIA/MINAM, Segunda Modificación del Plan de Cierre de Mina de la UM Cobriza (información a diciembre de 2021); MINEM, Producción Minera por titular.")
CAP("Figura 1. Cobre Contenido: Plan de Minado frente a Producción Real, 2022–2025")
IMGW("f5.png")
SRC("SINIA/MINAM (plan); MINEM (real).")
INT("La tabla 3 y la figura 1 muestran que el arranque de 2023 fue más lento de lo planeado y que desde 2024 la operación se acerca al plan. El plan también calibra la estimación: su ley de cabeza implícita (cobre contenido entre mineral) es 0,84% en 2023, 0,93% en 2024 y 0,96% en 2025, frente al 0,92% efectivo que usa el grupo (ley de 1,0% por recuperación de 92%), y el mineral estimado (1,61 y 1,80 millones de toneladas en 2024 y 2025) difiere menos de 2% del planeado. Con un concentrado de 23,5% en lugar de 24%, el cargo de tratamiento y el flete subirían menos de US$0,2 millones al año: la estimación no cambia. El MINEM solo registra cobre y plata para OCP, aunque su web menciona plomo, zinc y oro: esos metales existen en el yacimiento, pero no se reportan como producción comercial.")
SUB("Dependencia de OCP respecto a las 4 Variables Macroeconómicas Clave")
T("Las cuatro variables de orientación llegan a OCP de forma distinta que a una empresa de consumo. El PBI que la mueve no es el peruano sino el mundial, a través del precio del cobre; el PBI minero peruano solo indica la competencia por recursos. La inflación sube sus costos sin poder trasladarla a precios. El tipo de cambio le favorece cuando el sol se deprecia, porque vende en dólares y paga en soles. La tasa de interés del BCRP casi no la toca, porque su financiamiento está en dólares; la que importa es la de la Fed.")
CAP("Tabla 2. Variables Macroeconómicas Clave y su Impacto en OCP 2023-2027P")
APA(["Variable", "2023", "2024", "2025", "2026P", "2027P", "Impacto en OCP"], [
    ["Cobre LME (US$/lb)", "3,85", "4,15", "4,51", "6,14", "6,38 / 5,70", "↑ Ventas y margen"],
    ["PBI minería metálica (var. %)", "10,9", "3,2", "1,9", "−0,2* / 1,68", "3,02", "Competencia por recursos"],
    ["Inflación fin de periodo (%)", "3,2", "2,0", "1,5", "5,25 (oct) / 3,85", "2,0 / 2,53", "↑ Costos en soles"],
    ["Tasa de referencia (%)", "6,75", "5,00", "4,25", "4,25 (nov)", "n. d.", "Costo de proveedores"],
    ["Tipo de cambio promedio (S/ por US$)", "3,744", "3,754", "3,568", "3,403", "3,35 (MEF)", "↓ E: ↑ costos en US$"],
], [3.6, 1.3, 1.3, 1.3, 2.4, 2.0, 3.2])
SRC("BCRPData (PN01652XM, índice de minería metálica, IPC de Lima, PD04722MM y PN01234PM); BCRP, RI setiembre 2026 (cobre 2027: 6,38); MEF, MMM 2027-2030, cuadros C-01 y C-02 (cobre 2027: 5,70). * Enero-agosto. Tipo de cambio 2026: promedio enero-octubre.")
INT("La tabla 4 muestra que 2026 combina el precio del cobre más alto de la serie con la inflación más alta desde 2023 y un sol fuerte: la variable que más ayuda a OCP coexiste con las dos que más le restan.")
CAP("Tabla 3. Estados Financieros Estimados de OCP, 2023–2026P (US$ millones)")
APA(["Partida (estimado por el grupo)", "2023", "2024", "2025", "2026P", "Var. 25/24"], [
    ["Ingreso bruto por cobre", "68,4", "130,5", "158,7", "206,2", "+21,6%"],
    ["Ingreso bruto por plata (subproducto)", "7,3", "16,5", "25,7", "48,3", "+55,6%"],
    ["(−) TC/RC y flete al Callao", "−7,4", "−12,4", "−7,8", "−5,3", "−37,4%"],
    ["Ventas netas", "68,2", "134,5", "176,6", "249,2", "+31,3%"],
    ["Costo de operación (mina y planta)", "56,9", "80,4", "93,5", "96,1", "+16,3%"],
    ["EBITDA", "5,3", "45,2", "72,7", "136,0", "+61,1%"],
    ["Depreciación y amortización", "2,2", "5,3", "11,6", "16,6", "+117,1%"],
    ["Regalía minera, IEM y aportes", "1,0", "3,0", "4,4", "10,5", "+46,2%"],
    ["Utilidad operativa (EBIT)", "3,1", "39,8", "61,2", "119,5", "+53,5%"],
    ["Gastos financieros", "0,0", "1,7", "4,1", "3,7", "+145,5%"],
    ["Participación de trabajadores e IR", "1,1", "13,4", "20,0", "40,7", "+49,4%"],
    ["Utilidad neta", "2,0", "24,8", "37,0", "75,1", "+49,4%"],
    ["Cuentas por cobrar (30 días)", "5,6", "11,1", "14,5", "20,5", "+31,3%"],
    ["Cuentas por pagar (45 días)", "7,6", "10,7", "12,3", "12,7", "+15,2%"],
    ["Capex", "25,0", "50,0", "40,0", "35,0", "−20,0%"],
    ["Deuda con vinculadas / prepagos", "20,9", "51,3", "45,6", "0,0", "−11,0%"],
    ["Patrimonio", "32,0", "50,7", "87,7", "162,9", "+72,9%"],
], [6.0, 1.8, 1.8, 1.8, 1.8, 2.4])
SRC(EST + ". Producción: MINEM; precios: BCRPData; metodología: tabla 6. Cifras en dólares; ventas 2025 equivalentes a S/630 millones al tipo de cambio promedio.")
CAP("Tabla 4. Metodología y Fuentes de la Estimación de los Estados Financieros de OCP")
APA(["Partida", "Método de estimación", "Fuente"], [
    ["Producción (dato real)", "Cobre y plata finos por mes, titular OCP, unidad Expansión Cobriza", "MINEM, Producción Minera por titular"],
    ["Ventas netas", "Cu pagable 96,5% y Ag pagable 90% × precio promedio anual − TC/RC benchmark − flete US$70/tmh", "BCRPData; benchmark China-Antofagasta (88, 80, 21,25 y 0 US$/dms)"],
    ["Mineral tratado", "Cu fino / (ley 1,0% × recuperación 92%; 88% en 2023): 1,8 Mt en 2025 (~5.100 t/d)", "Supuesto del grupo; planta de 9.100 t/d"],
    ["Costo de operación", "Mineral tratado × US$60, 50, 52 y 56 por tonelada (2023-2026P)", "Volcan (49-70 US$/t); Nexa Cerro Lindo (39,9 US$/t)"],
    ["Depreciación", "Compra de US$22 MM a 10 años; capex a 8 años", "Andina; Energiminas; Veritrade (capex importado)"],
    ["Regalía e IEM", "Tramos por margen operativo (1%-12% y 2%-8,4%)", "Leyes 29788 y 29789"],
    ["Participación e IR", "8% y 29,5% con arrastre de pérdidas", "D. Leg. 892; LIR"],
    ["Balance", "Capital de US$30 MM menos la reducción de S/22,6 MM; deuda como variable de cierre al 8%", "El Peruano (2024); supuesto del grupo"],
], [3.0, 7.6, 5.4])
SRC("OCP_EEFF.xlsx y FUENTES_Y_SUPUESTOS.md del grupo. Las cifras son estimaciones con fuentes públicas, no estados financieros auditados.")
CAP("Tabla 5. Ratios Financieros Estimados de OCP, 2023–2026P")
APA(["Ratio", "2023", "2024", "2025", "2026P"], [
    ["Margen EBITDA (%)", "7,7", "33,6", "41,2", "54,6"],
    ["Margen neto (%)", "2,9", "18,4", "21,0", "30,2"],
    ["Cash cost C1 neto de plata (US$/lb Cu)", "3,49", "2,62", "2,32", "1,78"],
    ["Plata / ingreso bruto (%)", "9,6", "11,2", "13,9", "19,0"],
    ["Deuda / EBITDA (veces)", "3,96", "1,13", "0,63", "0,00"],
    ["Rentabilidad del patrimonio, ROE (%)", "6,2", "48,8", "42,2", "46,1"],
    ["Liquidez corriente (veces)", "2,06", "2,17", "2,26", "3,10"],
    ["Capex / ventas (%)", "36,6", "37,2", "22,6", "14,0"],
    ["Pagos al Estado y trabajadores (US$ MM)*", "2,1", "16,4", "24,4", "51,2"],
], [8.0, 2.0, 2.0, 2.0, 2.0])
SRC("Cálculos con base en " + EST + ". * Regalía, IEM, aportes, impuesto a la renta y participación de trabajadores.")
INT("Las tablas 5 a 7 muestran una mina que pasó de su arranque (margen EBITDA de 7,7%) a un margen extraordinario (54,6%) en tres años, y que se desapalancó al mismo ritmo (deuda/EBITDA de 3,96 a 0). De los 13,4 pp de mejora del margen EBITDA entre 2025 y 2026P, prácticamente todos vienen del precio.")

SUB("Variable 1. PBI Mundial, Minería Metálica y Precio del Cobre: el precio define las ventas")
T("Las ventas de OCP no responden al PBI peruano sino al precio del cobre. Entre 2024 y 2025 el volumen creció 11,9% y el precio 8,7%, y las ventas estimadas 31,3%; entre 2025 y 2026P el volumen cae 4,5% y el precio sube 36,1%, y las ventas suben 41,1%. Frente al precio del cobre, la elasticidad de las ventas es 0,86 (el cobre aporta 84% del ingreso bruto) y la del EBITDA 1,55, porque el costo por tonelada no cambia con el precio. Con el volumen proyectado (+5% anual por el aumento del ritmo de planta, supuesto del grupo), se proyectan tres escenarios de precio: alto (US$7,00 y US$6,80, por encima del BCRP), base (US$5,70 y US$5,60, MMM 2027-2030) y bajo (US$4,50 y US$4,30, vuelta al nivel de 2025 si China crece cerca de 4%).")
FORM("Elasticidad = % de cambio de las ventas / % de cambio del precio del cobre (o del PBI minero)",
     "la elasticidad mide cuántos puntos porcentuales cambian las ventas por cada 1% que cambia la variable macro; si es mayor que 1, la empresa amplifica el ciclo.",
     "precio del cobre 2027P de US$5,70 a US$6,27 (+10%): ventas de US$233,4 a 253,5 millones (+8,6%) → ε = 8,6% / 10% = 0,86; EBITDA +15,5% → ε = 1,55. Frente al PBI minero: en 2025 las ventas estimadas crecieron 31,3% con un PBI de minería metálica de 1,9% → 31,3 / 1,9 = 16,5, una cifra que no mide causalidad sino que el precio y el arranque de la mina dominan.",
     "las ventas de OCP siguen al cobre casi uno a uno y su EBITDA lo amplifica; frente al PBI minero peruano la relación es débil, por lo que la proyección se hace con el precio y no con el PBI.")
CAP("Tabla 6. Proyección de Ventas de OCP según el Precio del Cobre, 2026P–2028P (US$ millones)")
APA(["Escenario (probabilidad)", "Cobre 2027 / 2028 (US$/lb)", "2025", "2026P", "2027P", "2028P"], [
    ["Alto (25%)", "7,00 / 6,80", "176,6", "249,2", "286,3", "288,4"],
    ["Base, MMM (50%)", "5,70 / 5,60", "176,6", "249,2", "233,4", "236,5"],
    ["Bajo (25%)", "4,50 / 4,30", "176,6", "249,2", "176,9", "173,5"],
    ["Cobre fino (TMF)", "—", "16.545", "15.792", "16.582", "17.411"],
    ["PBI minería metálica (var. %)", "—", "1,9", "1,68", "3,02", "1,46"],
], [4.0, 3.4, 1.9, 1.9, 1.9, 1.9])
SRC(EST + "; BCRPData; MEF, MMM 2027-2030, cuadros C-01 y C-02. 2026P: precio enero-octubre (US$6,14) en los tres escenarios. Probabilidades: juicio del grupo.")
CAP("Figura 1. Ventas Estimadas de OCP por Escenario de Precio del Cobre, 2023–2028P")
IMGW("f1.png")
SRC(EST + ". Proyecciones según la tabla 8.")
INT("La figura 2 muestra que 2026 sería el máximo de ventas en los escenarios base y bajo: la producción no crece lo suficiente para compensar un cobre que vuelva a US$5,60. La brecha entre el escenario alto y el bajo en 2028 (US$115 millones) es más de la mitad de las ventas de 2025: el riesgo de precio domina cualquier otra variable.")
CONJ("si el cargo de tratamiento vuelve a niveles positivos (US$20-40 por tonelada) en 2027-2028, como ocurre cuando las fundiciones chinas recortan producción, OCP perdería además US$2-3 millones al año por términos de venta; por eso el precio del cobre y los cargos de tratamiento tienden a moverse juntos en contra de la mina cuando el ciclo se revierte.")

SUB("Variable 2. Inflación: presión sobre los costos en soles sin traslado al precio")
T("El costo de operación estimado de OCP fue US$93,5 millones en 2025 (US$52 por tonelada tratada) y sería US$96,1 millones en 2026P (US$56 por tonelada), en línea con la referencia de Volcan, cuyo costo unitario consolidado subió de US$49,2 por tonelada en 2024 a US$60,6-70 en 2026 (Volcan, 2026), y por encima de Cerro Lindo de Nexa (US$39,9 en 2025), una mina de mayor escala (Nexa Resources, 2026). El grupo supone que 55% de ese costo se paga en soles (planilla, contratistas, energía, explosivos, reactivos y bolas de molienda, que no aparecen en las importaciones directas de OCP). Con la inflación de 5,25%, el efecto precio sobre la parte en soles suma US$3,0 millones en 2026; con 2,0% (BCRP) en 2027 y 2,50% (MEF) en 2028, US$1,2 y US$1,6 millones. OCP no puede trasladar ese aumento: su precio de venta lo fija la LME.")
CAP("Tabla 7. Inflación y Costos en Soles de OCP, 2025–2028P (US$ millones)")
APA(["Concepto", "2025", "2026P", "2027P", "2028P"], [
    ["Inflación aplicada (%)", "1,5", "5,25", "2,0", "2,50"],
    ["Costo de operación + G&A", "99,5", "102,6", "109,2", "116,8"],
    ["Parte en soles (55%)", "54,7", "56,4", "60,1", "64,2"],
    ["Aumento de costo por inflación", "0,8", "3,0", "1,2", "1,6"],
    ["Costo por tonelada tratada (US$/t)", "52", "56", "57", "58"],
], [7.0, 2.2, 2.2, 2.2, 2.2])
SRC(EST + "; BCRPData (inflación 2025 y octubre 2026); BCRP, RI setiembre 2026 (2027P); MEF, MMM 2027-2030, cuadro C-01 (2028P).")
CAP("Figura 2. Costo por Tonelada de OCP, Referencia de Volcan e Inflación, 2023–2026P")
IMGW("f2.png")
SRC(EST + "; Volcan Compañía Minera, Análisis y Discusión de la Gerencia (promedio simple de trimestres; 2026: enero-setiembre); BCRPData.")
CAP("Modelo 5. Isocuanta Minera: Trabajo y Capital ante la Inflación y la Ampliación")
IMGW("m4.png", 6.6)
SRC(EST + "; Veritrade/SUNAT (capex importado); BCRPData. Diagrama conceptual.")
INT("La figura 3 muestra que el costo de OCP sigue la tendencia de su referencia y que el alza de 2026 coincide con el salto de la inflación. El modelo 5 muestra que la inflación salarial vuelve más empinada la recta de isocosto y desplaza el óptimo de A a B: más capital por trabajador, que es la lógica de los filtros prensa, la bomba de relleno y el topador importados en 2025-2026, y de la ampliación a 12.000 t/d (Q₁).")

SUB("Variable 3. Tipo de Cambio Sol/USD: cobertura natural invertida")
T("OCP vende en dólares y paga cerca de 55% de su costo en soles, de modo que una depreciación del sol le favorece y una apreciación le perjudica. Con el escenario base de 2027, una depreciación de 10% elevaría el EBITDA en US$4,5 millones y una apreciación de 5% lo reduciría en US$2,7 millones. Su capex importado (US$7,27 millones CIF entre 2023 y 2026, 77% de Italia y Alemania) se paga en dólares o euros y no depende del sol, pero sí de la inflación externa. La regalía y el IEM se calculan sobre resultados en soles, por lo que un sol débil también eleva los pagos al Estado. La apreciación de 2025 (del promedio de S/3,754 en 2024 a S/3,568) le costó, por este canal, alrededor de US$2,8 millones.")
CAP("Tabla 8. Escenarios de Tipo de Cambio y EBITDA de OCP, 2027P (US$ millones)")
APA(["Escenario", "TC (S/ por US$)", "Costo en soles medido en US$", "EBITDA 2027P", "Var. frente a base"], [
    ["Sol apreciado (−5%)", "3,28", "59,5", "114,0", "−2,7"],
    ["Base (MEF 2027)", "3,35-3,45", "56,5", "116,6", "—"],
    ["Sol depreciado (+5%)", "3,62", "53,8", "119,0", "+2,4"],
    ["Sol depreciado (+10%)", "3,80", "51,4", "121,1", "+4,5"],
], [4.0, 2.6, 3.6, 2.8, 3.0])
SRC(EST + "; MEF, MMM 2027-2030, cuadro C-01. Cobre a US$5,70 por libra; 55% del costo operativo en soles (supuesto del grupo).")
CAP("Figura 3. EBITDA 2027P de OCP según el Precio del Cobre y el Tipo de Cambio")
IMGW("f3.png")
SRC(EST + ". Precio de equilibrio: cobre con el que la utilidad operativa es cero.")
INT("La figura 4 muestra que el tipo de cambio desplaza la curva de EBITDA en unos pocos millones, mientras el cobre la recorre de US$40 a US$175 millones. Para OCP, el tipo de cambio es un riesgo de segundo orden; el precio de equilibrio de US$2,83 por libra muestra que la mina resiste una caída de 50% del cobre antes de perder dinero.")

SUB("Variable 4. Tasa de Referencia BCRP y tasa internacional: costo del financiamiento")
T("La tasa de referencia bajó de 7,50% en diciembre de 2022 a 4,25% en 2025, pero OCP no se benefició: no tiene deuda bancaria pública conocida. El grupo estima que financió el arranque y el capex de 2023-2024 (US$75 millones) con aportes de capital (US$30 millones), préstamos de vinculadas y prepagos de compradores, con una deuda que llegó a US$51,3 millones en 2024 y gastos financieros de US$4,1 millones en 2025, a una tasa supuesta de 8% (SOFR más un margen). En setiembre de 2024 la junta redujo el capital en S/22,6 millones (US$6,0 millones), una devolución a los accionistas que solo tiene sentido si la caja operativa ya cubría el capex. Con el flujo libre de 2026P (US$50,9 millones), la deuda estimada se cancela.")
CAP("Tabla 9. Tasa de Referencia y Estructura Financiera Estimada de OCP, 2023–2026P (US$ millones)")
APA(["Indicador", "2023", "2024", "2025", "2026P"], [
    ["Tasa de referencia BCRP, diciembre (%)", "6,75", "5,00", "4,25", "4,25"],
    ["Fed, punto medio, diciembre (%)", "5,375", "4,375", "3,625", "3,875"],
    ["Deuda con vinculadas / prepagos (estimada)", "20,9", "51,3", "45,6", "0,0"],
    ["Gastos financieros (8%)", "0,0", "1,7", "4,1", "3,7"],
    ["Flujo de caja libre (operación − capex)", "−23,9", "−24,4", "5,7", "50,9"],
    ["Capital social (neto de la reducción)", "30,0", "24,0", "24,0", "24,0"],
], [7.0, 2.2, 2.2, 2.2, 2.2])
SRC("BCRPData, PD04722MM; Federal Reserve (2026); El Peruano (2024); " + EST + ".")
CAP("Figura 4. Deuda Estimada y Gastos Financieros de OCP, 2023–2026P")
IMGW("f4.png")
SRC(EST + ".")
INT("La figura 5 muestra que el ciclo de deuda de OCP fue de arranque y que el precio del cobre lo cerró en 2026. La sensibilidad a la tasa es baja (US$0,11 millones por 25 pb sobre la deuda de 2025), pero la tasa vuelve a importar si la ampliación a 12.000 t/d se financia con deuda en 2027-2028.")

H2("En base al análisis de la sección anterior, analizar el impacto del entorno macroeconómico sobre la empresa en cuestión, considerando la situación actual y los próximos tres años."); MARK("s2imp")

SUB("1. Variaciones del PBI y del precio del cobre: efecto sobre las ventas de OCP")
T("El hilo con la Sección 1 es directo: el crecimiento mundial (subtema 1) y la escasez de concentrado (modelo 1) fijan el precio, y el precio fija las ventas. Con el escenario base del MMM, las ventas estimadas caerían de US$249,2 millones en 2026 a US$233,4 millones en 2027 y US$236,5 millones en 2028, aunque la producción crezca 5% al año. En el escenario alto llegarían a US$288 millones y en el bajo a US$174 millones.")
AC("la variable que el informe debe vigilar no es el PBI peruano sino el crecimiento de China y la inversión mundial en redes eléctricas; una caída de un punto en el crecimiento chino bajaría el cobre en el orden de 10% a 15% y las ventas de OCP en unos US$20-30 millones.")
CADENA("Cadena 14. PBI de China (Y*) → Precio del Cobre (Pcu) → Ventas y EBITDA de OCP",
       [("↓Y China", "4,5% → 4,2% (2027)"), ("↓D cobre", "Construcción y redes"), ("↓Pcu", "US$6,14 → 5,70 (base)"), ("↓Ventas", "US$249,2 → 233,4 MM"), ("↓EBITDA", "ε = 1,55"), ("↓Utilidad", "US$75,1 → 62,1 MM")],
       "Si China se desacelera → baja la demanda de cobre → cae el precio → bajan las ventas de OCP y, más que proporcionalmente, su EBITDA y su utilidad, porque el costo por tonelada no baja.",
       "BCRP, RI setiembre 2026; MEF, MMM 2027-2030; " + EST + ".")

SUB("2. Tasa de interés y su efecto sobre las cuentas por cobrar (CxC)")
T("Las cuentas por cobrar estimadas de OCP (US$14,5 millones en 2025, 30 días de ventas) son liquidaciones pendientes de Glencore y Mercuria: el comprador paga cerca de 90% del valor provisional al embarque y el saldo cuando se fija el precio, uno a tres meses después. Con una tasa de 8%, mantener ese saldo cuesta US$1,2 millones al año, y cada 25 pb adicionales de la Fed, US$0,04 millones. El riesgo no es de cobranza, porque los compradores son traders globales, sino de precio: si el cobre baja entre el embarque y la liquidación final, la cuenta por cobrar se ajusta a la baja. Con una caída de 5% del cobre en el periodo de cotización, el ajuste sería de alrededor de US$0,7 millones por cada mes de ventas pendiente.")
AC("en una mina, la tasa de interés afecta poco a las cuentas por cobrar; lo que las afecta es la volatilidad del precio durante el periodo de cotización, que se puede cubrir con el propio comprador.")
CADENA("Cadena 15. Tasa de la Fed (i*) → Costo de Financiar las CxC → Caja de OCP",
       [("↑i*", "Fed 3,75%–4,00%"), ("↑SOFR", "Tasa de prepagos"), ("↑Costo CxC", "US$1,2 MM (2025)"), ("Pcu volátil", "Periodo de cotización"), ("↓Liquidación final", "−US$0,7 MM por −5%"), ("↓Caja OCP", "Capital de trabajo")],
       "Si sube la tasa internacional → se encarece financiar las cuentas por cobrar; si además baja el cobre durante el periodo de cotización → la liquidación final reduce la caja de OCP.",
       "Federal Reserve (2026); " + EST + ".")

SUB("3. Tasa de interés: efecto sobre cuentas por pagar y gastos financieros")
T("El grupo estima una deuda de US$45,6 millones a fin de 2025, con gastos financieros de US$4,1 millones. El grupo supone que la deuda con vinculadas es de largo plazo y que los prepagos de traders son de corto plazo, porque se cancelan con entregas de concentrado en uno o dos años. Un alza de 25 pb costaría US$0,11 millones al año y una de 100 pb, US$0,46 millones: el riesgo de tasa es pequeño y desaparece en 2026P, cuando el flujo libre cancela la deuda. Las cuentas por pagar comerciales (US$12,3 millones, 45 días) son financiamiento sin costo de proveedores locales, que valen US$1,0 millones al año al 8%; si el BCRP sube la tasa, esos proveedores intentarán acortar plazos. El punto crítico es la ampliación: si los US$93,3 millones de la MEIA se financiaran con deuda a 8%, el gasto financiero sería de unos US$7,5 millones al año.")
AC("la tasa de interés importa menos para la operación actual que para la decisión de ampliar; con el cobre alto, financiar la ampliación con caja propia evita depender de la Fed.")
CAP("Tabla 11. Sensibilidad de los Gastos Financieros de OCP a la Tasa, 2025–2028P (US$ millones)")
APA(["Escenario de tasa", "2025", "2026P", "2027P", "2028P"], [
    ["Base: gastos financieros estimados", "4,1", "3,7", "0,0", "0,0"],
    ["Alza de 25 pb sobre US$45,6 MM", "+0,11", "+0,11", "0,0", "0,0"],
    ["Alza de 100 pb sobre US$45,6 MM", "+0,46", "+0,46", "0,0", "0,0"],
    ["Ampliación financiada con deuda (US$93,3 MM al 8%)", "—", "—", "7,5", "7,5"],
    ["Valor de las CxP sin costo al 8% (US$12,3 MM)", "1,0", "1,0", "1,1", "1,2"],
], [7.6, 2.0, 2.0, 2.0, 2.0])
SRC(EST + "; Energiminas (2023), MEIA-d de US$93,3 MM.")
CADENA("Cadena 16. Tasa de Interés (i) → Gastos Financieros y CxP de OCP",
       [("↑P", "π 5,25%"), ("↓r", "Ex post −1,00%"), ("↑i", "+25 pb (escenario)"), ("↑Gastos financieros", "+US$0,11 MM"), ("↓Plazo de proveedores", "CxP 45 días"), ("↑Costo de ampliar", "US$7,5 MM/año con deuda")],
       "Si la inflación lleva a subir la tasa → sube levemente el gasto financiero y los proveedores acortan plazos → el mayor costo aparece si OCP financia la ampliación con deuda.",
       "BCRPData; " + EST + ".")

SUB("4. Inflación y su repercusión sobre los costos operativos")
T("Con una inflación de 5,25%, el efecto precio sobre la parte en soles del costo de OCP suma US$3,0 millones en 2026, US$1,2 millones en 2027 y US$1,6 millones en 2028 (tabla 9). Cada punto de inflación cuesta alrededor de US$0,6 millones sobre los costos en soles, y US$1,0 millones si se suman los efectos indirectos sobre el diésel y los fletes. El margen absorbe estos montos sin dificultad en los escenarios alto y base, pero no en el bajo: con cobre de US$4,50, el EBITDA de 2027 caería a US$64 millones y la inflación acumulada de 2026-2027 equivaldría a 6% de ese EBITDA. El riesgo es que el costo por tonelada se ajusta hacia arriba con la inflación y no vuelve a bajar cuando el cobre cae.")
AC("la inflación es el costo que el ciclo de precios oculta: hoy representa 2% del EBITDA, pero en el escenario bajo duplica su peso.")
CADENA("Cadena 17. Inflación (P) → Salarios e Insumos (w) → Costo por Tonelada de OCP",
       [("↑P", "π 5,25%"), ("↑w", "Convenio colectivo"), ("↑Insumos", "Diésel, explosivos, reactivos"), ("↑Costo/t", "US$52 → 56/t"), ("↑Costo total", "+US$3,0 MM (2026)"), ("↓Margen", "−1,2 pp")],
       "Si sube la inflación → suben salarios e insumos locales → sube el costo por tonelada → como OCP no fija su precio, el aumento sale íntegramente del margen.",
       "BCRPData; " + EST + ".")

SUB("5. Inflación y su repercusión sobre CxC y CxP")
T("La inflación redistribuye valor entre OCP, sus compradores y sus proveedores, pero en monedas distintas. Las cuentas por cobrar están en dólares y pierden poder de compra con la inflación de EE.UU. (3,7% PCE en 2026): US$0,8 millones sobre US$20,5 millones en 2026P. Las cuentas por pagar están mayormente en soles y se alivian con la inflación peruana (5,25%): US$0,7 millones sobre US$12,7 millones. El efecto neto es casi nulo (−US$0,1 millones al año). Lo que importa es el plazo: como el comprador liquida en 30 días y los proveedores cobran a 45, OCP se financia con sus proveedores; si la inflación los lleva a acortar plazos, la empresa debe inmovilizar unos US$2,3 millones más por cada 15 días de plazo que pierda con sus proveedores locales.")
AC("con un ciclo de caja positivo y corto, la inflación no erosiona el capital de trabajo de OCP; su efecto pasa por los costos y no por el balance.")
CADENA("Cadena 18. Inflación (P y π*) → Valor Real de CxC y CxP → Capital de Trabajo de OCP",
       [("↑π*", "PCE 3,7%"), ("↓Valor real CxC", "−US$0,8 MM"), ("↑π Perú", "5,25%"), ("↓Valor real CxP", "+US$0,7 MM"), ("Efecto neto", "−US$0,1 MM"), ("↓Plazo proveedores", "+US$2,3 MM por 15 días")],
       "Si sube la inflación en EE.UU. y en el Perú → se compensan las pérdidas en cuentas por cobrar y las ganancias en cuentas por pagar → el riesgo real está en que los proveedores acorten plazos.",
       "BCRPData; " + EST + ".")

SUB("6. Tipo de cambio y sus implicancias en operaciones y balance")
T("El hilo con la Sección 1 (subtemas 4 y 3 de Perú) muestra la paradoja de OCP: el cobre caro aprecia el sol y le encarece los costos. En el escenario base de 2027, una depreciación de 10% sumaría US$4,5 millones al EBITDA y una apreciación de 5% restaría US$2,7 millones (tabla 10). En el balance, sus activos y pasivos son mayormente en dólares (cuentas por cobrar, deuda con vinculadas), por lo que la diferencia de cambio se concentra en las cuentas por pagar y en los impuestos por pagar en soles. El capex importado (US$4,59 millones en 2026, 77% de Italia y Alemania) agrega una exposición al euro que el sol no cubre. En el crédito, la deuda con vinculadas y los prepagos están en dólares, igual que sus ventas, por lo que el tipo de cambio no altera su capacidad de pago; el crédito de proveedores locales, en soles, se abarata en dólares cuando el sol se deprecia.")
AC("OCP tiene una cobertura natural invertida: gana cuando el sol se debilita, que suele ser cuando el cobre baja; esa correlación amortigua el escenario bajo en unos US$4-5 millones de EBITDA.")
CADENA("Cadena 19. Tipo de Cambio (E) → Costos en Dólares → EBITDA de OCP",
       [("↓Pcu", "Escenario bajo US$4,50"), ("↓Oferta de US$", "Menos exportaciones"), ("↑E", "S/3,45 → 3,80"), ("↓Costo en US$", "US$56,5 → 51,4 MM"), ("↑EBITDA", "+US$4,5 MM"), ("Amortiguador parcial", "64 → 69 MM")],
       "Si baja el cobre → se reducen las exportaciones y el sol se deprecia → bajan los costos en soles medidos en dólares → el EBITDA de OCP cae menos de lo que caería con un tipo de cambio fijo.",
       "BCRPData; MEF, MMM 2027-2030; " + EST + ".")

SUB("7. Empleo, salarios y poder adquisitivo: efecto sobre costos laborales y licencia social")
T("La economía peruana crea empleo (desempleo de Lima en 4,4%) pero con salarios reales que caen 4,0%. En Huancavelica, OCP tuvo entre 437 y 461 trabajadores en planilla en 2025, más contratistas, y genera en 2026P una participación de utilidades estimada de US$9,3 millones, el doble que en 2025. Esa combinación tiene dos efectos: eleva el costo laboral total en los años de cobre alto y eleva las expectativas de la comunidad.")
AC("el canal laboral es procíclico: cuanto más sube el cobre, más sube el costo laboral y social de OCP, que no baja con la misma rapidez cuando el precio cae.")
CADENA("Cadena 20. Empleo (N) y Salario Real (w/P) → Costo Laboral y Licencia Social de OCP",
       [("↓u", "Lima 4,4%"), ("↓w/P", "−4,0% real"), ("↑Utilidad", "US$75,1 MM (2026P)"), ("↑Participación", "US$4,6 → 9,3 MM"), ("↑Expectativas", "Comunidad de Coris"), ("↑Costo social", "Riesgo de paralización")],
       "Si el salario real cae mientras las utilidades de la mina suben → aumentan la participación y las expectativas de trabajadores y comunidad → sube el costo social y el riesgo de conflicto de OCP.",
       "BCRPData; Proactivo (2022); " + EST + ".")

SUB("8. PBI de los clientes de OCP (Glencore, Mercuria y China como destino final) y efecto indirecto")
T("OCP tiene dos clientes grandes, según la información de la empresa y el grupo: Perubar S.A., la filial de Glencore que almacena, mezcla y embarca concentrados en el Callao (Glencore Perú, 2026), y Mercuria Energy Group. La evidencia pública es indirecta pero consistente: SUNAT no registra exportaciones con el RUC de OCP (Veritrade), lo que indica que vende en el mercado local a traders que figuran como exportadores. El «PBI» relevante de esos clientes es el margen de las fundiciones chinas a las que revenden: con un cargo de tratamiento de US$0 en 2026 y spot negativo, las fundiciones pierden dinero en cada tonelada, lo que hoy beneficia a OCP pero vuelve frágil el acuerdo. Si China crece 4,2% en 2027 y recorta la producción de cobre refinado, los traders exigirán cargos positivos o reducirán sus prepagos.")
T("La macroeconomía afecta a Glencore y a Mercuria por tres vías: el crecimiento chino, que define cuánto concentrado pueden revender; la tasa de la Fed, que encarece el capital de trabajo con que financian inventarios y prepagos; y el dólar, que mueve el precio de los metales. Con la Fed en 3,75%–4,00% y China desacelerándose, los traders serán más selectivos con productores pequeños, y eso llega a OCP como menores prepagos y cargos más altos.")
AC("depender de dos compradores no es un riesgo de crédito, porque son de los traders más grandes del mundo, sino un riesgo de negociación: OCP es un proveedor pequeño de concentrado de baja escala, y su poder de negociación existe solo mientras haya escasez.")
CADENA("Cadena 21. PBI de China (Y*) → Margen de las Fundiciones → Términos de Glencore y Mercuria → OCP",
       [("↓Y China", "4,2% (2027)"), ("↓Margen de fundición", "TC/RC US$0; spot −US$125"), ("↓Producción refinada", "Recorte de fundiciones"), ("↑TC/RC", "US$0 → 20-40/dms"), ("↓Prepagos", "Traders más selectivos"), ("↓Ventas netas OCP", "−US$2-3 MM al año")],
       "Si China se desacelera → las fundiciones con márgenes negativos recortan producción → los traders exigen mayores cargos de tratamiento y reducen prepagos → bajan las ventas netas y el financiamiento disponible de OCP.",
       "BCRP, RI setiembre 2026; Skillings (2026); Fastmarkets (2026); Veritrade/SUNAT; información de la empresa/grupo.")

SUB("9. Liquidez del sistema financiero, crédito y riesgo de financiamiento")
T("La liquidez en soles crece 16,7% y el crédito privado 10,3%, pero ese ciclo no llega a OCP, que se financia con su grupo y sus compradores. El grupo estima un déficit de caja de US$48,2 millones en 2023-2024 (capex de US$75 millones), cubierto con deuda de vinculadas o prepagos, y un superávit desde 2025: el flujo libre pasa de US$5,7 a US$50,9 millones en 2026P. El riesgo de liquidez de OCP no es de crédito bancario, sino de que el ciclo de precios se revierta justo cuando necesite financiar la ampliación: en el escenario bajo, el flujo libre de 2027 caería a cerca de US$20 millones, menos de la cuarta parte de lo que exige la ampliación de US$93,3 millones.")
T("La morosidad del sistema financiero no afecta a OCP como acreedor, porque sus deudores son traders globales, pero sí como cliente de contratistas locales: si el BCRP sube la tasa y la morosidad de las pymes de servicios mineros aumenta, sus proveedores en Huancavelica tendrán menos crédito y más incentivos para pedir adelantos o acortar plazos.")
AC("la mejor oportunidad de financiamiento de OCP es interna y temporal: el flujo libre de 2026-2027 en el escenario base (más de US$100 millones acumulados) alcanza para la ampliación sin deuda, pero solo si no se reparte antes.")
CAP("Tabla 13. Escenarios de Resultados de OCP, 2027P–2028P (US$ millones)")
APA(["Escenario (prob.)", "Cobre (US$/lb)", "Ventas 2027P", "EBITDA 2027P", "Utilidad 2027P", "EBITDA 2028P", "Utilidad 2028P"], [
    ["Alto (25%)", "7,00 / 6,80", "286,3", "164,1", "92,9", "160,0", "87,7"],
    ["Base (50%)", "5,70 / 5,60", "233,4", "116,6", "62,1", "113,2", "57,4"],
    ["Bajo (25%)", "4,50 / 4,30", "176,9", "64,1", "28,0", "53,7", "18,8"],
    ["Valor esperado", "—", "232,5", "115,3", "61,3", "110,0", "55,4"],
], [3.0, 2.4, 2.0, 2.2, 2.2, 2.2, 2.0])
SRC(EST + "; MEF, MMM 2027-2030; BCRP, RI setiembre 2026. Probabilidades: juicio del grupo. Utilidades sin gastos financieros (deuda cero desde 2026P).")
CADENA("Cadena 22. Liquidez (M) y Precio del Cobre (Pcu) → Flujo Libre → Financiamiento de la Ampliación",
       [("↑M local", "Liquidez +16,7%"), ("Fondeo en US$", "Grupo DC y traders"), ("↑Pcu", "US$6,14/lb"), ("↑Flujo libre", "US$50,9 MM (2026P)"), ("↓Pcu (bajo)", "Flujo libre ~US$20 MM"), ("↑Deuda para ampliar", "US$93,3 MM al 8%")],
       "Si el cobre se mantiene alto → el flujo libre financia la ampliación sin deuda; si baja → la ampliación requeriría deuda en dólares justo cuando la Fed mantiene tasas altas y los traders son más selectivos.",
       "BCRPData; Energiminas (2023); " + EST + ".")
CAP("Diagrama 7. Ishikawa del Impacto del Entorno Macroeconómico sobre OCP, 2026–2028")
IMGW("i9.png")
SRC(EST + "; síntesis de los nueve canales. Diagrama conceptual.")
CRIT("los nueve canales muestran que el entorno macroeconómico pesa sobre OCP a través de una sola variable dominante, el precio del cobre, y de tres variables secundarias que se mueven en contra cuando el cobre sube: la inflación local, el sol fuerte y las expectativas laborales y sociales. La elasticidad del EBITDA al cobre es 1,55 y la de la utilidad neta 1,89; la diferencia entre el escenario alto y el bajo en 2027 es de US$100 millones de EBITDA, frente a US$4,5 millones por una depreciación de 10%, US$3,0 millones por la inflación de 2026 y US$0,11 millones por 25 pb de tasa. La conjetura del grupo es que el riesgo más subestimado no es la caída del precio en sí, sino su coincidencia con tres hechos: la ampliación a 12.000 t/d en ejecución, cargos de tratamiento que vuelvan a ser positivos y costos que ya se ajustaron a la inflación de 2026. En ese escenario, la mina que hoy gana US$75 millones podría ganar menos de US$20 millones en 2028 con la misma producción. La fortaleza de OCP es su precio de equilibrio de US$2,83 por libra: no está en riesgo de quiebra, sino de no poder financiar su crecimiento.")
ESTR("OCP debe gestionar cada variable con el instrumento que le corresponde y en el orden de su peso. Primero el cobre: fijar el precio de 30% a 40% de la producción de 2027 mientras la LME esté sobre US$5,50, con un contrato de compra anticipada o una cobertura con Glencore o Mercuria, lo que elevaría el EBITDA del escenario bajo de US$64 a US$83 millones. Segundo, los términos comerciales: negociar un cargo de tratamiento plurianual cercano a cero y un prepago para la ampliación mientras los traders compiten por concentrado. Tercero, la inflación y el tipo de cambio: indexar los contratos de contratistas a la inflación esperada y mantener la caja en dólares, convirtiendo a soles solo lo del trimestre. Cuarto, la tasa: financiar la ampliación con el flujo libre de 2026-2027 y no con deuda, posponiendo cualquier nueva reducción de capital hasta que la ampliación esté pagada. Con estas medidas, el valor esperado del EBITDA de 2027 (US$115 millones) se mantendría y el piso del escenario bajo subiría alrededor de 30%.")

# ============ SECCIÓN 3 ============
H1("Sección 3."); MARK("s3")
H2("Recomendaciones, Sugerencias y Comentarios")
SUB("1. Recomendaciones Estratégicas Macroeconómicas")
P("Recomendación R1. Fijar el precio de una parte de la producción de 2027 mientras el cobre supere US$5,50 por libra.", bold=True)
T("Variable y hallazgo: precio del cobre y crecimiento de China; el cobre está 36% sobre 2025 por una escasez que el modelo 1 considera transitoria (Sección 1, subtemas 1 y 2), y la elasticidad del EBITDA al precio es 1,55 (Sección 2, Variable 1 y canal 1). Mientras la LME supere US$5,50, OCP debería fijar el precio de 6.000 toneladas de 2027 (36% de la producción) con su comprador. Meta: un EBITDA de 2027 de al menos US$80 millones aun en el escenario bajo.")
P("Recomendación R2. Negociar términos comerciales plurianuales mientras haya escasez de concentrado.", bold=True)
T("Variable y hallazgo: demanda de los clientes y margen de las fundiciones chinas; el cargo de tratamiento es US$0 en 2026 y el spot llegó a −US$125 por tonelada (Sección 1, modelo 1; Sección 2, canal 8). Mientras el benchmark esté por debajo de US$20 por tonelada, OCP debería firmar un contrato de tres años con cargo cercano a cero y un prepago para la ampliación. Meta: evitar US$2-3 millones anuales de cargos cuando el ciclo se revierta y obtener US$30 millones de prepago para la ampliación.")
P("Recomendación R3. Indexar los costos locales a la inflación esperada y mantener la caja en dólares.", bold=True)
T("Variable y hallazgo: inflación y tipo de cambio; la inflación llegó a 5,25% con expectativas de 3,05% (Sección 1, Perú, subtema 2) y el sol fuerte resta margen a una empresa que vende en dólares (Sección 2, Variable 3). Mientras la inflación observada supere a la esperada en más de 1 pp, OCP debería atar los reajustes de sus contratistas a la expectativa del BCRP y convertir a soles solo lo del trimestre. Meta: un costo por tonelada que no supere US$57 en 2027.")
P("Recomendación R4. Financiar la ampliación con el flujo libre y no con deuda.", bold=True)
T("Variable y hallazgo: tasas de la Fed y liquidez; la Fed subió a 3,75%–4,00% y el diferencial con el BCRP es 0,375 pp (Sección 1, subtema 4), mientras el flujo libre de OCP sería US$50,9 millones en 2026P (Sección 2, canal 9). Mientras el cobre supere US$5,00, OCP debería reservar el flujo libre de 2026-2027 para la ampliación a 12.000 t/d sin nuevas reducciones de capital. Meta: ejecutar la MEIA de US$93,3 millones con una deuda/EBITDA menor a 0,5 veces.")
CAP("Tabla 14. Análisis Costo-Beneficio de las Recomendaciones (US$ millones, horizonte 2026–2027)")
APA(["Recomendación", "Costo estimado", "Beneficio estimado", "B/C"], [
    ["R1. Fijar precio de 6.000 t de 2027", "4,8 (prima o descuento de 3% sobre US$77 MM, más el costo esperado de renunciar al alza ponderado)", "19,1 en el escenario bajo × 25% de probabilidad = 4,8 esperado; más reducción de la volatilidad del EBITDA de 2027 en 19%", "1,0–2,0"],
    ["R2. Términos comerciales plurianuales", "0,5 (asesoría y exclusividad con un comprador)", "5,0 (cargos evitados de US$2,5 MM × 2 años) + menor costo de financiar la ampliación", "10,0"],
    ["R3. Costos indexados a inflación esperada", "0,3 (renegociación y cláusulas)", "2,4 (diferencia de 2,2 pp sobre US$56 MM en dos años)", "8,0"],
    ["R4. Ampliación con flujo libre", "2,0 (costo de oportunidad del dividendo diferido)", "7,5 (intereses evitados al 8% sobre US$93,3 MM, un año)", "3,8"],
    ["Total", "7,6", "19,7", "2,6"],
], [3.8, 4.4, 6.6, 1.2])
SRC("Estimaciones del grupo con base en " + EST + "; BCRPData; MEF, MMM 2027-2030. Cifras referenciales.")
INT("R2 y R3 tienen la mayor relación beneficio/costo; R1 tiene un beneficio esperado cercano a su costo, pero es la más importante porque eleva el piso del EBITDA en el escenario que más daño hace.")
SUB("2. Sugerencias Operativas con Base Macroeconómica")
T("S1. SI: el cobre LME cae por debajo de US$5,50 por libra durante dos meses seguidos o el crecimiento de China se proyecta bajo 4%: ejecutar las coberturas pendientes de R1, postergar el capex no comprometido de la ampliación y priorizar el mineral de mayor ley.")
T("S2. SI: el cargo de tratamiento de 2027 supera US$20 por tonelada: activar el contrato de R2 y licitar cada embarque entre Glencore, Mercuria, Trafigura e IXM.")
T("S3. SI: el tipo de cambio supera S/3,60 por dólar: adelantar la compra de soles para la planilla y los contratos de los próximos dos trimestres; si cae por debajo de S/3,35, convertir solo la necesidad mensual.")
T("S4. SI: la inflación de Lima supera 5,5% o el BCRP sube su tasa a 4,50%: renegociar los contratos de diésel, explosivos y transporte con tope de reajuste y revisar el plazo de pago a proveedores para no perder el financiamiento de 45 días.")
SUB("3. Comentarios Finales sobre el Entorno Macroeconómico 2026–2027")
T("C1. El entorno 2026-2028 es favorable para OCP en precio y desfavorable en costos: el cobre (US$6,14) y la plata (US$71,6) llevaron el margen EBITDA estimado a 55%, pero la inflación de 5,25%, el sol fuerte y las expectativas laborales suben un costo por tonelada que no bajará cuando el ciclo cambie.")
T("C2. El riesgo macroeconómico central es China y no el Perú: el PBI minero peruano puede caer mientras OCP gana, y viceversa. Una desaceleración china a 4% llevaría el cobre hacia US$4,50, el EBITDA de 2027 a US$64 millones y elevaría los cargos de tratamiento que hoy son cero.")
T("C3. La principal decisión de OCP es cuánto del precio de hoy asegurar para financiar su crecimiento: con un precio de equilibrio de US$2,83 por libra no está en riesgo de quiebra, pero sí de llegar a la ampliación con caja insuficiente si reparte ahora el flujo extraordinario de 2026.")

# ============ DECLARACIÓN DE IA ============
H1("Declaración de uso de Inteligencia Artificial")
T("De acuerdo con el sílabo del curso, el grupo declara el uso de herramientas de inteligencia artificial generativa en la preparación del documento, con el alcance que se detalla en la tabla 15.")
CAP("Tabla 15. Uso de Herramientas de Inteligencia Artificial en el Informe")
APA(["Herramienta", "Modalidad", "Rubros", "Temas específicos"], [
    ["Claude (Anthropic), mediante Claude Code", "Asistente de investigación, programación y revisión, bajo instrucciones del grupo", "Datos públicos, cálculos, gráficos, borrador y verificación", "Descarga de datos del MINEM y BCRPData; resumen de Veritrade; EEFF estimados y escenarios en Python; gráficos; primera versión de los párrafos y control aritmético, revisados por el grupo"],
], [3.4, 3.6, 3.6, 5.4])
SRC("Registro de uso del grupo de trabajo.")
T("El grupo definió la estructura, los supuestos de la estimación de los estados financieros, la selección de escenarios y probabilidades, y las recomendaciones. Todas las cifras fueron contrastadas con su fuente primaria, y las de OCP se presentan como estimaciones del grupo. El uso de la inteligencia artificial no sustituyó la interpretación, el análisis crítico ni las conclusiones, que son responsabilidad exclusiva de los integrantes del grupo.")

H1("Referencias")
for ref in [
    "Andina. (2022, 26 de julio). Grupo Dyer adquiere la mina Cobriza por un valor de US$ 19,7 millones. https://andina.pe/agencia/noticia-grupo-dyer-adquiere-mina-cobriza-un-valor-197-millones-903195.aspx",
    "Banco Central de Reserva del Perú. (2025). Huancavelica: Síntesis de actividad económica, julio 2025. Sucursal Huancayo. https://www.bcrp.gob.pe/docs/Sucursales/Huancayo/2025/presentacion-huancavelica-07-2025.pdf",
    "Banco Central de Reserva del Perú. (2026a). Reporte de Inflación, setiembre de 2026. https://www.bcrp.gob.pe/publicaciones/reporte-de-inflacion.html",
    "Banco Central de Reserva del Perú. (2026b). BCRPData: Series estadísticas [Base de datos]. Consultado el 13 de noviembre de 2026. https://estadisticas.bcrp.gob.pe",
    "El Peruano. (2024, noviembre). Aviso de reducción de capital de Operadores Concentrados Peruanos S.A.C. (junta general del 24 de setiembre de 2024). Boletín Oficial del Diario Oficial El Peruano.",
    "Energiminas. (2023, 27 de diciembre). Mina Cobriza: Grupo Dyer Coriat planea destinar US$ 93,3 millones para plan de minado y optimización. https://energiminas.com/2023/12/27/mina-cobriza-grupo-dyer-coriat-planea-destinarus-93-3-millones-para-plan-de-minado-y-optimizacion",
    "Fastmarkets. (2026). Mercuria, Glencore secure future copper concentrate supply with at least $450 mln in offtake deals. https://www.fastmarkets.com/insights/mercuria-glencore-copper-offtake-deals/",
    "Federal Reserve. (2026). Open market operations: Policy rate changes. federalreserve.gov",
    "Glencore Perú. (2026). Perubar: Unidad logística. glencoreperu.pe",
    "Mining.com. (2025, 30 de diciembre). Mercuria signs copper concentrate offtake agreement with Bulgarian miner. https://www.mining.com/web/mercuria-signs-copper-concentrate-offtake-agreement-with-bulgarian-miner/",
    "Ministerio de Economía y Finanzas. (2026). Marco Macroeconómico Multianual 2027-2030 y cuadros estadísticos. Lima: MEF.",
    "SINIA/MINAM. (s. f.). Informe final de la Segunda Modificación del Plan de Cierre de Mina de la UM Cobriza. https://sinia.minam.gob.pe/sites/default/files/siar-huancavelica/archivos/public/docs/informe_final_de_la_smpcm_-_um_cobriza2.pdf",
    "Datos Perú. (2026). Operadores Concentrados Peruanos S.A.C.: trabajadores por mes. https://www.datosperu.org/empresa-operadores-concentrados-peruanos-sac-20608321731.php",
    "Ministerio de Energía y Minas. (2026). Producción minera: producción minera metálica por titular y unidad, 2023, 2024, 2025 y enero-agosto 2026 [Conjunto de datos]. https://www.gob.pe/institucion/minem/informes-publicaciones/5472883-produccion-minera",
    "Nexa Resources. (2026). 2025 production, sales and costs guidance and 2026-2028 outlook. https://www.newsfilecorp.com/release/282981",
    "OEFA. (2025a). Resolución Directoral N.° 0155-2025-OEFA/DFAI. https://cdn.www.gob.pe/uploads/document/file/8226264/6871962-resolucion-n-0155-2025-oefa-dfai.pdf",
    "OEFA. (2025b). Resolución Directoral N.° 01807-2025-OEFA/DFAI. https://cdn.www.gob.pe/uploads/document/file/9465822/7750663-resolucion-n-1807-2025-oefa-dfai.pdf",
    "Proactivo. (2022). Grupo Dyer Coriat toma control de mina Cobriza y recontratará a más de 600 trabajadores. proactivo.com.pe",
    "Proactivo. (2025). Senace aprueba octavo ITS de Cobriza con inversión de US$ 8,25 millones. proactivo.com.pe",
    "Skillings. (2026). Copper price forecast 2026: Smelter treatment charges fall below $20. https://www.skillings.net/copper-price-forecast-2026-smelter-treatment-charges-fall-below-20/",
    "SUNAT. (2024). Resolución N.° 000009-2024/SUNAT, anexo 1: Principales Contribuyentes Nacionales. https://www.sunat.gob.pe/legislacion/superin/2024/anexo1-000009-2024.pdf",
    "Veritrade. (2026). Perú – Importaciones: importador Operadores Concentrados Peruanos S.A.C., enero 2019 – noviembre 2026 [Base de datos con información de SUNAT].",
    "Volcan Compañía Minera. (2026). Análisis y discusión de la gerencia, 4T25 a 3T26. Latibex.",
]:
    p = P(ref); p.paragraph_format.left_indent = Cm(1.27); p.paragraph_format.first_line_indent = Cm(-1.27)

doc.save(OUT)
print("saved", OUT)

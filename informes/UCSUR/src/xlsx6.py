import re, os, sys, ast
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
S = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]

# ---------------- Cadenas (formato ElRocio) ----------------
src = open(os.path.join(S, "build6.py"), encoding="utf-8").read()
# delimitar secciones por marcadores
cuts = {"s1int": src.index('MARK("s1int")'), "s1peru": src.index('MARK("s1peru")'), "s2desc": src.index('MARK("s2desc")'), "s2imp": src.index('MARK("s2imp")')}
pat = re.compile(r'CADENA\("([^"]+)",\s*\n\s*(\[.*?\]),\s*\n\s*"([^"]*)"', re.S)
chains = []
for m in pat.finditer(src):
    pos = m.start(); sec = "s1int" if pos < cuts["s1peru"] else "s1peru" if pos < cuts["s2desc"] else "s2imp"
    chains.append((sec, m.group(1), ast.literal_eval(m.group(2)), m.group(3)))
wb = Workbook(); ws = wb.active; ws.title = "Cadenas de Razonamiento"
for i, col in enumerate("ABCDEFGHIJK"): ws.column_dimensions[col].width = 22 if i % 2 == 0 else 3
ws["A1"] = "UNIVERSIDAD CIENTÍFICA DEL SUR S.A.C. — CADENAS DE RAZONAMIENTO MACROECONÓMICO 2026-2028"; ws["A1"].font = Font(name="Calibri", bold=True, size=13)
ws["A2"] = "Fuente: BCRP RI setiembre 2026 / BCRPData (consulta 13-nov-2026) / INEI / Federal Reserve / UCSUR EEFF auditados 2023-2025"; ws["A2"].font = Font(name="Calibri", size=8)
titles = {"s1int": "■  SECCIÓN 1 — INTERNACIONAL", "s1peru": "■  SECCIÓN 1 — PERÚ", "s2imp": "■  SECCIÓN 2 — IMPACTO SOBRE UCSUR (9 CANALES)"}
F_FIRST, F_MID, F_LAST = "FFDDEEFF", "FFE2EFDA", "FFF2F2F2"
r = 4; cur = None
for sec, title, elems, nota in chains:
    if sec != cur:
        r += 1; ws.cell(r, 1, titles[sec]).font = Font(name="Calibri", bold=True, size=11); r += 2; cur = sec
    ws.cell(r, 1, title).font = Font(name="Calibri", bold=True, size=10); r += 1
    n = len(elems)
    for k, (no, ci) in enumerate(elems):
        col = 1 + 2 * k
        fill = PatternFill("solid", fgColor=F_FIRST if k == 0 else F_LAST if k == n - 1 else F_MID)
        sym = no[0] if no[0] in "↑↓" else "→"
        c = ws.cell(r, col, sym); c.font = Font(name="Calibri", bold=True, size=13); c.fill = fill; c.alignment = Alignment(horizontal="center")
        txt = (no[1:] if no[0] in "↑↓" else no).strip() + "\n" + ci
        c = ws.cell(r + 1, col, txt); c.font = Font(name="Calibri", size=9); c.fill = fill; c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
        if k < n - 1:
            a = ws.cell(r, col + 1, "→"); a.font = Font(name="Calibri", bold=True, size=14); a.alignment = Alignment(horizontal="center")
    ws.row_dimensions[r + 1].height = 72
    c = ws.cell(r + 2, 1, nota); c.font = Font(name="Calibri", size=9, italic=True); c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r + 2, start_column=1, end_row=r + 2, end_column=11); ws.row_dimensions[r + 2].height = 30
    r += 5
wb.save(os.path.join(OUT, "UCSUR_Cadenas_Razonamiento.xlsx"))
print("cadenas", len(chains))

# ---------------- EEFF (formato minera corona) ----------------
HDR = PatternFill("solid", fgColor="FFBEBEBE"); SUBT = PatternFill("solid", fgColor="FFD3D3D3"); WH = PatternFill("solid", fgColor="FFFFFFFF")
def sheet(ws, title, years, rows, start_col=1, note_col=False):
    c0 = start_col
    hdr = [title] + (["NOTA"] if note_col else []) + years
    for j, h in enumerate(hdr):
        c = ws.cell(1, c0 + j, h); c.font = Font(name="Calibri", bold=True, size=9); c.fill = HDR
    for i, row in enumerate(rows, 2):
        label, *rest = row
        bold = label.isupper() or label.startswith("Total") or label.startswith("Utilidad") or label.startswith("Flujo") or label.startswith("Activo") or label.startswith("Pasivo") or label.startswith("Patrimonio") or label.startswith("Efectivo neto") or label.startswith("Saldo")
        vals = rest
        for j, v in enumerate([label] + vals):
            c = ws.cell(i, c0 + j, v); c.font = Font(name="Calibri", bold=bold, size=8); c.fill = SUBT if bold else WH
            if isinstance(v, (int, float)): c.number_format = "#,##0"
    ws.column_dimensions["A"].width = 46
    for col in "BCDEFG": ws.column_dimensions[col].width = 12

k = lambda *v: [round(x) for x in v]
wb = Workbook(); ws = wb.active; ws.title = "Hoja1"
Y = ["2025", "2024", "2023", "2022"]
bg = [
    ["Activos"] + [0] * 4, ["Activos Corrientes"] + [0] * 4,
    ["Efectivo y Equivalentes al Efectivo (n. 3)"] + k(139350.536, 75415.304, 9752.154, 6133.115),
    ["Inversiones Financieras (n. 7)"] + k(38258.421, 38889.967, 31356.245, 30525.084),
    ["Derechos de Enseñanza por Cobrar, neto (n. 4)"] + k(48807.901, 20413.436, 17663.775, 13447.361),
    ["Cuentas por Cobrar a Relacionadas (n. 23(c))"] + k(2686.916, 4349.823, 4665.291, 3025.014),
    ["Otras Cuentas por Cobrar, neto (n. 5)"] + k(2530.617, 13315.555, 6150.655, 13037.076),
    ["Textos y Útiles, Materiales y Suministros"] + k(0, 0, 255.901, 298.237),
    ["Gastos Pagados por Anticipado (n. 6)"] + k(4071.499, 3399.380, 3839.050, 2343.544),
    ["Total Activos Corrientes"] + k(235705.890, 155783.465, 73683.071, 68809.431),
    ["Activos No Corrientes"] + [0] * 4,
    ["Gastos Pagados por Anticipado (n. 6)"] + k(537.598, 257.203, 0, 0),
    ["Cuentas por Cobrar a Relacionadas (n. 23(c))"] + k(3106.043, 4432.540, 4235.537, 4942.870),
    ["Otras Cuentas por Cobrar, neto (n. 5)"] + k(176.941, 1036.434, 1087.551, 1042.066),
    ["Inversiones Financieras"] + k(0, 0, 4521.687, 4399.573),
    ["Inmuebles, Mobiliario y Equipo, neto (n. 9)"] + k(349744.621, 290925.722, 207067.022, 210312.512),
    ["Activos Intangibles, neto"] + k(3615.014, 1638.819, 881.702, 999.283),
    ["Activos Biológicos"] + k(10.325, 32.118, 50.975, 22.500),
    ["Activos por Derecho de Uso, neto (n. 8)"] + k(167263.820, 132619.377, 139124.166, 98839.756),
    ["Total Activos No Corrientes"] + k(524454.362, 430942.213, 356968.640, 320558.560),
    ["TOTAL DE ACTIVOS"] + k(760160.252, 586725.678, 430651.711, 389367.991),
    ["Pasivos y Patrimonio"] + [0] * 4, ["Pasivos Corrientes"] + [0] * 4,
    ["Obligaciones Financieras (n. 13)"] + k(25517.741, 17657.359, 12273.410, 15090.697),
    ["Cuentas por Pagar Comerciales (n. 10)"] + k(39959.528, 24911.992, 25862.993, 23117.420),
    ["Cuentas por Pagar a Relacionadas (n. 23(c))"] + k(1229.506, 1835.246, 899.963, 1655.447),
    ["Tributos, Remuneraciones y Otras Cuentas por Pagar (n. 11)"] + k(90055.120, 59544.794, 37591.495, 33719.204),
    ["Pasivos por Arrendamiento (n. 12)"] + k(8061.425, 12098.451, 9183.601, 9807.616),
    ["Total Pasivos Corrientes"] + k(164823.320, 116047.842, 85811.462, 83390.384),
    ["Pasivos No Corrientes"] + [0] * 4,
    ["Obligaciones Financieras (n. 13)"] + k(147249.214, 113633.351, 100864.315, 73871.014),
    ["Pasivos por Arrendamiento (n. 12)"] + k(94827.055, 130496.366, 80772.211, 88575.047),
    ["Pasivo por Impuesto a la Renta Diferido (n. 14)"] + k(2685.250, 5070.310, 4896.090, 3622.234),
    ["Total Pasivos No Corrientes"] + k(244761.519, 249200.027, 186532.616, 166068.295),
    ["Total Pasivos"] + k(409584.839, 365247.869, 272344.078, 249458.679),
    ["Patrimonio (n. 15)"] + [0] * 4,
    ["Capital Social"] + k(64297.518, 64297.518, 64297.518, 64297.518),
    ["Capital Adicional"] + k(269.045, 269.045, 269.045, 269.045),
    ["Reserva Legal"] + k(12859.504, 12859.504, 12859.504, 12859.504),
    ["Resultados Acumulados"] + k(273149.346, 144051.742, 80881.566, 62483.245),
    ["Total Patrimonio"] + k(350575.413, 221477.809, 158307.633, 139909.312),
    ["TOTAL PASIVO Y PATRIMONIO"] + k(760160.252, 586725.678, 430651.711, 389367.991),
]
sheet(ws, "BG UCSUR MILES DE SOLES", Y, bg)
ws.cell(len(bg) + 3, 1, "Fuente: UCSUR, EEFF auditados 2023 (2023 y 2022) y 2025 (2025 y 2024, comparativo reexpresado). n. = nota citada en los estados.").font = Font(name="Calibri", size=8, italic=True)

ws2 = wb.create_sheet("Hoja2")
egp = [
    ["Ingresos por Derechos de Enseñanza (n. 17)"] + k(594839.418, 420436.230, 321787.880, 264107.390),
    ["Gastos de Personal Docente y Administrativo (n. 18)"] + k(-214660.501, -169468.096, -152532.560, -116839.698),
    ["Gastos Generales de Operación y Administración (n. 19)"] + k(-128161.320, -108792.130, -94707.396, -78434.487),
    ["Depreciación y Amortización"] + k(-35684.917, -32374.616, -23167.933, -16091.249),
    ["Provisiones (n. 20)"] + k(-7275.196, -6210.661, -3683.209, -2182.161),
    ["Otros Ingresos (n. 22)"] + k(10417.150, 17529.070, 3140.930, 4397.286),
    ["Utilidad de Operación"] + k(219474.634, 121119.797, 50837.712, 54957.081),
    ["Ingresos Financieros (n. 21)"] + k(10149.716, 10066.861, 8793.900, 1256.490),
    ["Gastos Financieros (n. 21)"] + k(-27514.999, -27183.483, -22992.709, -16915.079),
    ["Diferencia de Cambio, neta (n. 25.1(ii))"] + k(-1732.243, -382.742, -117.757, -0.884),
    ["Utilidad antes de Impuestos"] + k(200377.108, 103620.433, 36521.146, 39297.608),
    ["Gasto por Impuesto a las Ganancias (n. 14(c))"] + k(-58745.277, -27096.357, -14503.111, -14310.651),
    ["Utilidad Neta del Ejercicio"] + k(141631.831, 76524.076, 22018.035, 24986.957),
]
sheet(ws2, "EGP UCSUR MILES DE SOLES", Y, egp)
side = [("Sector", "2022", "2023", "2024", "2025"), ("Otros servicios (incl. educación), var. %", 3.4, 2.3, 3.6, 4.0), ("Producto Bruto Interno, var. %", 2.8, -0.4, 3.5, 3.4),
        ("Consumo privado, var. %", 3.6, 0.1, 2.8, 3.6), ("Ingresos reales UCSUR, var. %", None, 14.7, 27.7, 39.4), ("Elasticidad ingresos / otros servicios", None, 6.4, 7.7, 9.9)]
for i, row in enumerate(side):
    for j, v in enumerate(row):
        c = ws2.cell(3 + i, 8 + j, v); c.font = Font(name="Calibri", size=11, bold=(i == 0 or j == 0 and False))
ws2.column_dimensions["H"].width = 40
ws2.cell(10, 8, "Fuente: INEI; BCRPData; UCSUR, EEFF auditados.").font = Font(name="Calibri", size=8, italic=True)

ws3 = wb.create_sheet("Hoja3")
fl = [
    ["Flujo de Efectivo de Actividades de Operación", "", 0, 0, 0, 0],
    ["Utilidad Neta del Ejercicio", "", *k(141631.831, 76524.076, 22018.035, 24986.957)],
    ["Estimación para Pérdidas Crediticias Esperadas", "4(d)", *k(6532.323, 5299.960, 3567.181, 1680.567)],
    ["Depreciación de Activos por Derecho de Uso", "8(a)", *k(15558.092, 14925.023, 12796.874, 9653.341)],
    ["Depreciación de Inmuebles, Mobiliario y Equipo", "9(a)", *k(19779.034, 17275.420, 10235.411, 6305.810)],
    ["Intereses Devengados por Pasivo por Arrendamiento", "12(c)", *k(12009.106, 11687.494, 0, 0)],
    ["Castigos de Derechos de Enseñanza por Cobrar", "4(d)", *k(-3689.345, -2005.365, -700.097, -3134.703)],
    ["(Aumento) de Derechos de Enseñanza por Cobrar", "", *k(-31237.443, -6044.256, -7083.498, -1219.263)],
    ["Aumento (Disminución) de Cuentas por Pagar Comerciales", "", *k(15047.536, -951.001, 2745.573, 9609.848)],
    ["Flujo de Efectivo Neto de Actividades de Operación", "", *k(230600.789, 141661.372, 50243.670, 61318.159)],
    ["Flujo de Efectivo de Actividades de Inversión", "", 0, 0, 0, 0],
    ["Compra de Activos Fijos", "9(a)", *k(-82530.016, -46187.283, -58551.005, -61178.288)],
    ["Flujo de Efectivo Neto de Actividades de Inversión", "", *k(-84857.853, -46967.533, -60668.584, -53492.991)],
    ["Flujo de Efectivo de Actividades de Financiamiento", "", 0, 0, 0, 0],
    ["Fondos Recibidos de Obligaciones Financieras", "25.4", *k(61660.000, 41328.512, 130094.594, 4118.590)],
    ["Amortización de Obligaciones Financieras", "25.4", *k(-30648.956, -33602.386, -105918.580, -8124.193)],
    ["Pago de Pasivos por Arrendamiento", "12(c)", *k(-24857.132, -23518.555, -10132.061, -8971.063)],
    ["Pago Anticipado de Cuotas de Arrendamiento", "8(c)", *k(-77263.690, 0, 0, 0)],
    ["Dividendos Pagados (2023: en actividades de operación)", "15(d)", *k(-12534.227, -13356.725, -3619.714, 0)],
    ["Flujo de Efectivo Neto de Actividades de Financiamiento", "", *k(-81807.704, -29030.689, 14043.953, -11321.219)],
    ["Efectivo Neto: Aumento (Disminución)", "", *k(63935.232, 65663.150, 3619.039, -3496.051)],
    ["Saldo de Efectivo al Final del Año", "3", *k(139350.536, 75415.304, 9752.154, 6133.115)],
]
sheet(ws3, "CUENTA", Y, fl, note_col=True)
ws3.column_dimensions["A"].width = 52

ws4 = wb.create_sheet("Ratios")
rat = [
    ["Margen operativo (%)", 36.9, 28.8, 15.8, 20.8], ["Margen neto (%)", 23.8, 18.2, 6.8, 9.5],
    ["Gastos de personal / ingresos (%)", 36.1, 40.3, 47.4, 44.2], ["Días de cobro (CxC / ingresos × 365)", 30, 18, 20, 19],
    ["Días de pago (CxP comerciales / gastos generales × 365)", 114, 84, 100, 108], ["Liquidez corriente (veces)", 1.43, 1.34, 0.86, 0.83],
    ["Pasivo total / patrimonio (veces)", 1.17, 1.65, 1.72, 1.78], ["Obligaciones financieras / patrimonio (veces)", 0.49, 0.59, 0.71, 0.64],
    ["ROE (%)", 40.4, 34.5, 13.9, 17.9], ["Rotación del activo (veces)", 0.78, 0.72, 0.75, 0.68],
    ["Flujo libre (operación − capex), S/ miles", *k(148070.773, 95474.089, -8307.335, 139.871)],
]
sheet(ws4, "RATIOS UCSUR", Y, rat)
for row in ws4.iter_rows(min_row=2, max_row=len(rat) + 1, min_col=2, max_col=5):
    for c in row:
        if isinstance(c.value, float): c.number_format = "0.00" if c.value < 3 else "0.0"
wb.save(os.path.join(OUT, "UCSUR_EEFF.xlsx"))
print("eeff ok")

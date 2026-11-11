import os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
S = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(S, "fig2")
exec(open(os.path.join(S, "charts3.py")).read().split("# g13 resultados UCSUR")[0])
exec("def ishikawa" + open(os.path.join(S, "charts3.py")).read().split("def ishikawa")[1].split("ishikawa(\"i3.png\"")[0])

# g15 PBI total, otros servicios (incl. educación) y consumo privado
yrs = ["2022", "2023", "2024", "2025", "2026*"]
pbi = [2.8, -0.4, 3.5, 3.4, 3.1]; os_ = [3.4, 2.3, 3.6, 4.0, 4.6]; cp = [3.6, 0.1, 2.8, 3.6, 3.6]
fig, ax = plt.subplots(figsize=(7.5, 3.6)); x = np.arange(5); w = 0.27
for i, (v, c, l) in enumerate([(pbi, GR, "PBI total"), (os_, AZ, "Otros servicios (incluye educación pública y privada)"), (cp, CEL, "Consumo privado")]):
    ax.bar(x + (i - 1) * w, v, w, color=c, label=l)
    for xi, vi in zip(x + (i - 1) * w, v): vl(ax, xi, max(vi, 0), f1(vi))
ax.axhline(0, color="k", lw=0.8); ax.set_xticks(x); ax.set_xticklabels(yrs); ax.set_ylabel("var. % real"); ax.set_ylim(-1.5, 6.5)
ax.legend(frameon=False, fontsize=9, loc="upper left"); save(fig, "g15.png")

# g16 tasa Fed vs BCRP
def L(c):
    d = json.load(open(os.path.join(S, "bcrp", c))); return [(p["name"], float(p["values"][0])) for p in d["periods"] if p["values"][0] != "n.d."]
br = [p for p in L("H_PD04722MM.json") if p[0][-4:] in ("2024", "2025", "2026")]
fedmid = {}
def setfed(start, val):
    fedmid[start] = val
steps = [("Ene.2024", 5.375), ("Sep.2024", 4.875), ("Nov.2024", 4.625), ("Dic.2024", 4.375), ("Set.2025", 4.125), ("Oct.2025", 3.875), ("Dic.2025", 3.625), ("Set.2026", 3.875)]
mon = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
fv = []; cur = 5.375
stepd = {s.replace("Set", "Sep"): v for s, v in steps}
for n, _ in br:
    if n in stepd: cur = stepd[n]
    fv.append(cur)
fig, ax = plt.subplots(figsize=(7.5, 3.4)); xs = list(range(len(br)))
ax.step(xs, [v for _, v in br], where="post", color=AZ, lw=2, label="Tasa de referencia BCRP")
ax.step(xs, fv, where="post", color=RO, lw=2, label="Fed, punto medio del rango")
ax.fill_between(xs, fv, [v for _, v in br], step="post", color=NA, alpha=0.15, label="Diferencial")
ax.annotate("0,375 pp", (xs[-1], 4.06), xytext=(-40, 18), textcoords="offset points", fontsize=9, color=NA)
lab = lambda n: f"{n.split('.')[0]}-{n.split('.')[1][2:]}"
ax.set_xticks(xs[::3]); ax.set_xticklabels([lab(n) for n, _ in br][::3], rotation=45); ax.set_ylabel("%"); ax.set_ylim(3, 7)
ax.legend(frameon=False, fontsize=9, loc="upper right"); save(fig, "g16.png")

# g17 costos de UCSUR vs inflación
yy = ["2022", "2023", "2024", "2025"]; per = [116.8, 152.5, 169.5, 214.7]; gg = [78.4, 94.7, 108.8, 128.2]; inf = [7.9, 6.3, 2.4, 1.5]
fig, ax = plt.subplots(figsize=(7.5, 3.4)); x = np.arange(4)
ax.bar(x, per, 0.55, color=AZ, label="Gastos de personal (nota 18)"); ax.bar(x, gg, 0.55, bottom=per, color="#9dc3e6", label="Gastos generales (nota 19)")
for xi, a, b in zip(x, per, gg): vl(ax, xi, a + b, f1(a + b))
ax.set_xticks(x); ax.set_xticklabels(yy); ax.set_ylabel("S/ millones"); ax.set_ylim(0, 420)
ax2 = ax.twinx(); ax2.plot(x, inf, color=RO, marker="o", label="Inflación promedio de Lima, % (eje der.)"); ax2.set_ylim(0, 10); ax2.grid(False); ax2.spines["right"].set_visible(True)
for xi, v in zip(x, inf): ax2.annotate(f1(v), (xi, v), xytext=(8, 2), textcoords="offset points", color=RO, fontsize=9)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=9, loc="upper left")
save(fig, "g17.png")

# g19 diferencia de cambio vs tipo de cambio de diciembre
tcd = [3.829, 3.734, 3.735, 3.367]; dc = [0.0, 0.1, 0.4, 1.7]
fig, ax = plt.subplots(figsize=(7.5, 3.4))
ax.bar(x, dc, 0.5, color=RO, label="Pérdida por diferencia de cambio (S/ MM, nota 25.1(ii))")
for xi, v in zip(x, dc): vl(ax, xi, v, f1(v))
ax.set_xticks(x); ax.set_xticklabels(yy); ax.set_ylabel("S/ millones"); ax.set_ylim(0, 2.6)
ax2 = ax.twinx(); ax2.plot(x, tcd, color=AZ, marker="o", label="Tipo de cambio promedio de diciembre (eje der.)"); ax2.set_ylim(3.0, 4.0); ax2.grid(False); ax2.spines["right"].set_visible(True)
for xi, v in zip(x, tcd): ax2.annotate(f1(v, 3), (xi, v), xytext=(8, 4), textcoords="offset points", color=AZ, fontsize=9)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=9, loc="center left")
save(fig, "g19.png")

# g14 (nueva) proyección con PBI de educación
hist = {2022: 264.1, 2023: 321.8, 2024: 420.4, 2025: 594.8}
esc = {"Techo (ε = 8,0)": ([841.4, 1112.3, 1470.4], RO), "Base (ε = 4,0)": ([733.8, 859.2, 1006.1], AZ), "Prudente (ε = 1,5)": ([666.5, 717.5, 772.5], VE)}
sv = {2022: 3.4, 2023: 2.3, 2024: 3.6, 2025: 4.0, 2026: 4.3, 2027: 3.7, 2028: 3.7}
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.bar(list(hist), list(hist.values()), color="#9dc3e6", label="Ingresos observados (S/ MM)")
for k, v in hist.items(): vl(ax, k, v, f1(v))
for name, (v, c) in esc.items():
    ax.plot([2025, 2026, 2027, 2028], [594.8] + v, marker="o", color=c, label=name)
    ax.annotate(f1(v[-1]), (2028, v[-1]), xytext=(6, -3), textcoords="offset points", fontsize=9, color=c)
ax.set_ylabel("S/ millones"); ax.set_ylim(0, 1650); ax.set_xlim(2021.4, 2028.8)
ax2 = ax.twinx(); ax2.plot(list(sv), list(sv.values()), color=GR, ls="--", marker="s", ms=4, label="PBI de servicios/educación, var. % (eje der.)")
ax2.set_ylim(0, 12); ax2.grid(False); ax2.spines["right"].set_visible(True)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left", fontsize=9)
save(fig, "g14b.png")

ishikawa("i5.png", "Ventas de\nUCSUR\n(Variable 1)", [
    ("PBI de educación", ["Otros servicios 4,0% (2025)", "Educación privada 4,2% (I-26)", "ε = 8,0"], VE),
    ("Consumo privado", ["3,6% (2026P)", "3,0% (2027P)", "65,6% del PBI"], VE),
    ("Participación", ["Licencia 2018", "Nuevas carreras", "Nuevos locales (2021)"], VE),
    ("Precio", ["Servicios +5,3% (2026P)", "Ingreso real −4,0%", "Reajuste de pensiones"], RO),
    ("Becas y fiscal", ["G 3,2% → 2,3%", "Pronabec", "Déficit 1,5%"], GR),
    ("Riesgos", ["El Niño", "Desempleo juvenil 11,3%", "Deserción"], RO)])
ishikawa("i6.png", "Costos de\nUCSUR\n(Variable 2)", [
    ("Energía", ["WTI US$98,9", "Tarifas eléctricas", "Pasajes"], RO),
    ("Salarios", ["Personal S/214,7 MM", "Reajustes 2027", "36,1% de ingresos"], RO),
    ("Servicios", ["Generales S/128,2 MM", "Servicios +5,3% (2026P)", "Proveedores CxP +60,4%"], RO),
    ("Expectativas", ["Eπ 3,05%", "Meta 1%–3%", "π 2027P 2,0%"], GR),
    ("Equipamiento", ["Importado +5,1%", "Capex S/82,5 MM", "Licencias en US$"], GR),
    ("Traslado a precio", ["Elasticidad alta", "Ingreso real −4,0%", "Margen 36,9%"], VE)])
ishikawa("i7.png", "Exposición\ncambiaria de UCSUR\n(Variable 3)", [
    ("Fed", ["3,75%–4,00%", "PCE 3,7%", "Diferencial 0,375 pp"], RO),
    ("Balanza de pagos", ["CA +4,0% del PBI", "Saldo US$48.865 MM", "TI +18,1%"], VE),
    ("BCRP", ["Compras US$15.715 MM", "RIN US$96.668 MM", "TC S/3,412"], VE),
    ("Pasivos en US$", ["Dif. cambio −S/1,7 MM", "Nota 25.1(ii)", "Arrendamientos"], RO),
    ("Capex importado", ["S/82,5 MM (2025)", "+5,1% en soles", "Escenario S/3,60: +10,9%"], RO),
    ("Ingresos", ["100% en soles", "Sin exportación", "Cobertura natural nula"], GR)])
ishikawa("i8.png", "Costo financiero\nde UCSUR\n(Variable 4)", [
    ("Tasa BCRP", ["4,25% desde set-25", "r ex ante 1,20%", "r ex post −1,00%"], GR),
    ("Deuda", ["S/172,8 MM (nota 13)", "No corriente S/147,2 MM", "Costo implícito 10,2%"], RO),
    ("Arrendamientos", ["S/102,9 MM (nota 12)", "Intereses S/12,0 MM", "Prepago S/77,3 MM"], GR),
    ("Liquidez propia", ["Caja S/139,4 MM", "Ingresos fin. S/10,1 MM", "Inversiones S/38,3 MM"], VE),
    ("Crédito a familias", ["Consumo +13,2%", "CxC S/48,8 MM", "30 días de cobro"], RO),
    ("Sensibilidad", ["+25 pb = S/0,43 MM", "+50 pb = S/0,86 MM", "Gastos fin. S/27,5 MM"], RO)])
print("ok")

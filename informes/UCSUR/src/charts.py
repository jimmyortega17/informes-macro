import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np

S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, "fig"); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.3, "figure.dpi": 100})
AZ, RO, GR, NA, VE = "#1f4e79", "#c00000", "#7f7f7f", "#d97a00", "#2e7d32"

def L(code, pref="L_"):
    d = json.load(open(os.path.join(S, "bcrp", f"{pref}{code}.json")))
    return [(p["name"], float(p["values"][0])) for p in d["periods"] if p["values"][0] != "n.d."]

def lab(n):  # 'Ene.2026' -> 'Ene-26'
    m, y = n.split("."); return f"{m}-{y[2:]}"

def save(fig, name):
    fig.tight_layout(); fig.savefig(os.path.join(OUT, name), dpi=200); plt.close(fig)

def vl(ax, x, y, t, **k):
    ax.annotate(t, (x, y), textcoords="offset points", xytext=(0, 4), ha="center", fontsize=8, **k)

# G1 crecimiento mundial
eco = ["Mundo", "EE.UU.", "Eurozona", "China", "América Latina", "Perú"]
g25 = [3.4, 2.1, 1.4, 5.0, 2.4, 3.4]; g26 = [3.1, 2.2, 1.0, 4.5, 2.2, 3.2]; g27 = [3.1, 2.2, 1.3, 4.2, 2.4, 3.0]
fig, ax = plt.subplots(figsize=(7.5, 3.6)); x = np.arange(len(eco)); w = 0.27
for i, (v, c, l) in enumerate([(g25, "#9dc3e6", "2025"), (g26, AZ, "2026P"), (g27, NA, "2027P")]):
    b = ax.bar(x + (i - 1) * w, v, w, color=c, label=l)
    for xi, vi in zip(x + (i - 1) * w, v): vl(ax, xi, vi, f"{vi:.1f}".replace(".", ","))
ax.set_xticks(x); ax.set_xticklabels(eco); ax.set_ylabel("var. % real"); ax.legend(frameon=False, ncol=3); ax.set_ylim(0, 6)
save(fig, "g1.png")

# G2 WTI y cobre
w_ = L("PN01660XM"); c_ = L("PN01652XM")
w_ = [p for p in w_ if p[0].endswith(("2025", "2026"))]; c_ = [p for p in c_ if p[0].endswith(("2025", "2026"))]
fig, ax = plt.subplots(figsize=(7.5, 3.6)); xs = range(len(w_))
ax.plot(xs, [v for _, v in w_], color=RO, marker="o", ms=3, label="Petróleo WTI (US$/barril, eje izq.)")
ax.axhline(82, color=RO, ls="--", lw=1); ax.text(0, 83.5, "Supuesto RI set-26 para 2026: US$82", color=RO, fontsize=8)
ax2 = ax.twinx(); ax2.plot(xs, [v / 100 for _, v in c_], color=NA, marker="s", ms=3, label="Cobre LME (US$/lb, eje der.)")
ax2.spines["right"].set_visible(True); ax2.grid(False)
ax.set_xticks(list(xs)[::2]); ax.set_xticklabels([lab(n) for n, _ in w_][::2], rotation=45)
vl(ax, len(w_) - 1, w_[-1][1], f"{w_[-1][1]:.1f}".replace(".", ","), color=RO)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left", fontsize=8)
ax.set_ylim(50, 110); ax2.set_ylim(3, 7.5)
save(fig, "g2.png")

# G3 UCSUR resultados
yrs = ["2022", "2023", "2024", "2025"]; ing = [264.1, 321.8, 420.4, 594.8]; uop = [55.0, 50.8, 121.1, 219.5]; un = [25.0, 22.0, 76.5, 141.6]
fig, ax = plt.subplots(figsize=(7.5, 3.6)); x = np.arange(4); w = 0.27
for i, (v, c, l) in enumerate([(ing, AZ, "Ingresos por derechos de enseñanza"), (uop, NA, "Utilidad de operación"), (un, VE, "Utilidad neta")]):
    ax.bar(x + (i - 1) * w, v, w, color=c, label=l)
    for xi, vi in zip(x + (i - 1) * w, v): vl(ax, xi, vi, f"{vi:.0f}")
ax.set_xticks(x); ax.set_xticklabels(yrs); ax.set_ylabel("S/ millones"); ax.set_ylim(0, 680)
ax2 = ax.twinx(); mg = [u / i * 100 for u, i in zip(uop, ing)]; ax2.plot(x, mg, color=RO, marker="o", label="Margen operativo % (eje der.)")
for xi, m in zip(x, mg): ax2.annotate(f"{m:.1f}%".replace(".", ","), (xi, m), xytext=(10, -2), textcoords="offset points", color=RO, fontsize=8)
ax2.set_ylim(0, 45); ax2.grid(False); ax2.spines["right"].set_visible(True)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left", fontsize=8)
save(fig, "g3.png")

# G4 tipo de cambio
tc = [p for p in L("PN01210PM") if p[0].endswith(("2025", "2026"))]
fig, ax = plt.subplots(figsize=(7.5, 3.4)); xs = list(range(len(tc)))
ax.plot(xs, [v for _, v in tc], color=AZ, marker="o", ms=3, label="Tipo de cambio bancario, promedio mensual")
ax.plot([xs[-1], xs[-1] + 1], [tc[-1][1], 3.412], color=AZ, ls=":", marker="D", ms=4)
ax.annotate("3,412 (9-nov-26)", (xs[-1] + 1, 3.412), xytext=(-10, -30), textcoords="offset points", fontsize=8, ha="center")
ax.fill_between([xs[-1] + 1, xs[-1] + 3], 3.40, 3.50, color=NA, alpha=0.25, label="Rango esperado S/3,40–3,50")
ax.set_xticks(xs[::2]); ax.set_xticklabels([lab(n) for n, _ in tc][::2], rotation=45); ax.set_ylabel("S/ por US$")
for i in [0, 11, len(tc) - 1]: vl(ax, i, tc[i][1], f"{tc[i][1]:.3f}".replace(".", ","))
ax.legend(frameon=False, fontsize=8, loc="upper right"); ax.set_ylim(3.25, 3.85)
save(fig, "g4.png")

# G5 costo de equipo importado
esc = ["Dic-25\n(TC 3,367)", "Nov-26\n(TC 3,412)", "TC 3,50", "TC 3,60"]
tcs = [3.367, 3.412, 3.50, 3.60]; base = [1.0 * tcs[0]] + [1.037 * t for t in tcs[1:]]
fig, ax = plt.subplots(figsize=(7.5, 3.4)); b = ax.bar(esc, base, color=[GR, AZ, NA, RO])
for i, v in enumerate(base):
    ax.annotate(f"S/{v:.3f} MM".replace(".", ",") + ("" if i == 0 else f"\n(+{(v / base[0] - 1) * 100:.1f}%)".replace(".", ",")), (i, v), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8)
ax.set_ylabel("S/ millones por US$1 MM FOB"); ax.set_ylim(3.0, 4.05)
save(fig, "g5.png")

# G6 PBI mensual
pb = [p for p in L("PN01728AM") if p[0].endswith(("2025", "2026"))]
fig, ax = plt.subplots(figsize=(7.5, 3.4)); xs = list(range(len(pb)))
ax.bar(xs, [v for _, v in pb], color=[AZ if n.endswith("2026") else "#9dc3e6" for n, _ in pb])
for i, (n, v) in enumerate(pb): vl(ax, i, v, f"{v:.1f}".replace(".", ","))
ax.axhline(3.2, color=RO, ls="--", lw=1); ax.text(0, 3.35, "Proyección RI set-26 para 2026: 3,2%", color=RO, fontsize=8)
ax.set_xticks(xs); ax.set_xticklabels([lab(n) for n, _ in pb], rotation=60, fontsize=8); ax.set_ylabel("var. % interanual")
save(fig, "g6.png")

# G7 inflación
inf = [p for p in L("PN01273PM") if p[0].endswith(("2025", "2026"))]; ex = dict(L("PD12912AM"))
fig, ax = plt.subplots(figsize=(7.5, 3.4)); xs = list(range(len(inf)))
ax.fill_between([-0.5, len(inf) - 0.5], 1, 3, color=VE, alpha=0.12, label="Rango meta 1%–3%")
ax.plot(xs, [v for _, v in inf], color=RO, marker="o", ms=3, label="Inflación Lima, var. % 12 meses")
ax.plot(xs, [ex.get(n, np.nan) for n, _ in inf], color=AZ, ls="--", label="Expectativa de inflación a 12 meses")
ax.plot([len(inf) + 1], [4.2], marker="*", ms=12, color=NA, ls="none", label="Proyección RI set-26 (dic-26): 4,2%")
vl(ax, len(inf) - 1, inf[-1][1], "5,25", color=RO)
ax.set_xticks(xs[::2]); ax.set_xticklabels([lab(n) for n, _ in inf][::2], rotation=45); ax.set_ylabel("%")
ax.legend(frameon=False, fontsize=8, loc="upper left"); ax.set_ylim(0, 6.2)
save(fig, "g7.png")

# G8 costos financieros UCSUR
gf = [16.9, 23.0, 27.2, 27.5]; dc = [0.0, 0.1, 0.4, 1.7]; deu = [89.0, 113.1, 131.3, 172.8]
fig, ax = plt.subplots(figsize=(7.5, 3.4)); x = np.arange(4); w = 0.38
ax.bar(x - w / 2, gf, w, color=AZ, label="Gastos financieros"); ax.bar(x + w / 2, dc, w, color=RO, label="Pérdida por diferencia de cambio")
for xi, v in zip(x - w / 2, gf): vl(ax, xi, v, f"{v:.1f}".replace(".", ","))
for xi, v in zip(x + w / 2, dc): vl(ax, xi, v, f"{v:.1f}".replace(".", ","))
ax.set_ylabel("S/ millones"); ax.set_xticks(x); ax.set_xticklabels(yrs); ax.set_ylim(0, 35)
ax2 = ax.twinx(); ax2.plot(x, deu, color=NA, marker="o", label="Obligaciones financieras (eje der.)"); ax2.grid(False); ax2.spines["right"].set_visible(True); ax2.set_ylim(0, 200)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8, loc="upper left")
save(fig, "g8.png")

# G9 empleo e ingresos Lima
u = [p for p in L("PN38063GM") if p[0].endswith(("2025", "2026"))]; uj = dict(L("PN38066GM")); yi = dict(L("PN38070GM"))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.5, 3.4)); xs = list(range(len(u)))
a1.plot(xs, [v for _, v in u], color=AZ, label="Desempleo total"); a1.plot(xs, [uj[n] for n, _ in u], color=RO, label="Desempleo 14-24 años")
a1.set_xticks(xs[::4]); a1.set_xticklabels([lab(n) for n, _ in u][::4], rotation=45, fontsize=8); a1.set_ylabel("%"); a1.legend(frameon=False, fontsize=8)
vl(a1, xs[-1], uj[u[-1][0]], "11,3", color=RO); vl(a1, xs[-1], u[-1][1], "4,4", color=AZ)
a2.plot(xs, [yi[n] for n, _ in u], color=VE, marker="o", ms=3); a2.set_xticks(xs[::4]); a2.set_xticklabels([lab(n) for n, _ in u][::4], rotation=45, fontsize=8)
a2.set_ylabel("S/ por mes (nominal)"); a2.set_title("Ingreso promedio mensual", fontsize=9); a1.set_title("Tasa de desempleo", fontsize=9)
vl(a2, xs[-1], yi[u[-1][0]], "2.302")
save(fig, "g9.png")

# G10 crédito de consumo y cobranza UCSUR
cc = [p for p in L("PN00537MM") if p[0].endswith(("2025", "2026"))]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.5, 3.4)); xs = list(range(len(cc)))
a1.plot(xs, [v for _, v in cc], color=AZ, marker="o", ms=3); a1.set_title("Crédito de consumo, var. % 12 meses", fontsize=9)
a1.set_xticks(xs[::4]); a1.set_xticklabels([lab(n) for n, _ in cc][::4], rotation=45, fontsize=8); vl(a1, xs[-1], cc[-1][1], "13,2")
rec = [13.4, 17.7, 20.4, 48.8]; dias = [r / i * 365 for r, i in zip(rec, ing)]
a2.bar(yrs, rec, color="#9dc3e6"); a2.set_title("UCSUR: derechos por cobrar (S/ MM) y días", fontsize=9)
for i, (r, d) in enumerate(zip(rec, dias)): vl(a2, i, r, f"{r:.1f}\n{d:.0f} días".replace(".", ","))
a2.set_ylim(0, 62)
save(fig, "g10.png")

# Modelos conceptuales
def axes_model(ax, xl, yl):
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    ax.set_xlabel(xl); ax.set_ylabel(yl)

# M1 mercado de petróleo
fig, ax = plt.subplots(figsize=(6.5, 3.8)); axes_model(ax, "Cantidad de petróleo", "Precio WTI (US$/barril)")
q = np.linspace(1, 9, 50); ax.plot(q, 9.5 - 0.8 * q, color=AZ, label="D"); ax.plot(q, 0.5 + 0.8 * q, color=GR, label="S₀ (feb-26)")
ax.plot(q, 2.5 + 0.8 * q, color=RO, label="S₁ (conflicto en Medio Oriente)")
for (qq, pp, t) in [(5.625, 5.0, "E₀: US$64"), (4.375, 6.0, "E₁: US$99 (oct-26)")]:
    ax.plot(qq, pp, "ko"); ax.annotate(t, (qq, pp), xytext=(8, 4), textcoords="offset points", fontsize=8)
ax.annotate("", (3.6, 6.4), (4.8, 6.4), arrowprops=dict(arrowstyle="->", color=RO)); ax.legend(frameon=False, fontsize=8, loc="upper right")
save(fig, "m1.png")

# M2 mercado cambiario
fig, ax = plt.subplots(figsize=(6.5, 3.8)); axes_model(ax, "Cantidad de dólares", "Tipo de cambio (S/ por US$)")
ax.plot(q, 9.5 - 0.8 * q, color=AZ, label="D$₀"); ax.plot(q, 10.3 - 0.8 * q, color=AZ, ls="--", label="D$₁ (Fed 3,75%–4,00%, petróleo)")
ax.plot(q, 1.0 + 0.8 * q, color=VE, label="S$ (superávit comercial, compras BCRP)")
ax.plot(5.3125, 5.25, "ko"); ax.annotate("E₀: 3,367 (dic-25)", (5.3125, 5.25), xytext=(8, -12), textcoords="offset points", fontsize=8)
ax.plot(5.8125, 5.65, "ko"); ax.annotate("E₁: 3,412 (9-nov-26)", (5.8125, 5.65), xytext=(8, 4), textcoords="offset points", fontsize=8)
ax.legend(frameon=False, fontsize=8, loc="upper right"); save(fig, "m2.png")

# M3 OA-DA
fig, ax = plt.subplots(figsize=(6.5, 3.8)); axes_model(ax, "Producto (Y)", "Nivel de precios (P)")
ax.plot(q, 9.5 - 0.8 * q, color=AZ, label="DA₀"); ax.plot(q, 10.1 - 0.8 * q, color=AZ, ls="--", label="DA₁ (inversión privada +14%)")
ax.plot(q, 0.5 + 0.8 * q, color=GR, label="OA₀"); ax.plot(q, 1.5 + 0.8 * q, color=RO, label="OA₁ (petróleo y El Niño)")
ax.axvline(5.6, color="k", ls=":", lw=1); ax.text(5.65, 0.3, "Yₙ", fontsize=9)
ax.plot(5.625, 5.0, "ko"); ax.annotate("E₀: π 1,5%", (5.625, 5.0), xytext=(8, -12), textcoords="offset points", fontsize=8)
ax.plot(5.375, 5.8, "ko"); ax.annotate("E₁: Y +3,2%, π 4,2%–5,3%", (5.375, 5.8), xytext=(8, 4), textcoords="offset points", fontsize=8)
ax.legend(frameon=False, fontsize=8, loc="upper right"); save(fig, "m3.png")

# M4 IS-MP
fig, ax = plt.subplots(figsize=(6.5, 3.8)); axes_model(ax, "Producto (Y)", "Tasa de interés real (r)")
ax.plot(q, 9.5 - 0.9 * q, color=AZ, label="IS₀"); ax.plot(q, 10.2 - 0.9 * q, color=AZ, ls="--", label="IS₁ (crédito de consumo +13%, inversión)")
ax.axhline(4.0, color=GR, label="MP₀: r ex ante 1,20%"); ax.axhline(4.8, color=RO, ls="--", label="MP₁: alza de 25 pb (escenario)")
ax.plot(6.11, 4.0, "ko"); ax.plot(6.0, 4.8, "ko"); ax.annotate("E₁", (6.0, 4.8), xytext=(6, 4), textcoords="offset points")
ax.legend(frameon=False, fontsize=8, loc="upper right"); save(fig, "m4.png")

# Ishikawa
def ishikawa(name, efecto, espinas):
    fig, ax = plt.subplots(figsize=(7.5, 4.2)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.annotate("", (8.0, 3), (0.3, 3), arrowprops=dict(arrowstyle="-|>", lw=2, color="k"))
    ax.text(8.1, 3, efecto, va="center", fontsize=9, fontweight="bold", bbox=dict(boxstyle="round", fc="#f2f2f2", ec="k"))
    xs = [1.6, 4.1, 6.6]
    for i, (tit, items, col) in enumerate(espinas):
        x = xs[i % 3]; up = i < 3; y0 = 5.6 if up else 0.4
        ax.plot([x, x + 1.0], [y0, 3], color=col, lw=1.5)
        ax.text(x, y0 + (0.12 if up else -0.12), tit, ha="center", va="bottom" if up else "top", fontsize=8.5, fontweight="bold", color=col)
        for j, it in enumerate(items):
            yy = y0 - (0.55 + 0.42 * j) if up else y0 + (0.55 + 0.42 * j)
            ax.text(x + (yy - y0) / (3 - y0) * 1.0 - 0.05, yy, it, ha="right", va="center", fontsize=7)
    save(fig, name)

ishikawa("i1.png", "Ingresos y costos\nde UCSUR\n2026-2027", [
    ("Crecimiento mundial", ["Mundo 3,1% (2026)", "China 4,5%", "EE.UU. 2,2%"], VE),
    ("Energía", ["WTI US$99 (oct-26)", "Tarifas eléctricas", "Pasajes"], RO),
    ("Fed y dólar", ["Fed 3,75%–4,00%", "PCE EE.UU. 3,7%", "Diferencial 0,375 pp"], RO),
    ("Términos de intercambio", ["+18,1% (2026)", "Cobre US$6,59/lb", "Superávit comercial"], VE),
    ("Equipamiento importado", ["Laboratorios y simulación", "Software y licencias", "Costo +5,1% en S/"], RO),
    ("Capitales y riesgo", ["RIN US$96.668 MM", "Bonos no residentes 45%", "Prima de riesgo país"], GR)])
ishikawa("i2.png", "Matrícula, cobranza\ny margen de UCSUR\n2026-2027", [
    ("PBI y consumo", ["PBI 3,2% (2026P)", "Consumo privado 3,6%", "PBI ago 3,23%"], VE),
    ("Inflación", ["Lima 5,25% (oct-26)", "Servicios 5,3% (2026P)", "Ingreso real −4,0%"], RO),
    ("Tasa y Fisher", ["Referencia 4,25%", "r ex ante 1,20%", "r ex post −1,00%"], GR),
    ("Empleo", ["Desempleo Lima 4,4%", "Jóvenes 14-24: 11,3%", "242 mil empleos formales"], VE),
    ("Crédito educativo", ["Consumo +13,2%", "Cobranza 30 días", "Provisiones S/7,3 MM"], RO),
    ("Tipo de cambio", ["S/3,412 (9-nov)", "Rango S/3,40-3,50", "Pérdida cambiaria S/1,7 MM"], GR)])
print("ok", sorted(os.listdir(OUT)))

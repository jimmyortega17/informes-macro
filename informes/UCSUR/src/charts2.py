import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, "fig2"); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"text.parse_math": False, "font.family": "Carlito", "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.3})
AZ, CEL, RO, GR, NA, VE = "#1f4e79", "#3a8dc5", "#c00000", "#7f7f7f", "#e69500", "#2e7d32"

def L(code):
    d = json.load(open(os.path.join(S, "bcrp", f"L_{code}.json")))
    return [(p["name"], float(p["values"][0])) for p in d["periods"] if p["values"][0] != "n.d."]
def y2526(s): return [p for p in s if p[0].endswith(("2025", "2026"))]
def lab(n): m, y = n.split("."); return f"{m}-{y[2:]}"
def f1(x, d=1): return f"{x:.{d}f}".replace(".", ",")
def save(fig, name): fig.tight_layout(); fig.savefig(os.path.join(OUT, name), dpi=200); plt.close(fig)
def vl(ax, x, y, t, **k): ax.annotate(t, (x, y), textcoords="offset points", xytext=(0, 4), ha="center", fontsize=9, **k)
def dual_legend(ax, ax2, **k):
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, frameon=False, **k)

# ---------- Datos ----------
# G1 crecimiento mundial (RI set-26)
eco = ["Mundo", "EE.UU.", "Eurozona", "China", "América Latina", "Perú"]
g = {"2025": [3.4, 2.1, 1.4, 5.0, 2.4, 3.4], "2026P": [3.1, 2.2, 1.0, 4.5, 2.2, 3.2], "2027P": [3.1, 2.2, 1.3, 4.2, 2.4, 3.0]}
fig, ax = plt.subplots(figsize=(7.5, 3.6)); x = np.arange(6); w = 0.27
for i, (k, c) in enumerate(zip(g, ["#9dc3e6", AZ, NA])):
    ax.bar(x + (i - 1) * w, g[k], w, color=c, label=k)
    for xi, vi in zip(x + (i - 1) * w, g[k]): vl(ax, xi, vi, f1(vi))
ax.set_xticks(x); ax.set_xticklabels(eco); ax.set_ylabel("var. % real"); ax.legend(frameon=False, ncol=3); ax.set_ylim(0, 6)
save(fig, "g1.png")

# G2 WTI y cobre
w_ = y2526(L("PN01660XM")); c_ = y2526(L("PN01652XM"))
fig, ax = plt.subplots(figsize=(7.5, 3.6)); xs = range(len(w_))
ax.plot(xs, [v for _, v in w_], color=RO, marker="o", ms=3, label="Petróleo WTI (US$/barril, eje izq.)")
ax.axhline(82, color=RO, ls="--", lw=1); ax.text(0, 83.5, "Supuesto RI set-26 para 2026: US$82", color=RO, fontsize=9)
ax2 = ax.twinx(); ax2.plot(xs, [v / 100 for _, v in c_], color=NA, marker="s", ms=3, label="Cobre LME (US$/lb, eje der.)")
ax2.spines["right"].set_visible(True); ax2.grid(False)
ax.set_xticks(list(xs)[::2]); ax.set_xticklabels([lab(n) for n, _ in w_][::2], rotation=45)
vl(ax, len(w_) - 1, w_[-1][1], f1(w_[-1][1]), color=RO); dual_legend(ax, ax2, loc="upper left", fontsize=9)
ax.set_ylim(50, 110); ax2.set_ylim(3, 7.5); save(fig, "g2.png")

# G3 tipo de cambio
tc = y2526(L("PN01210PM"))
fig, ax = plt.subplots(figsize=(7.5, 3.4)); xs = list(range(len(tc)))
ax.plot(xs, [v for _, v in tc], color=AZ, marker="o", ms=3, label="Tipo de cambio bancario, promedio mensual")
ax.plot([xs[-1], xs[-1] + 1], [tc[-1][1], 3.412], color=AZ, ls=":", marker="D", ms=4)
ax.annotate("3,412 (9-nov-26)", (xs[-1] + 1, 3.412), xytext=(-10, -30), textcoords="offset points", fontsize=9, ha="center")
ax.fill_between([xs[-1] + 1, xs[-1] + 3], 3.40, 3.50, color=NA, alpha=0.25, label="Rango esperado S/3,40–3,50")
ax.set_xticks(xs[::2]); ax.set_xticklabels([lab(n) for n, _ in tc][::2], rotation=45); ax.set_ylabel("S/ por US$")
for i in [0, 11, len(tc) - 1]: vl(ax, i, tc[i][1], f1(tc[i][1], 3))
ax.legend(frameon=False, fontsize=9, loc="upper right"); ax.set_ylim(3.25, 3.85); save(fig, "g3.png")

# G4 balanza comercial (RI set-26)
yrs = ["2025", "2026P", "2027P"]; X = [93993, 119876, 124274]; M = [58560, 71011, 75995]; SB = [a - b for a, b in zip(X, M)]
fig, ax = plt.subplots(figsize=(7.5, 3.4)); x = np.arange(3); w = 0.27
for i, (v, c, l) in enumerate([(X, VE, "Exportaciones"), (M, RO, "Importaciones"), (SB, AZ, "Saldo comercial")]):
    ax.bar(x + (i - 1) * w, [t / 1000 for t in v], w, color=c, label=l)
    for xi, vi in zip(x + (i - 1) * w, v): vl(ax, xi, vi / 1000, f1(vi / 1000))
ax.set_xticks(x); ax.set_xticklabels(yrs); ax.set_ylabel("US$ miles de millones"); ax.legend(frameon=False, ncol=3, fontsize=9); ax.set_ylim(0, 140)
save(fig, "g4.png")

# G5 costo de equipo importado
esc = ["Dic-25\n(TC 3,367)", "Nov-26\n(TC 3,412)", "TC 3,50", "TC 3,60"]; tcs = [3.367, 3.412, 3.50, 3.60]
base = [tcs[0]] + [1.037 * t for t in tcs[1:]]
fig, ax = plt.subplots(figsize=(7.5, 3.4)); ax.bar(esc, base, color=[GR, AZ, NA, RO])
for i, v in enumerate(base):
    ax.annotate(f"S/{f1(v, 3)} MM" + ("" if i == 0 else f"\n(+{f1((v / base[0] - 1) * 100)}%)"), (i, v), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9)
ax.set_ylabel("S/ millones por US$1 MM FOB"); ax.set_ylim(3.0, 4.05); save(fig, "g5.png")

# G6 PBI mensual
pb = y2526(L("PN01728AM"))
fig, ax = plt.subplots(figsize=(7.5, 3.4)); xs = list(range(len(pb)))
ax.bar(xs, [v for _, v in pb], color=[AZ if n.endswith("2026") else "#9dc3e6" for n, _ in pb])
for i, (n, v) in enumerate(pb): vl(ax, i, v, f1(v))
ax.axhline(3.2, color=RO, ls="--", lw=1); ax.text(0, 3.35, "Proyección RI set-26 para 2026: 3,2%", color=RO, fontsize=9)
ax.set_xticks(xs); ax.set_xticklabels([lab(n) for n, _ in pb], rotation=60, fontsize=9); ax.set_ylabel("var. % interanual")
save(fig, "g6.png")

# G7 cruce 3 años: PBI, consumo e ingresos reales UCSUR
yy = ["2023", "2024", "2025"]; pbi = [-0.35, 3.52, 3.43]; cp = [0.06, 2.77, 3.63]; ing = [14.66, 27.66, 39.39]
fig, ax = plt.subplots(figsize=(7.5, 3.4)); x = np.arange(3); w = 0.27
for i, (v, c, l) in enumerate([(pbi, GR, "PBI real"), (cp, CEL, "Consumo privado real"), (ing, AZ, "Ingresos reales de UCSUR")]):
    ax.bar(x + (i - 1) * w, v, w, color=c, label=l)
    for xi, vi in zip(x + (i - 1) * w, v): vl(ax, xi, max(vi, 0), f1(vi))
ax.axhline(0, color="k", lw=0.8); ax.set_xticks(x); ax.set_xticklabels(yy); ax.set_ylabel("var. % real"); ax.legend(frameon=False, fontsize=9, loc="upper left"); ax.set_ylim(-3, 46)
for xi, e in zip(x[1:], ["ε = 9,99", "ε = 10,85"]): ax.text(xi, 43, e, ha="center", fontsize=10, color=RO, fontweight="bold")
save(fig, "g7.png")

# G8 inflación y expectativas
inf = y2526(L("PN01273PM")); ex = dict(L("PD12912AM"))
fig, ax = plt.subplots(figsize=(7.5, 3.4)); xs = list(range(len(inf)))
ax.fill_between([-0.5, len(inf) - 0.5], 1, 3, color=VE, alpha=0.12, label="Rango meta 1%–3%")
ax.plot(xs, [v for _, v in inf], color=RO, marker="o", ms=3, label="Inflación Lima, var. % 12 meses")
ax.plot(xs, [ex.get(n, np.nan) for n, _ in inf], color=AZ, ls="--", label="Expectativa de inflación a 12 meses")
ax.plot([len(inf) + 1], [4.2], marker="*", ms=12, color=NA, ls="none", label="Proyección RI set-26 (dic-26): 4,2%")
vl(ax, len(inf) - 1, inf[-1][1], "5,25", color=RO)
ax.set_xticks(xs[::2]); ax.set_xticklabels([lab(n) for n, _ in inf][::2], rotation=45); ax.set_ylabel("%")
ax.legend(frameon=False, fontsize=9, loc="upper left"); ax.set_ylim(0, 6.2); save(fig, "g8.png")

# G9 liquidez vs inflación (M×V=P×Y)
liq = y2526(L("PN00189MM")); infd = dict(inf)
fig, ax = plt.subplots(figsize=(7.5, 3.4)); xs = list(range(len(liq)))
ax.plot(xs, [v for _, v in liq], color=AZ, marker="o", ms=3, label="Liquidez en soles (M), var. % 12 meses")
ax.plot(xs, [infd.get(n, np.nan) for n, _ in liq], color=RO, marker="s", ms=3, label="Inflación Lima (P), var. % 12 meses")
ax.axhline(3.2, color=GR, ls="--", lw=1, label="PBI real 2026P (Y): 3,2%")
vl(ax, len(liq) - 1, liq[-1][1], f1(liq[-1][1]), color=AZ)
ax.set_xticks(xs[::2]); ax.set_xticklabels([lab(n) for n, _ in liq][::2], rotation=45); ax.set_ylabel("%"); ax.legend(frameon=False, fontsize=9, loc="upper left"); ax.set_ylim(0, 22)
save(fig, "g9.png")

# G10 costos financieros UCSUR
y4 = ["2022", "2023", "2024", "2025"]; gf = [16.9, 23.0, 27.2, 27.5]; dc = [0.0, 0.1, 0.4, 1.7]; deu = [89.0, 113.1, 131.3, 172.8]
fig, ax = plt.subplots(figsize=(7.5, 3.4)); x = np.arange(4); w = 0.38
ax.bar(x - w / 2, gf, w, color=AZ, label="Gastos financieros"); ax.bar(x + w / 2, dc, w, color=RO, label="Pérdida por diferencia de cambio")
for xi, v in zip(x - w / 2, gf): vl(ax, xi, v, f1(v))
for xi, v in zip(x + w / 2, dc): vl(ax, xi, v, f1(v))
ax.set_ylabel("S/ millones"); ax.set_xticks(x); ax.set_xticklabels(y4); ax.set_ylim(0, 35)
ax2 = ax.twinx(); ax2.plot(x, deu, color=NA, marker="o", label="Obligaciones financieras (eje der.)"); ax2.grid(False); ax2.spines["right"].set_visible(True); ax2.set_ylim(0, 200)
for xi, v in zip(x, deu): ax2.annotate(f1(v), (xi, v), xytext=(12, -3), textcoords="offset points", fontsize=9, color=NA)
dual_legend(ax, ax2, fontsize=9, loc="upper left"); save(fig, "g10.png")

# G11 empleo e ingresos
u = y2526(L("PN38063GM")); uj = dict(L("PN38066GM")); yi = dict(L("PN38070GM"))
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.5, 3.4)); xs = list(range(len(u)))
a1.plot(xs, [v for _, v in u], color=AZ, label="Desempleo total"); a1.plot(xs, [uj[n] for n, _ in u], color=RO, label="Desempleo 14-24 años")
a1.set_xticks(xs[::4]); a1.set_xticklabels([lab(n) for n, _ in u][::4], rotation=45, fontsize=9); a1.set_ylabel("%"); a1.legend(frameon=False, fontsize=9)
vl(a1, xs[-1], uj[u[-1][0]], "11,3", color=RO); vl(a1, xs[-1], u[-1][1], "4,4", color=AZ)
a2.plot(xs, [yi[n] for n, _ in u], color=VE, marker="o", ms=3); a2.set_xticks(xs[::4]); a2.set_xticklabels([lab(n) for n, _ in u][::4], rotation=45, fontsize=9)
a2.set_ylabel("S/ por mes (nominal)"); a2.set_title("Ingreso promedio mensual", fontsize=10); a1.set_title("Tasa de desempleo", fontsize=10)
vl(a2, xs[-1], yi[u[-1][0]], "2.302"); save(fig, "g11.png")

# G12 crédito de consumo y cobranza UCSUR
cc = y2526(L("PN00537MM")); ingn = [264.1, 321.8, 420.4, 594.8]; rec = [13.4, 17.7, 20.4, 48.8]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.5, 3.4)); xs = list(range(len(cc)))
a1.plot(xs, [v for _, v in cc], color=AZ, marker="o", ms=3); a1.set_title("Crédito de consumo, var. % 12 meses", fontsize=10)
a1.set_xticks(xs[::4]); a1.set_xticklabels([lab(n) for n, _ in cc][::4], rotation=45, fontsize=9); vl(a1, xs[-1], cc[-1][1], "13,2")
a2.bar(y4, rec, color="#9dc3e6"); a2.set_title("UCSUR: derechos por cobrar (S/ MM) y días", fontsize=10)
for i, (r, ii) in enumerate(zip(rec, ingn)): vl(a2, i, r, f"{f1(r)}\n{r / ii * 365:.0f} días")
a2.set_ylim(0, 62); save(fig, "g12.png")

# ---------- Modelos de curvas (estilo PPT/MAC70B) ----------
def model_axes(xl, yl):
    fig, ax = plt.subplots(figsize=(7.0, 4.3)); ax.grid(False); ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_xlabel(xl, fontweight="bold"); ax.set_ylabel(yl, fontweight="bold"); return fig, ax
def eq(ax, x, y, t, col, dx=8, dy=-14):
    ax.plot([x, x], [0, y], ":", color=GR, lw=1); ax.plot([0, x], [y, y], ":", color=GR, lw=1)
    ax.plot(x, y, "o", color=col, ms=8, zorder=5); ax.annotate(t, (x, y), xytext=(dx, dy), textcoords="offset points", color=col, fontweight="bold", fontsize=11)
def arrow(ax, a, b, col=NA): ax.annotate("", b, a, arrowprops=dict(arrowstyle="-|>", lw=2.5, color=col))
q = np.linspace(0.6, 9.4, 100)

# M1 petróleo: S se contrae
fig, ax = model_axes("Cantidad de petróleo (barriles)", "Precio WTI (US$/barril)")
ax.plot(q, 9.2 - 0.75 * q, color=CEL, lw=2.5); ax.text(0.7, 8.9, "D (demanda mundial, 3,1%)", color=CEL, fontweight="bold")
ax.plot(q, 0.6 + 0.75 * q, color=AZ, lw=2.5); ax.text(8.0, 6.3, "S₀ (feb-26)", color=AZ, fontweight="bold")
ax.plot(q, 2.6 + 0.75 * q, color=RO, lw=2.5, ls="--"); ax.text(5.6, 7.9, "S₁ (conflicto en Medio Oriente)", color=RO, fontweight="bold")
eq(ax, 5.733, 4.9, "E₀: US$64,4", CEL); eq(ax, 4.4, 5.9, "E₁: US$98,9 (oct-26)", RO, dx=-150, dy=8)
arrow(ax, (6.6, 5.8), (5.3, 6.7)); save(fig, "m1.png")

# M2 mercado cambiario
fig, ax = model_axes("Cantidad de dólares (US$)", "Tipo de cambio (S/ por US$)")
ax.plot(q, 9.2 - 0.75 * q, color=CEL, lw=2.5); ax.text(0.7, 8.9, "D$₀ (dic-25)", color=CEL, fontweight="bold")
ax.plot(q, 10.0 - 0.75 * q, color=RO, lw=2.5, ls="--"); ax.text(3.0, 8.4, "D$₁ (Fed 3,75%–4,00%; WTI US$99)", color=RO, fontweight="bold")
ax.plot(q, 0.9 + 0.75 * q, color=VE, lw=2.5); ax.text(6.9, 4.3, "S$ (superávit comercial US$48.865 MM;\ncompras BCRP US$15.715 MM)", color=VE, fontweight="bold", fontsize=9)
eq(ax, 5.533, 5.05, "E₀: S/3,367 (dic-25)", CEL, dx=-150, dy=-22); eq(ax, 6.067, 5.45, "E₁: S/3,412 (9-nov-26)", RO, dx=-40, dy=14)
arrow(ax, (4.0, 6.6), (4.9, 7.1)); save(fig, "m2.png")

# M3 OA-DA
fig, ax = model_axes("Producto real (Y)", "Nivel de precios (P)")
ax.plot(q, 9.2 - 0.75 * q, color=CEL, lw=2.5); ax.text(0.7, 8.9, "DA₀", color=CEL, fontweight="bold")
ax.plot(q, 9.9 - 0.75 * q, color=CEL, lw=2.5, ls="--"); ax.text(1.0, 9.6, "DA₁ (inversión privada +14,0%; consumo +3,6%)", color=CEL, fontweight="bold")
ax.plot(q, 0.6 + 0.75 * q, color=AZ, lw=2.5); ax.text(8.6, 6.7, "OA₀", color=AZ, fontweight="bold")
ax.plot(q, 1.5 + 0.75 * q, color=RO, lw=2.5, ls="--"); ax.text(6.6, 7.4, "OA₁ (petróleo, El Niño)", color=RO, fontweight="bold")
ax.axvline(5.75, color=NA, ls="--", lw=2); ax.text(5.85, 0.4, "Yn (OALP)", color=NA, fontweight="bold")
eq(ax, 5.733, 4.9, "E₀ 2025: π 1,5%; PBI 3,4%", AZ, dx=12, dy=-34); eq(ax, 5.6, 5.7, "E₁ 2026: π 5,25%; PBI 3,2%", RO, dx=-205, dy=8)
save(fig, "m3.png")

# M4 isocuanta de servicios educativos
fig, ax = model_axes("Horas docentes (L)", "Capital académico: laboratorios y campus (K)")
L_ = np.linspace(1.2, 9.5, 100)
ax.plot(L_, 16 / L_, color=AZ, lw=2.5); ax.text(7.9, 1.55, "Q₀: servicio educativo 2025", color=AZ, fontweight="bold")
ax.plot(L_, 8.0 - 1.0 * L_, color=CEL, lw=2.5); ax.text(6.3, 0.9, "Isocosto₀ (w/r inicial)", color=CEL, fontweight="bold")
ax.plot(L_, 9.238 - 1.3333 * L_, color=RO, lw=2.5, ls="--"); ax.text(4.9, 6.4, "Isocosto₁: ↑w por inflación 5,25%\ny ↑r por equipo +5,1% en S/", color=RO, fontweight="bold", fontsize=9)
eq(ax, 4.0, 4.0, "A: L/K inicial", CEL, dx=10, dy=-6); eq(ax, 3.464, 4.619, "B: más capital,\nmenos horas por alumno", RO, dx=-175, dy=28)
save(fig, "m4.png")

# M5 IS-MP
fig, ax = model_axes("Producto real (Y)", "Tasa de interés real (r)")
ax.plot(q, 9.2 - 0.85 * q, color=CEL, lw=2.5); ax.text(0.7, 8.8, "IS₀", color=CEL, fontweight="bold")
ax.plot(q, 9.9 - 0.85 * q, color=CEL, lw=2.5, ls="--"); ax.text(1.4, 9.1, "IS₁ (crédito de consumo +13,2%; inversión +14,0%)", color=CEL, fontweight="bold")
ax.axhline(4.2, color=AZ, lw=2.5); ax.text(8.0, 3.7, "MP₀: r = 1,20%", color=AZ, fontweight="bold")
ax.axhline(5.0, color=RO, lw=2.5, ls="--"); ax.text(7.3, 5.2, "MP₁: alza de 25 pb", color=RO, fontweight="bold")
eq(ax, 6.7, 4.2, "E₁", AZ, dx=6, dy=-18); eq(ax, 5.76, 5.0, "E₂", RO, dx=-24, dy=6)
arrow(ax, (7.2, 4.4), (6.3, 4.9)); save(fig, "m5.png")

# ---------- Ishikawa ----------
def ishikawa(name, efecto, espinas):
    fig, ax = plt.subplots(figsize=(7.5, 4.3)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.annotate("", (8.0, 3), (0.3, 3), arrowprops=dict(arrowstyle="-|>", lw=2, color="k"))
    ax.text(8.1, 3, efecto, va="center", fontsize=10, fontweight="bold", bbox=dict(boxstyle="round", fc="#f2f2f2", ec="k"))
    xs = [1.6, 4.1, 6.6]
    for i, (tit, items, col) in enumerate(espinas):
        x = xs[i % 3]; up = i < 3; y0 = 5.6 if up else 0.4
        ax.plot([x, x + 1.0], [y0, 3], color=col, lw=1.5)
        ax.text(x, y0 + (0.12 if up else -0.12), tit, ha="center", va="bottom" if up else "top", fontsize=10, fontweight="bold", color=col)
        for j, it in enumerate(items):
            yy = y0 - (0.55 + 0.42 * j) if up else y0 + (0.55 + 0.42 * j)
            ax.text(x + (yy - y0) / (3 - y0) * 1.0 - 0.05, yy, it, ha="right", va="center", fontsize=8.5)
    save(fig, name)

ishikawa("i1.png", "Ingresos y costos\nde UCSUR\n2026-2027", [
    ("Y* y Y", ["Mundo 3,1% (2026)", "China 4,5%", "Perú 3,2%"], VE),
    ("Petróleo e inflación", ["WTI US$98,9 (oct-26)", "Inflación 5,25%", "Ingreso real −4,0%"], RO),
    ("Fed y tipo de cambio", ["Fed 3,75%–4,00%", "i − i* = 0,375 pp", "TC S/3,412"], RO),
    ("TI y balanza de pagos", ["TI +18,1% (2026)", "CA 4,0% del PBI", "RIN US$96.668 MM"], VE),
    ("π EE.UU. y dólar", ["PCE EE.UU. 3,7%", "Equipo +5,1% en S/", "Capex S/82,5 MM"], RO),
    ("Capitales y riesgo", ["Compras BCRP US$15.715 MM", "Bonos no residentes 45%", "Prima de riesgo país"], GR)])
ishikawa("i2.png", "Matrícula, cobranza\ny margen de UCSUR\n2026-2027", [
    ("PBI y consumo", ["PBI 3,2% (2026P)", "Consumo 3,6% → 3,0%", "ε aparente = 10,4"], VE),
    ("Inflación y dinero", ["π Lima 5,25%", "Liquidez +16,7%", "Servicios 5,3% (2026P)"], RO),
    ("Tasa y Fisher", ["Referencia 4,25%", "r ex ante 1,20%", "r ex post −1,00%"], GR),
    ("Empleo e ingresos", ["Desempleo Lima 4,4%", "Jóvenes 14-24: 11,3%", "Ingreso S/2.302"], VE),
    ("Crédito y morosidad", ["Consumo +13,2%", "Cobranza 30 días", "Castigos +84%"], RO),
    ("Política fiscal", ["Déficit 1,5% del PBI", "Consumo público 3,2% → 2,3%", "Deuda 28,2% (2027)"], GR)])
print("ok", sorted(os.listdir(OUT)))

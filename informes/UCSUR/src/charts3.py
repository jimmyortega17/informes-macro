import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
S = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(S, "fig2")
plt.rcParams.update({"text.parse_math": False, "font.family": "Carlito", "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.3})
AZ, CEL, RO, GR, NA, VE = "#1f4e79", "#3a8dc5", "#c00000", "#7f7f7f", "#e69500", "#2e7d32"
def f1(x, d=1): return f"{x:.{d}f}".replace(".", ",")
def vl(ax, x, y, t, **k): ax.annotate(t, (x, y), textcoords="offset points", xytext=(0, 4), ha="center", fontsize=9, **k)
def save(fig, n): fig.tight_layout(); fig.savefig(os.path.join(OUT, n), dpi=200); plt.close(fig)

# g13 resultados UCSUR
yrs = ["2022", "2023", "2024", "2025"]; ing = [264.1, 321.8, 420.4, 594.8]; uop = [55.0, 50.8, 121.1, 219.5]; un = [25.0, 22.0, 76.5, 141.6]
fig, ax = plt.subplots(figsize=(7.5, 3.6)); x = np.arange(4); w = 0.27
for i, (v, c, l) in enumerate([(ing, AZ, "Ingresos por derechos de enseñanza"), (uop, NA, "Utilidad de operación"), (un, VE, "Utilidad neta")]):
    ax.bar(x + (i - 1) * w, v, w, color=c, label=l)
    for xi, vi in zip(x + (i - 1) * w, v): vl(ax, xi, vi, f1(vi))
ax.set_xticks(x); ax.set_xticklabels(yrs); ax.set_ylabel("S/ millones"); ax.set_ylim(0, 690)
ax2 = ax.twinx(); mg = [u / i * 100 for u, i in zip(uop, ing)]; ax2.plot(x, mg, color=RO, marker="o", label="Margen operativo % (eje der.)")
for xi, m in zip(x, mg): ax2.annotate(f1(m) + "%", (xi, m), xytext=(10, -2), textcoords="offset points", color=RO, fontsize=9)
ax2.set_ylim(0, 45); ax2.grid(False); ax2.spines["right"].set_visible(True)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left", fontsize=9)
save(fig, "g13.png")

# g14 proyección de ingresos por escenario y PBI
hist = {2022: 264.1, 2023: 321.8, 2024: 420.4, 2025: 594.8}
esc = {"Techo (ε = 10,4)": ([860.5, 1151.5, 1541.0], RO), "Base (ε = 5,2)": ([743.3, 876.4, 1033.4], AZ), "Prudente (ε = 2,0)": ([671.1, 725.6, 784.6], VE)}
pbi = {2022: 2.82, 2023: -0.35, 2024: 3.52, 2025: 3.43, 2026: 3.2, 2027: 3.0, 2028: 3.0}
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.bar(list(hist), list(hist.values()), color="#9dc3e6", label="Ingresos observados (S/ MM)")
for k, v in hist.items(): vl(ax, k, v, f1(v))
for name, (v, c) in esc.items():
    ax.plot([2025, 2026, 2027, 2028], [594.8] + v, marker="o", color=c, label=name)
    ax.annotate(f1(v[-1]), (2028, v[-1]), xytext=(6, -3), textcoords="offset points", fontsize=9, color=c)
ax.set_ylabel("S/ millones"); ax.set_ylim(0, 1700); ax.set_xlim(2021.4, 2028.7)
ax2 = ax.twinx(); ax2.plot(list(pbi), list(pbi.values()), color=GR, ls="--", marker="s", ms=4, label="PBI real, var. % (eje der.)")
ax2.set_ylim(-2, 12); ax2.grid(False); ax2.spines["right"].set_visible(True)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left", fontsize=9)
save(fig, "g14.png")

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

ishikawa("i3.png", "Dependencia de\nUCSUR de las 4\nvariables clave", [
    ("PBI y consumo", ["Ingresos S/594,8 MM", "ε aparente = 10,4", "C +3,6% → +3,0%"], VE),
    ("Inflación", ["Planilla S/214,7 MM", "Gastos generales S/128,2 MM", "Efecto precio S/18,0 MM"], RO),
    ("Tipo de cambio", ["Capex S/82,5 MM", "Pérdida cambiaria S/1,7 MM", "Equipo +5,1% en S/"], GR),
    ("Tasa de interés", ["Deuda S/172,8 MM", "Costo implícito 10,2%", "+25 pb = S/0,43 MM"], RO),
    ("Cobranza", ["CxC S/48,8 MM", "30 días de cobro", "Estimación S/6,5 MM"], RO),
    ("Estructura", ["Margen operativo 36,9%", "Caja operativa S/230,6 MM", "Patrimonio S/350,6 MM"], VE)])
ishikawa("i4.png", "Ingresos y margen\nde UCSUR\n2026-2028", [
    ("PBI → ventas", ["Base ε = 5,2", "Ventas 2026P S/743 MM", "−1 pp C = −S/31 MM"], VE),
    ("Tasa → CxC y CxP", ["Referencia 4,25%", "CxC S/48,8 MM", "CxP S/40,0 MM"], GR),
    ("Inflación → costos", ["π 5,25% (2026)", "+S/18,0 MM costos", "π 2,0% (2027P)"], RO),
    ("Tipo de cambio", ["S/3,40–3,50", "Capex en US$", "Forwards 50%"], GR),
    ("Empleo e ingreso", ["Desempleo 4,4%", "Ingreso real −4,0%", "Castigos +84%"], RO),
    ("Liquidez y crédito", ["Liquidez +16,7%", "Crédito consumo +13,2%", "Morosidad al alza"], VE)])
print("ok")

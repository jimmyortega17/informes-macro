import os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
S = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(S, "fig2")
exec(open(os.path.join(S, "charts3.py")).read().split("# g13 resultados UCSUR")[0])
exec("def ishikawa" + open(os.path.join(S, "charts3.py")).read().split("def ishikawa")[1].split("ishikawa(\"i3.png\"")[0])

# g14 (nueva) proyección con PBI de educación
hist = {2022: 264.1, 2023: 321.8, 2024: 420.4, 2025: 594.8}
esc = {"Techo (ε = 8,0)": ([841.4, 1112.3, 1472.1], RO), "Base (ε = 4,0)": ([733.8, 859.2, 1008.9], AZ), "Prudente (ε = 1,5)": ([666.5, 717.5, 775.6], VE)}
sv = {2022: 3.4, 2023: 2.3, 2024: 3.6, 2025: 4.0, 2026: 4.3, 2027: 3.7, 2028: 3.64}
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.bar(list(hist), list(hist.values()), color="#9dc3e6", label="Ingresos observados (S/ MM)")
for k, v in hist.items(): vl(ax, k, v, f1(v))
for name, (v, c) in esc.items():
    ax.plot([2025, 2026, 2027, 2028], [594.8] + v, marker="o", color=c, label=name)
    ax.annotate(f1(v[-1]), (2028, v[-1]), xytext=(6, -3), textcoords="offset points", fontsize=9, color=c)
ax.set_ylabel("S/ millones"); ax.set_ylim(0, 1650); ax.set_xlim(2021.4, 2028.8)
ax2 = ax.twinx(); ax2.plot(list(sv), list(sv.values()), color=GR, ls="--", marker="s", ms=4, label="PBI de servicios, var. % (BCRP 2026-27; MEF 2028, eje der.)")
ax2.set_ylim(0, 12); ax2.grid(False); ax2.spines["right"].set_visible(True)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels(); ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left", fontsize=9)
save(fig, "g14c.png")

print("ok")

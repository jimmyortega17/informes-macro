import os, sys, shutil
S = os.path.dirname(os.path.abspath(__file__))
def run(fname, reps, keep):
    src = open(os.path.join(S, fname), encoding="utf-8").read()
    for a, b in reps:
        if src.count(a) != 1: sys.exit(f"{fname}: count {src.count(a)} for {a[:60]}")
        src = src.replace(a, b)
    src = src.replace('os.path.join(S, "fig2")', 'os.path.join(S, "figtmp")')
    # charts4 ejecuta charts3 leyéndolo del disco: redirigir también ahí
    src = src.replace('open(os.path.join(S, "charts3.py")).read()', 'open(os.path.join(S, "charts3.py")).read().replace(\'os.path.join(S, "fig2")\', \'os.path.join(S, "figtmp")\')')
    g = {"__file__": os.path.join(S, fname), "__name__": "__main__"}
    exec(compile(src, fname, "exec"), g)
    for k in keep: shutil.copy(os.path.join(S, "figtmp", k), os.path.join(S, "fig3", k))
run("charts2.py", [
    ('ax.text(8.0, 3.7, "MP₀: r = 1,20%"', 'ax.text(7.2, 3.7, "MP₀: r = 1,20% (i = 4,25%)"'),
    ('ax.text(7.3, 5.2, "MP₁: alza de 25 pb"', 'ax.text(6.15, 5.25, "MP₁: r = 1,45% (i = 4,50%, nov-26)"'),
    ('"i − i* = 0,375 pp"', '"i − i* = 0,625 pp"'),
    ('("Tasa y Fisher", ["Referencia 4,25%", "r ex ante 1,20%", "r ex post −1,00%"], GR)', '("Tasa y Fisher", ["Referencia 4,50% (nov-26)", "r ex ante 1,45%", "r ex post −0,75%"], GR)'),
], ["m5.png", "i1.png", "i2.png"])
run("charts4.py", [
    ('br = [p for p in L("H_PD04722MM.json") if p[0][-4:] in ("2024", "2025", "2026")]',
     'br = [p for p in L("H_PD04722MM.json") if p[0][-4:] in ("2024", "2025", "2026")] + [("Nov.2026", 4.50), ("Nov.2026 ", 4.50)]'),
    ('ax.annotate("0,375 pp", (xs[-1], 4.06), xytext=(-40, 18)', 'ax.annotate("0,625 pp", (xs[-1], 4.19), xytext=(-48, 22)'),
    ('"Diferencial 0,375 pp"', '"Diferencial 0,625 pp"'),
    ('("Tasa BCRP", ["4,25% desde set-25", "r ex ante 1,20%", "r ex post −1,00%"], GR)', '("Tasa BCRP", ["4,50% desde 13-nov-26", "r ex ante 1,45%", "r ex post −0,75%"], GR)'),
    ('("Sensibilidad", ["+25 pb = S/0,43 MM", "+50 pb = S/0,86 MM", "Gastos fin. S/27,5 MM"], RO)', '("Sensibilidad", ["Alza nov-26: S/0,43 MM", "Otra alza: +S/0,43 MM", "Gastos fin. S/27,5 MM"], RO)'),
], ["g16.png", "i7.png", "i8.png"])
print("figs ok")

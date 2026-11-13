import json, os, collections
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
S=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(S,"fig"); os.makedirs(OUT,exist_ok=True)
plt.rcParams.update({"text.parse_math":False,"font.family":"Carlito","font.size":11,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.alpha":0.3})
AZ,CEL,RO,GR,NA,VE="#1f4e79","#3a8dc5","#c00000","#7f7f7f","#e69500","#2e7d32"
def L(code):
    d=json.load(open(os.path.join(S,"bcrp",f"L_{code}.json"))); return [(p["name"],float(p["values"][0])) for p in d["periods"] if p["values"][0]!="n.d."]
def y2526(s): return [p for p in s if p[0].endswith(("2025","2026"))]
def lab(n): m,y=n.split("."); return f"{m}-{y[2:]}"
def f1(x,d=1): return f"{x:,.{d}f}".replace(",","X").replace(".",",").replace("X",".")
def save(fig,name): fig.tight_layout(); fig.savefig(os.path.join(OUT,name),dpi=200); plt.close(fig)
def vl(ax,x,y,t,**k): ax.annotate(t,(x,y),textcoords="offset points",xytext=(0,4),ha="center",fontsize=9,**k)
def dual_legend(ax,ax2,**k):
    h1,l1=ax.get_legend_handles_labels(); h2,l2=ax2.get_legend_handles_labels(); ax.legend(h1+h2,l1+l2,frameon=False,**k)
M=json.load(open('/tmp/claude-0/ocp_model.json')); R=M['R']; Y=M['Y']
P=json.load(open('/tmp/claude-0/ocp_prod.json'))
SC=json.load(open('/tmp/claude-0/ocp_scen.json'))

# g1 crecimiento mundial
eco=["Mundo","EE.UU.","Eurozona","China","América Latina","Perú"]
g={"2025":[3.4,2.1,1.4,5.0,2.4,3.4],"2026P":[3.1,2.2,1.0,4.5,2.2,3.2],"2027P":[3.1,2.2,1.3,4.2,2.4,3.0]}
fig,ax=plt.subplots(figsize=(7.5,3.6)); x=np.arange(6); w=0.27
for i,(k,c) in enumerate(zip(g,["#9dc3e6",AZ,NA])):
    ax.bar(x+(i-1)*w,g[k],w,color=c,label=k)
    for xi,vi in zip(x+(i-1)*w,g[k]): vl(ax,xi,vi,f1(vi))
ax.set_xticks(x); ax.set_xticklabels(eco); ax.set_ylabel("var. % real"); ax.legend(frameon=False,ncol=3); ax.set_ylim(0,6); save(fig,"g1.png")

# g2 metales: cobre, plata, zinc, WTI (índice ene-23 = 100)
d=json.load(open(os.path.join(S,"bcrp","met.json"))); per=d["periods"]
names=[p["name"] for p in per]; vals=np.array([[float(v) for v in p["values"]] for p in per])
fig,ax=plt.subplots(figsize=(7.5,3.6)); xs=np.arange(len(per))
for j,(lb,c) in enumerate([("Cobre LME",NA),("Plata",GR),("Zinc LME",CEL),("Petróleo WTI",RO)]):
    s=vals[:,j]/vals[0,j]*100; ax.plot(xs,s,color=c,lw=2,label=lb); vl(ax,xs[-1],s[-1],f1(s[-1],0),color=c)
ax.axhline(100,color="k",lw=0.6); ax.set_xticks(xs[::4]); ax.set_xticklabels([lab(n) for n in names][::4],rotation=45,fontsize=9)
ax.set_ylabel("Índice ene-2023 = 100"); ax.legend(frameon=False,fontsize=9,loc="upper left",ncol=2); save(fig,"g2.png")

# g3 producción mensual OCP (MINEM)
cu=[];ag=[];lb=[]
mon=["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Set","Oct","Nov","Dic"]
for y in ["2023","2024","2025","2026"]:
    for i in range(12):
        v=P[y]["COBRE"][i]
        if v is None: continue
        cu.append(v); ag.append(P[y]["PLATA"][i]/31.1034768); lb.append(f"{mon[i]}-{y[2:]}")
fig,ax=plt.subplots(figsize=(7.5,3.6)); xs=np.arange(len(cu))
ax.bar(xs,cu,color=AZ,label="Cobre fino (TMF, eje izq.)")
ax2=ax.twinx(); ax2.plot(xs,np.array(ag),color=NA,marker="o",ms=2.5,label="Plata (miles de oz, eje der.)"); ax2.grid(False); ax2.spines["right"].set_visible(True)
ax.set_xticks(xs[::3]); ax.set_xticklabels(lb[::3],rotation=45,fontsize=9); ax.set_ylabel("TMF"); ax2.set_ylabel("miles de oz")
for yy,tot in [("2023",8351),("2024",14791),("2025",16545)]:
    i=lb.index(f"Jun-{yy[2:]}"); ax.text(i,1950,f"{yy}: {f1(tot,0)} TMF",ha="center",fontsize=9,color=AZ,fontweight="bold")
ax.set_ylim(0,2400); ax2.set_ylim(0,110); dual_legend(ax,ax2,fontsize=9,loc="upper left",ncol=2); save(fig,"g3.png")

# g4 tasas Fed vs BCRP
br=[p for p in json.load(open(os.path.join(S,"bcrp","H_PD04722MM.json")))["periods"] if p["name"][-4:] in ("2024","2025","2026") and p["values"][0]!="n.d."]
br=[(p["name"],float(p["values"][0])) for p in br]
steps={"Ene.2024":5.375,"Sep.2024":4.875,"Nov.2024":4.625,"Dic.2024":4.375,"Sep.2025":4.125,"Oct.2025":3.875,"Dic.2025":3.625,"Sep.2026":3.875}
fv=[];cur=5.375
for n,_ in br:
    if n in steps: cur=steps[n]
    fv.append(cur)
fig,ax=plt.subplots(figsize=(7.5,3.4)); xs=list(range(len(br)))
ax.step(xs,[v for _,v in br],where="post",color=AZ,lw=2,label="Tasa de referencia BCRP")
ax.step(xs,fv,where="post",color=RO,lw=2,label="Fed, punto medio del rango")
ax.fill_between(xs,fv,[v for _,v in br],step="post",color=NA,alpha=0.15,label="Diferencial")
ax.annotate("0,375 pp",(xs[-1],4.06),xytext=(-40,18),textcoords="offset points",fontsize=9,color=NA)
ax.set_xticks(xs[::3]); ax.set_xticklabels([lab(n) for n,_ in br][::3],rotation=45); ax.set_ylabel("%"); ax.set_ylim(3,7)
ax.legend(frameon=False,fontsize=9,loc="upper right"); save(fig,"g4.png")

# g5 importaciones OCP por origen y año (Veritrade)
I=json.load(open('/tmp/claude-0/imp.json'))
fig,(a1,a2)=plt.subplots(1,2,figsize=(7.5,3.4))
yrs=["2023","2024","2025","2026"]; v=[I["yr"][y]/1e6 for y in yrs]
a1.bar(["2023","2024","2025","2026*"],v,color=AZ); [vl(a1,i,x,f1(x,2)) for i,x in enumerate(v)]; a1.set_title("CIF importado por año (US$ MM)",fontsize=10); a1.set_ylim(0,5.4)
pa=sorted(I["pais"].items(),key=lambda x:-x[1])[:6]
a2.barh([p for p,_ in pa][::-1],[x/1e6 for _,x in pa][::-1],color=[NA if p in("ITALIA","ALEMANIA","FINLANDIA") else CEL for p,_ in pa][::-1])
for i,(p,x) in enumerate(pa[::-1]): a2.text(x/1e6+0.05,i,f1(x/1e6,2),va="center",fontsize=9)
a2.set_title("Por país de origen (US$ MM)",fontsize=10); a2.set_xlim(0,5.2); a2.tick_params(axis="y",labelsize=9)
save(fig,"g5.png")

# g6 PBI total vs minería metálica
yy=["2022","2023","2024","2025","2026*","2027P","2028P"]; pbi=[2.8,-0.4,3.5,3.4,3.1,3.44,3.96]; mm=[0.0,10.9,3.2,1.9,-0.2,3.02,1.46]
fig,ax=plt.subplots(figsize=(7.5,3.4)); x=np.arange(len(yy)); w=0.38
ax.bar(x-w/2,pbi,w,color=GR,label="PBI total"); ax.bar(x+w/2,mm,w,color=NA,label="Minería metálica")
for xi,vi in zip(x-w/2,pbi): vl(ax,xi,max(vi,0),f1(vi))
for xi,vi in zip(x+w/2,mm): vl(ax,xi,max(vi,0),f1(vi))
ax.axhline(0,color="k",lw=0.8); ax.set_xticks(x); ax.set_xticklabels(yy); ax.set_ylabel("var. % real"); ax.legend(frameon=False,fontsize=9); ax.set_ylim(-1.5,12.5)
save(fig,"g6.png")

# g7 inflación
inf=y2526(L("PN01273PM")); ex=dict(L("PD12912AM"))
fig,ax=plt.subplots(figsize=(7.5,3.4)); xs=list(range(len(inf)))
ax.fill_between([-0.5,len(inf)-0.5],1,3,color=VE,alpha=0.12,label="Rango meta 1%–3%")
ax.plot(xs,[v for _,v in inf],color=RO,marker="o",ms=3,label="Inflación Lima, var. % 12 meses")
ax.plot(xs,[ex.get(n,np.nan) for n,_ in inf],color=AZ,ls="--",label="Expectativa de inflación a 12 meses")
ax.plot([len(inf)+1],[4.2],marker="*",ms=12,color=NA,ls="none",label="Proyección RI set-26 (dic-26): 4,2%")
vl(ax,len(inf)-1,inf[-1][1],"5,25",color=RO)
ax.set_xticks(xs[::2]); ax.set_xticklabels([lab(n) for n,_ in inf][::2],rotation=45); ax.set_ylabel("%"); ax.legend(frameon=False,fontsize=9,loc="upper left"); ax.set_ylim(0,6.2); save(fig,"g7.png")

# g8 tipo de cambio
tc=y2526(L("PN01210PM"))
fig,ax=plt.subplots(figsize=(7.5,3.4)); xs=list(range(len(tc)))
ax.plot(xs,[v for _,v in tc],color=AZ,marker="o",ms=3,label="Tipo de cambio bancario, promedio mensual")
ax.plot([xs[-1],xs[-1]+1],[tc[-1][1],3.412],color=AZ,ls=":",marker="D",ms=4)
ax.annotate("3,412 (9-nov-26)",(xs[-1]+1,3.412),xytext=(-10,-30),textcoords="offset points",fontsize=9,ha="center")
ax.fill_between([xs[-1]+1,xs[-1]+3],3.40,3.50,color=NA,alpha=0.25,label="Rango esperado S/3,40–3,50")
ax.set_xticks(xs[::2]); ax.set_xticklabels([lab(n) for n,_ in tc][::2],rotation=45); ax.set_ylabel("S/ por US$")
for i in [0,11,len(tc)-1]: vl(ax,i,tc[i][1],f1(tc[i][1],3))
ax.legend(frameon=False,fontsize=9,loc="upper right"); ax.set_ylim(3.25,3.85); save(fig,"g8.png")

# g9 balanza comercial
yrs3=["2025","2026P","2027P"]; X=[93993,119876,124274]; Mm=[58560,71011,75995]; SB=[a-b for a,b in zip(X,Mm)]
fig,ax=plt.subplots(figsize=(7.5,3.4)); x=np.arange(3); w=0.27
for i,(v,c,l) in enumerate([(X,VE,"Exportaciones"),(Mm,RO,"Importaciones"),(SB,AZ,"Saldo comercial")]):
    ax.bar(x+(i-1)*w,[t/1000 for t in v],w,color=c,label=l)
    for xi,vi in zip(x+(i-1)*w,v): vl(ax,xi,vi/1000,f1(vi/1000))
ax.set_xticks(x); ax.set_xticklabels(yrs3); ax.set_ylabel("US$ miles de millones"); ax.legend(frameon=False,ncol=3,fontsize=9); ax.set_ylim(0,140); save(fig,"g9.png")

# g10 liquidez vs inflación
liq=y2526(L("PN00189MM")); infd=dict(inf)
fig,ax=plt.subplots(figsize=(7.5,3.4)); xs=list(range(len(liq)))
ax.plot(xs,[v for _,v in liq],color=AZ,marker="o",ms=3,label="Liquidez en soles (M), var. % 12 meses")
ax.plot(xs,[infd.get(n,np.nan) for n,_ in liq],color=RO,marker="s",ms=3,label="Inflación Lima (P), var. % 12 meses")
ax.axhline(3.2,color=GR,ls="--",lw=1,label="PBI real 2026P (Y): 3,2%")
vl(ax,len(liq)-1,liq[-1][1],f1(liq[-1][1]),color=AZ)
ax.set_xticks(xs[::2]); ax.set_xticklabels([lab(n) for n,_ in liq][::2],rotation=45); ax.set_ylabel("%"); ax.legend(frameon=False,fontsize=9,loc="upper left"); ax.set_ylim(0,22); save(fig,"g10.png")

# g11 EEFF estimados OCP: ventas, EBITDA, margen
yy=Y[:4]; ve=[R['ventas'][y] for y in yy]; eb=[R['ebitda'][y] for y in yy]; mg=[R['ebitda'][y]/R['ventas'][y]*100 for y in yy]
fig,ax=plt.subplots(figsize=(7.5,3.4)); x=np.arange(4); w=0.38
ax.bar(x-w/2,ve,w,color=AZ,label="Ventas netas (US$ MM)"); ax.bar(x+w/2,eb,w,color=CEL,label="EBITDA (US$ MM)")
for xi,v in zip(x-w/2,ve): vl(ax,xi,v,f1(v))
for xi,v in zip(x+w/2,eb): vl(ax,xi,v,f1(v))
ax2=ax.twinx(); ax2.plot(x,mg,color=RO,marker="o",label="Margen EBITDA (%, eje der.)"); ax2.grid(False); ax2.spines["right"].set_visible(True); ax2.set_ylim(0,70)
for xi,v in zip(x,mg): ax2.annotate(f1(v)+"%",(xi,v),xytext=(14,-4),textcoords="offset points",fontsize=9,color=RO)
ax.set_xticks(x); ax.set_xticklabels(["2023","2024","2025","2026P"]); ax.set_ylim(0,290); dual_legend(ax,ax2,fontsize=9,loc="upper left")
save(fig,"g11.png")

# f1 ventas por escenario
fig,ax=plt.subplots(figsize=(7.5,3.6))
hist=[R['ventas'][y] for y in ["2023","2024","2025","2026P"]]
ax.plot([0,1,2,3],hist,color=AZ,marker="o",lw=2.5,label="Estimado (2023-2025) y 2026P")
for k,c in [("Alto",VE),("Base",AZ),("Bajo",RO)]:
    v=[hist[-1]]+[SC['out'][k][y]['ventas'] for y in ["2027P","2028P"]]
    ax.plot([3,4,5],v,color=c,ls="--",marker="s",label=f"Escenario {k.lower()}")
    vl(ax,5,v[-1],f1(v[-1]),color=c)
for i,v in enumerate(hist): vl(ax,i,v,f1(v))
ax.set_xticks(range(6)); ax.set_xticklabels(["2023","2024","2025","2026P","2027P","2028P"]); ax.set_ylabel("US$ millones"); ax.set_ylim(0,330)
ax.legend(frameon=False,fontsize=9,loc="upper left"); save(fig,"f1.png")

# f2 costo de operación por tonelada vs inflación y referencias
yy=["2023","2024","2025","2026P"]; ct=[60,50,52,56]; volcan=[51.9,49.2,54.1,65.4]; infl=[3.2,2.0,1.5,5.25]
fig,ax=plt.subplots(figsize=(7.5,3.4)); x=np.arange(4); w=0.38
ax.bar(x-w/2,ct,w,color=AZ,label="OCP, costo estimado (US$/t)"); ax.bar(x+w/2,volcan,w,color=GR,label="Volcan, costo unitario (US$/t)")
for xi,v in zip(x-w/2,ct): vl(ax,xi,v,f1(v,0))
for xi,v in zip(x+w/2,volcan): vl(ax,xi,v,f1(v))
ax2=ax.twinx(); ax2.plot(x,infl,color=RO,marker="o",label="Inflación Lima fin de periodo (%, eje der.)"); ax2.grid(False); ax2.spines["right"].set_visible(True); ax2.set_ylim(0,12)
ax.set_xticks(x); ax.set_xticklabels(yy); ax.set_ylim(0,85); dual_legend(ax,ax2,fontsize=9,loc="upper left"); save(fig,"f2.png")

# f3 sensibilidad EBITDA 2027 al tipo de cambio y al precio del cobre
pc=np.linspace(3.5,7.5,9)
import importlib.util
spec=importlib.util.spec_from_file_location("scen",os.path.join(S,"scen_lib.py")); sl=importlib.util.module_from_spec(spec); spec.loader.exec_module(sl)
fig,ax=plt.subplots(figsize=(7.5,3.4))
for tcm,c,l in [(0.95,RO,"Sol apreciado (TC −5%)"),(1.0,AZ,"TC base (S/3,45)"),(1.10,VE,"Sol depreciado (TC +10%)")]:
    ax.plot(pc,[sl.pl('2027P',p,55,tc_mult=tcm)['ebitda'] for p in pc],color=c,lw=2,label=l)
ax.axvline(5.70,color=GR,ls=":"); ax.text(5.75,10,"Base MMM 2027: US$5,70",fontsize=9,color=GR)
ax.axvline(2.83,color=RO,ls=":"); ax.text(2.9,150,"Equilibrio\n(EBIT = 0):\nUS$2,83",fontsize=9,color=RO); ax.axhline(0,color="k",lw=0.6)
ax.set_xlabel("Precio del cobre 2027 (US$/lb)"); ax.set_ylabel("EBITDA 2027P (US$ MM)"); ax.legend(frameon=False,fontsize=9,loc="upper left"); save(fig,"f3.png")

# f4 deuda y gastos financieros
yy=["2023","2024","2025","2026P"]; de=[R['deuda'][y] for y in yy]; gi=[R['int'][y] for y in yy]
fig,ax=plt.subplots(figsize=(7.5,3.4)); x=np.arange(4)
ax.bar(x,de,0.5,color=CEL,label="Deuda con vinculadas / prepagos (US$ MM)")
for xi,v in zip(x,de): vl(ax,xi,v,f1(v))
ax2=ax.twinx(); ax2.plot(x,gi,color=RO,marker="o",label="Gastos financieros (US$ MM, eje der.)"); ax2.grid(False); ax2.spines["right"].set_visible(True); ax2.set_ylim(0,8)
ax.set_xticks(x); ax.set_xticklabels(yy); ax.set_ylim(0,65); dual_legend(ax,ax2,fontsize=9,loc="upper right"); save(fig,"f4.png")

# ---------- modelos ----------
def model_axes(xl,yl):
    fig,ax=plt.subplots(figsize=(7.0,4.3)); ax.grid(False); ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(0,10); ax.set_ylim(0,10); ax.set_xlabel(xl,fontweight="bold"); ax.set_ylabel(yl,fontweight="bold"); return fig,ax
def eq(ax,x,y,t,col,dx=8,dy=-14):
    ax.plot([x,x],[0,y],":",color=GR,lw=1); ax.plot([0,x],[y,y],":",color=GR,lw=1)
    ax.plot(x,y,"o",color=col,ms=8,zorder=5); ax.annotate(t,(x,y),xytext=(dx,dy),textcoords="offset points",color=col,fontweight="bold",fontsize=11)
def arrow(ax,a,b,col=NA): ax.annotate("",b,a,arrowprops=dict(arrowstyle="-|>",lw=2.5,color=col))
q=np.linspace(0.6,9.4,100)
# m1 mercado de cobre: D se expande, S rígida
fig,ax=model_axes("Cantidad de cobre refinado (t)","Precio del cobre (US$/lb)")
ax.plot(q,9.2-0.75*q,color=CEL,lw=2.5); ax.text(0.7,8.9,"D₀ (2025)",color=CEL,fontweight="bold")
ax.plot(q,10.6-0.75*q,color=CEL,lw=2.5,ls="--"); ax.text(2.6,9.1,"D₁ (China 4,5%; IA y redes eléctricas)",color=CEL,fontweight="bold")
ax.plot(q,-3.0+1.6*q,color=AZ,lw=2.5); ax.text(7.7,6.3,"S (oferta de mina rígida;\nTC/RC = US$0)",color=AZ,fontweight="bold",fontsize=9)
eq(ax,5.191,5.306,"E₀: US$4,51 (2025)",CEL,dx=12,dy=-20); eq(ax,5.787,6.26,"E₁: US$6,14 (2026)",RO,dx=-150,dy=10)
arrow(ax,(4.5,6.3),(5.4,7.0)); save(fig,"m1.png")
# m2 cambiario
fig,ax=model_axes("Cantidad de dólares (US$)","Tipo de cambio (S/ por US$)")
ax.plot(q,9.2-0.75*q,color=CEL,lw=2.5); ax.text(0.7,8.9,"D$ (Fed 3,75%–4,00%; WTI US$99)",color=CEL,fontweight="bold")
ax.plot(q,0.9+0.75*q,color=VE,lw=2.5); ax.text(7.6,6.0,"S$₀",color=VE,fontweight="bold")
ax.plot(q,0.1+0.75*q,color=VE,lw=2.5,ls="--"); ax.text(6.6,3.6,"S$₁ (exportaciones de cobre;\nsaldo US$48.865 MM)",color=VE,fontweight="bold",fontsize=9)
eq(ax,5.53,5.05,"E₀: S/3,568 (prom. 2025)",CEL,dx=-170,dy=-22); eq(ax,6.07,4.65,"E₁: S/3,412 (9-nov-26)",VE,dx=10,dy=-22)
arrow(ax,(7.6,6.6),(7.9,6.0),VE); save(fig,"m2.png")
# m3 OA-DA
fig,ax=model_axes("Producto real (Y)","Nivel de precios (P)")
ax.plot(q,9.2-0.75*q,color=CEL,lw=2.5); ax.text(0.7,8.9,"DA₀",color=CEL,fontweight="bold")
ax.plot(q,9.9-0.75*q,color=CEL,lw=2.5,ls="--"); ax.text(1.0,9.6,"DA₁ (inversión privada +14,0%; TI +18,1%)",color=CEL,fontweight="bold")
ax.plot(q,0.6+0.75*q,color=AZ,lw=2.5); ax.text(8.6,6.7,"OA₀",color=AZ,fontweight="bold")
ax.plot(q,1.5+0.75*q,color=RO,lw=2.5,ls="--"); ax.text(6.4,7.4,"OA₁ (petróleo, El Niño, minería −0,2%)",color=RO,fontweight="bold",fontsize=9)
ax.axvline(5.75,color=NA,ls="--",lw=2); ax.text(5.85,0.4,"Yn (OALP)",color=NA,fontweight="bold")
eq(ax,5.733,4.9,"E₀ 2025: π 1,5%; PBI 3,4%",AZ,dx=12,dy=-34); eq(ax,5.6,5.7,"E₁ 2026: π 5,25%; PBI 3,2%",RO,dx=-205,dy=8)
save(fig,"m3.png")
# m4 isocuanta minera
fig,ax=model_axes("Trabajo (L): 604 trabajadores y contratistas","Capital (K): equipos, filtros, bombas")
L_=np.linspace(1.2,9.5,100)
ax.plot(L_,16/L_,color=AZ,lw=2.5); ax.text(6.9,1.25,"Q₀: 16.545 TMF Cu (2025)",color=AZ,fontweight="bold")
ax.plot(L_,20/L_,color=AZ,lw=2.5,ls="--"); ax.text(6.9,3.0,"Q₁: ampliación a 12.000 t/d",color=AZ,fontweight="bold")
ax.plot(L_,8.0-1.0*L_,color=CEL,lw=2.5); ax.text(0.2,7.4,"Isocosto₀",color=CEL,fontweight="bold")
ax.plot(L_,9.238-1.3333*L_,color=RO,lw=2.5,ls="--"); ax.text(4.6,6.9,"Isocosto₁: ↑w (inflación 5,25%)\ny equipo importado en US$/EUR",color=RO,fontweight="bold",fontsize=9)
eq(ax,4.0,4.0,"A: L/K inicial",CEL,dx=10,dy=-16); eq(ax,3.464,4.619,"B: más capital por trabajador",RO,dx=12,dy=14)
save(fig,"m4.png")
# m5 IS-MP
fig,ax=model_axes("Producto real (Y)","Tasa de interés real (r)")
ax.plot(q,9.2-0.85*q,color=CEL,lw=2.5); ax.text(0.7,8.8,"IS₀",color=CEL,fontweight="bold")
ax.plot(q,9.9-0.85*q,color=CEL,lw=2.5,ls="--"); ax.text(1.4,9.1,"IS₁ (inversión minera y crédito +10,3%)",color=CEL,fontweight="bold")
ax.axhline(4.2,color=AZ,lw=2.5); ax.text(8.0,3.7,"MP₀: r = 1,20%",color=AZ,fontweight="bold")
ax.axhline(5.0,color=RO,lw=2.5,ls="--"); ax.text(7.3,5.2,"MP₁: alza de 25 pb",color=RO,fontweight="bold")
eq(ax,6.7,4.2,"E₁",AZ,dx=6,dy=-18); eq(ax,5.76,5.0,"E₂",RO,dx=-24,dy=6)
arrow(ax,(7.2,4.4),(6.3,4.9)); save(fig,"m5.png")

# ---------- Ishikawa ----------
def ishikawa(name,efecto,espinas):
    fig,ax=plt.subplots(figsize=(7.5,4.3)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,6)
    ax.annotate("",(8.0,3),(0.3,3),arrowprops=dict(arrowstyle="-|>",lw=2,color="k"))
    ax.text(8.1,3,efecto,va="center",fontsize=10,fontweight="bold",bbox=dict(boxstyle="round",fc="#f2f2f2",ec="k"))
    xs=[1.6,4.1,6.6]
    for i,(tit,items,col) in enumerate(espinas):
        x=xs[i%3]; up=i<3; y0=5.6 if up else 0.4
        ax.plot([x,x+1.0],[y0,3],color=col,lw=1.5)
        ax.text(x,y0+(0.12 if up else -0.12),tit,ha="center",va="bottom" if up else "top",fontsize=10,fontweight="bold",color=col)
        for j,it in enumerate(items):
            yy=y0-(0.55+0.42*j) if up else y0+(0.55+0.42*j)
            ax.text(x+(yy-y0)/(3-y0)*1.0-0.05,yy,it,ha="right",va="center",fontsize=8.5)
    save(fig,name)
ishikawa("i1.png","Ventas y costos\nde OCP Cobriza\n2026-2027",[
 ("China y Y*",["Mundo 3,1% (2026)","China 4,5% → 4,2%","Demanda de cobre por IA"],VE),
 ("Cobre y plata",["Cu US$6,14/lb (+36%)","Ag US$71,6/oz (+79%)","TC/RC = US$0"],VE),
 ("Fed y dólar",["Fed 3,75%–4,00%","i − i* = 0,375 pp","TC S/3,412"],RO),
 ("Petróleo",["WTI US$98,9 (oct-26)","Diésel y fletes al Callao","Explosivos y energía"],RO),
 ("π EE.UU. y Europa",["PCE EE.UU. 3,7%","Capex importado US$7,3 MM","Italia y Alemania 77%"],RO),
 ("Traders",["Glencore (Perubar)","Mercuria","Prepagos y términos"],GR)])
ishikawa("i2.png","Producción, costos\ny caja de OCP\n2026-2028",[
 ("PBI minero",["Minería metálica −0,2% (2026)","MMM: +3,0% (2027)","OCP 0,6% del Cu nacional"],VE),
 ("Inflación",["π Lima 5,25%","Insumos locales","Planilla de 604 trabajadores"],RO),
 ("Tipo de cambio",["Ventas en US$","~55% del costo en soles","S/3,40–3,50"],VE),
 ("Tasa y Fisher",["Referencia 4,25%","r ex ante 1,20%","r ex post −1,00%"],GR),
 ("TI y BP",["TI +18,1%","CA +4,0% del PBI","RIN US$96.668 MM"],VE),
 ("Fisco y regulación",["Regalía + IEM","OEFA: 34,2 UIT","MEIA US$93,3 MM"],RO)])
ishikawa("i5.png","Ventas de OCP\n(US$ MM)",[
 ("Precio del cobre",["US$4,51 → 6,14/lb","ε ventas = 0,86","Base MMM US$5,70 (2027)"],VE),
 ("Volumen",["16.545 TMF (2025)","Ley ~1% Cu (supuesto)","Planta 9,1 → 12 kt/d"],AZ),
 ("Plata",["711 mil oz (2025)","US$40 → 72/oz","Crédito de subproducto"],VE),
 ("Términos comerciales",["TC/RC de US$80 a US$0","Pagable 96,5%","Flete al Callao"],GR),
 ("Clientes",["Perubar (Glencore)","Mercuria","China, destino final"],GR),
 ("PBI minero",["Minería metálica 1,9% (2025)","Huancavelica +11,7%","MMM 1,7% (2026)"],AZ)])
ishikawa("i6.png","Costo operativo\nde OCP (US$/t)",[
 ("Inflación local",["π 5,25% (oct-26)","Reactivos y explosivos","Bolas de molienda"],RO),
 ("Petróleo",["WTI US$98,9","Diésel de flota y fletes","Energía"],RO),
 ("Salarios",["604 trabajadores","Participación 8%","Convenio colectivo"],RO),
 ("Escala",["Ritmo ~5.100 t/d","Planta de 9.100 t/d","Costo fijo diluido"],VE),
 ("Referencias",["Volcan 49-70 US$/t","Cerro Lindo 39,9 US$/t","OCP 50-56 US$/t"],GR),
 ("Tipo de cambio",["~55% en soles","Sol fuerte encarece","US$ cubre ventas"],GR)])
ishikawa("i7.png","Exposición\ncambiaria de OCP",[
 ("Ventas",["100% en US$","Precio LME","Pagos del trader"],VE),
 ("Costos",["~55% en soles","Planilla y servicios","Insumos locales"],RO),
 ("Capex importado",["US$7,3 MM CIF","Italia 4,4; Alemania 1,2","Euro y dólar"],RO),
 ("Fed",["3,75%–4,00%","Diferencial 0,375 pp","Flujo de capitales"],GR),
 ("BCRP",["Compras US$15.715 MM","RIN US$96.668 MM","TC S/3,412"],VE),
 ("Impuestos",["Regalía en US$","IR en soles","Diferencia de cambio"],GR)])
ishikawa("i8.png","Costo financiero\nde OCP",[
 ("BCRP",["Referencia 4,25%","r ex post −1,00%","Sesgo al alza"],GR),
 ("Fed y SOFR",["3,75%–4,00%","Prepagos en US$","Préstamos vinculados"],RO),
 ("Deuda estimada",["US$45,6 MM (2025)","0 en 2026P","Tasa 8% (supuesto)"],AZ),
 ("Capex",["US$150 MM (2023-26)","MEIA US$93,3 MM","ITS US$8,25 MM"],AZ),
 ("Capital",["US$30 MM inicial","Reducción S/22,6 MM (2024)","Grupo Dyer Coriat"],GR),
 ("Caja",["FCF US$50,9 MM (2026P)","Capital de trabajo","Pagos provisionales"],VE)])
ishikawa("i9.png","Utilidad y caja\nde OCP\n2026-2028",[
 ("Cobre",["Alto US$7,0; base 5,7; bajo 4,5","EBITDA 164 / 117 / 64","Equilibrio US$2,83"],VE),
 ("Plata",["US$72 → 35-65/oz","~16% de los ingresos","Crédito de subproducto"],VE),
 ("Inflación",["+1 pp = US$1,0 MM","Costo US$56-58/t","Planilla"],RO),
 ("Tipo de cambio",["TC +10% → EBITDA +US$4,5 MM","Costos en soles","Capex en EUR"],GR),
 ("Tasa",["Deuda 0 en 2026P","Prepagos con SOFR","Costo de capital"],GR),
 ("Clientes",["Glencore, Mercuria","China 4,2% (2027)","Términos TC/RC"],RO)])
print("ok",sorted(os.listdir(OUT)))
# g12 empleo e ingresos
u=y2526(L("PN38063GM")); uj=dict(L("PN38066GM")); yi=dict(L("PN38070GM"))
fig,(a1,a2)=plt.subplots(1,2,figsize=(7.5,3.4)); xs=list(range(len(u)))
a1.plot(xs,[v for _,v in u],color=AZ,label="Desempleo total"); a1.plot(xs,[uj[n] for n,_ in u],color=RO,label="Desempleo 14-24 años")
a1.set_xticks(xs[::4]); a1.set_xticklabels([lab(n) for n,_ in u][::4],rotation=45,fontsize=9); a1.set_ylabel("%"); a1.legend(frameon=False,fontsize=9)
vl(a1,xs[-1],u[-1][1],"4,4",color=AZ)
a2.plot(xs,[yi[n] for n,_ in u],color=VE,marker="o",ms=3); a2.set_xticks(xs[::4]); a2.set_xticklabels([lab(n) for n,_ in u][::4],rotation=45,fontsize=9)
a2.set_ylabel("S/ por mes (nominal)"); a2.set_title("Ingreso promedio mensual",fontsize=10); a1.set_title("Tasa de desempleo",fontsize=10)
vl(a2,xs[-1],yi[u[-1][0]],"2.302"); save(fig,"g12.png")

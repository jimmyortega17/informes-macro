import json
def load(c):
    d=json.load(open(f'bcrp/{c}.json')); return {p['name']:float(p['values'][0]) for p in d['periods'] if p['values'][0] not in ('n.d.',)}
DI=load('PN02528AQ');CP=load('PN02529AQ');X=load('PN02536AQ');M=load('PN02537AQ')
ann=lambda s,y: sum(s[f'T{q}.{y%100}'] for q in range(1,5))
pbi={y:ann(DI,y)+ann(X,y)-ann(M,y) for y in range(2021,2026)}
cp={y:ann(CP,y) for y in range(2021,2026)}
ipc=load('IPC'); print(list(ipc)[:2])
ipcavg={y:sum(v for k,v in ipc.items() if k.endswith("."+str(y)))/12 for y in range(2021,2026)}
rev={2022:264107390,2023:321787880,2024:420436230,2025:594839418}
for y in range(2022,2026):
    gp=pbi[y]/pbi[y-1]-1; gc=cp[y]/cp[y-1]-1; pi=ipcavg[y]/ipcavg[y-1]-1
    gr=rev[y]/rev[y-1]-1 if y>2022 else None
    s=f"{y}: PBI {gp*100:.2f}%  CP {gc*100:.2f}%  infl.prom {pi*100:.2f}%"
    if gr is not None:
        grr=(1+gr)/(1+pi)-1
        s+=f"  ingresos nom {gr*100:.2f}% real {grr*100:.2f}%  e_nom/PBI {gr/gp:.2f}  e_real/PBI {grr/gp:.2f}  e_real/CP {grr/gc:.2f}"
    print(s)
# cumulative 2022-2025
cg=lambda d,a,b:(d[b]/d[a])**(1/(b-a))-1
gr=cg(rev,2022,2025); gp=cg(pbi,2022,2025); gc=cg(cp,2022,2025); pi=cg(ipcavg,2022,2025)
grr=(1+gr)/(1+pi)-1
print(f"CAGR 22-25: ingresos {gr*100:.2f}% real {grr*100:.2f}% PBI {gp*100:.2f}% CP {gc*100:.2f}% pi {pi*100:.2f}%  e_nom/PBI {gr/gp:.2f} e_real/PBI {grr/gp:.2f} e_real/CP {grr/gc:.2f}")
print({y:round(pbi[y]) for y in pbi})
